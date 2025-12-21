from fastapi import APIRouter, Depends, HTTPException, status, Request
from supabase.client import Client
from app.database import get_auth_db
from json import loads, dumps
from typing import Annotated
from app.services.redis_service import RedisService
from app.services.meal_service import MealService
from app.schemas.meal import MealCreate, MealUpdate, MealResponse

router = APIRouter()

@router.get("/", 
    status_code=status.HTTP_200_OK,
    summary="List All Meals",
    description="Retrieve a list of all meal entries stored in the system."
)
async def list_meals(request: Request, db: Annotated[Client, Depends(get_auth_db)]):
    response = db.auth.get_user()
    user = response.user
    cached = await RedisService.get(f"meals:{user.id}")
    if cached:
        return {"meals": loads(cached)}
    meals = await MealService.list_meals(db)
    await RedisService.set(f"meals:{user.id}", dumps(meals), expire=300)
    return {"meals": meals}

@router.post("/", 
    status_code=status.HTTP_201_CREATED,
    summary="Create a New Meal",
    description="Add a new meal entry to the system.",
    response_model=MealResponse
)
def create_meal(meal: MealCreate, request: Request, db: Annotated[Client, Depends(get_auth_db)]):
    try:
        meal_data = MealService.create_meal(db, meal)
        return meal_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{meal_id}", 
    status_code=status.HTTP_200_OK,
    summary="Update an Existing Meal",
    description="Update the details of an existing meal entry by its ID."
)
def update_meal(meal_id: int, meal: MealUpdate, request: Request, db: Annotated[Client, Depends(get_auth_db)]):
    try:
        meal = MealService.update_meal(db, meal_id, meal)
        if not meal:
            raise HTTPException(status_code=404, detail="Meal not found")
        return {"message": f"Meal with ID {meal_id} updated", "meal": meal}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{meal_id}", 
    status_code=status.HTTP_200_OK,
    summary="Get Meal by ID",
    description="Retrieve the details of a specific meal entry by its ID."
)
async def read_meal(meal_id: int, request: Request, db: Annotated[Client, Depends(get_auth_db)]):
    response = db.auth.get_user()
    user = response.user
    cached = await RedisService.get(f"meal:{user.id}:{meal_id}")
    if cached:
        return {"meal": loads(cached)}
    meal = MealService.get_meal(db, meal_id)
    if not meal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meal not found")
    await RedisService.set(f"meal:{user.id}:{meal_id}", dumps(meal), expire=300)
    return {"meal": meal}

@router.delete("/{meal_id}", 
    status_code=status.HTTP_200_OK,
    summary="Delete Meal by ID",
    description="Delete a specific meal entry by its ID."
)
def delete_meal(meal_id: int, request: Request, db: Annotated[Client, Depends(get_auth_db)]):
    success = MealService.delete_meal(db, meal_id)
    if success:
        return {"message": f"Meal with ID {meal_id} deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meal not found")
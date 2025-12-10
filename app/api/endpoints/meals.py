from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from typing import Annotated
from app.services.meal_service import MealService
from app.schemas.meal import MealCreate, MealUpdate

router = APIRouter()

@router.get("/", 
    status_code=status.HTTP_200_OK,
    summary="List All Meals",
    description="Retrieve a list of all meal entries stored in the system."
)
async def list_meals(db: Annotated[Session, Depends(get_db)]):
    meals = MealService.list_meals(db)
    return {"meals": meals}

@router.post("/", 
    status_code=status.HTTP_201_CREATED,
    summary="Create a New Meal",
    description="Add a new meal entry to the system."
)
async def create_meal(meal: MealCreate, db: Annotated[Session, Depends(get_db)]):
    try:
        meal = MealService.create_meal(db, meal)
        return {"message": "Meal created", "meal": meal}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{meal_id}", 
    status_code=status.HTTP_200_OK,
    summary="Update an Existing Meal",
    description="Update the details of an existing meal entry by its ID."
)
async def update_meal(meal_id: int, meal: MealUpdate, db: Annotated[Session, Depends(get_db)]):
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
async def read_meal(meal_id: int, db: Annotated[Session, Depends(get_db)]):
    meal = MealService.get_meal(db, meal_id)
    if not meal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meal not found")
    return {"meal": meal}

@router.delete("/{meal_id}", 
    status_code=status.HTTP_200_OK,
    summary="Delete Meal by ID",
    description="Delete a specific meal entry by its ID."
)
async def delete_meal(meal_id: int, db: Annotated[Session, Depends(get_db)]):
    success = MealService.delete_meal(db, meal_id)
    if success:
        return {"message": f"Meal with ID {meal_id} deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meal not found")
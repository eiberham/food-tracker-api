from fastapi import APIRouter, Depends, HTTPException, status
from supabase.client import Client
from typing import Annotated
from json import loads, dumps
from app.services.food_service import FoodService
from app.services.redis_service import RedisService
from app.schemas.food import FoodCreate, FoodUpdate
from app.database import get_auth_db

router = APIRouter()

@router.get("/", 
    status_code=status.HTTP_200_OK,
    summary="List All Foods",
    description="Retrieve a list of all food items stored in the system."
)
async def list_foods(db: Annotated[Client, Depends(get_auth_db)]):
    response = db.auth.get_user()
    user = response.user
    cached = await RedisService.get(f"foods:{user.id}")
    if cached:
        return {"foods": loads(cached)}
    foods = FoodService.list_foods(db)
    await RedisService.set(f"foods:{user.id}", dumps(foods), expire=300)
    return {"foods": foods}

@router.post("/", 
    status_code=status.HTTP_201_CREATED,
    summary="Create a New Food",
    description="Add a new food item to the system."
)
def create_food(food: FoodCreate, db: Annotated[Client, Depends(get_auth_db)]):
    food = FoodService.create_food(db, food)
    return {"message": "Food created", "food": food}

@router.put("/{food_id}", 
    status_code=status.HTTP_200_OK,
    summary="Update an Existing Food",
    description="Update the details of an existing food item by its ID."
)
def update_food(food_id: int, food: FoodUpdate, db: Annotated[Client, Depends(get_auth_db)]):
    food = FoodService.update_food(db, food_id, food)
    if not food:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food not found")
    
    return {"message": f"Food with ID {food_id} updated", "food": food}

@router.get("/{food_id}", 
    status_code=status.HTTP_200_OK,
    summary="Get Food by ID",
    description="Retrieve the details of a specific food item by its ID."
)
async def read_food(food_id: int, db: Annotated[Client, Depends(get_auth_db)]):
    response = db.auth.get_user()
    user = response.user
    cached = await RedisService.get(f"food:{user.id}:{food_id}")
    if cached:
        return {"food": loads(cached)}
    food = FoodService.get_food(db, food_id)
    if not food:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food not found")
    await RedisService.set(f"food:{user.id}:{food_id}", dumps(food), expire=300)
    return {"food": food}

@router.delete("/{food_id}", 
    status_code=status.HTTP_200_OK,
    summary="Delete Food by ID",
    description="Delete a specific food item by its ID."
)
def delete_food(food_id: int, db: Annotated[Client, Depends(get_auth_db)]):
    success = FoodService.delete_food(db, food_id)
    if success:
        return {"message": f"Food with ID {food_id} deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food not found")
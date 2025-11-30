from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from app.services.FoodService import FoodService
from app.schemas.Food import FoodCreate, FoodUpdate
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
async def list_foods(db: Annotated[Session, Depends(get_db)]):
    foods = FoodService.list_foods(db)
    return {"foods": foods}

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_food(food: FoodCreate, db: Annotated[Session, Depends(get_db)]):
    food = FoodService.create_food(db, food)
    return {"message": "Food created", "food": food}

@router.put("/{food_id}", status_code=status.HTTP_200_OK)
async def update_food(food_id: int, food: FoodUpdate, db: Annotated[Session, Depends(get_db)]):
    food = FoodService.update_food(db, food_id, food)
    if not food:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food not found")
    
    return {"message": f"Food with ID {food_id} updated", "food": food}

@router.get("/{food_id}", status_code=status.HTTP_200_OK)
async def read_food(food_id: int, db: Annotated[Session, Depends(get_db)]):
    food = FoodService.get_food(db, food_id)
    if not food:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food not found")
    return {"food": food}

@router.delete("/{food_id}", status_code=status.HTTP_200_OK)
async def delete_food(food_id: int, db: Annotated[Session, Depends(get_db)]):
    success = FoodService.delete_food(db, food_id)
    if success:
        return {"message": f"Food with ID {food_id} deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food not found")
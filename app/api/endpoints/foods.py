from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from app.services.FoodService import FoodService
from app.schemas.Food import FoodCreate, FoodUpdate
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/")
async def list_foods(db: Annotated[Session, Depends(get_db)]):
    foods = FoodService.list_foods(db)
    return {"foods": foods}

@router.post("/")
async def create_food(food: FoodCreate, db: Annotated[Session, Depends(get_db)]):
    food = FoodService.create_food(db, food)
    return {"message": "Food created", "food": food}

@router.put("/{food_id}")
async def update_food(food_id: int, food: FoodUpdate, db: Annotated[Session, Depends(get_db)]):
    food = FoodService.update_food(db, food_id, food)
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    
    return {"message": f"Food with ID {food_id} updated", "food": food}

@router.get("/{food_id}")
async def read_food(food_id: int, db: Annotated[Session, Depends(get_db)]):
    food = FoodService.get_food(db, food_id)
    return {"food": food}

@router.delete("/{food_id}")
async def delete_food(food_id: int, db: Annotated[Session, Depends(get_db)]):
    success = FoodService.delete_food(db, food_id)
    if success:
        return {"message": f"Food with ID {food_id} deleted"}
    raise HTTPException(status_code=404, detail="Food not found")
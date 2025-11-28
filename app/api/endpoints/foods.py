from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_root():
    return "Welcome to the foods endpoint."

@router.post("/")
async def create_food(food: dict):
    return {"message": "Food created", "food": food}
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_root():
    return "Welcome to the foods endpoint."

@router.post("/")
async def create_food(food: dict):
    return {"message": "Food created", "food": food}

@router.put("/{food_id}")
async def update_food(food_id: int, food: dict):
    return {"message": f"Food with ID {food_id} updated", "food": food}

@router.get("/{food_id}")
async def read_food(food_id: int):
    return {"food_id": food_id, "description": f"Food{food_id} details"}

@router.delete("/{food_id}")
async def delete_food(food_id: int):
    return {"message": f"Food with ID {food_id} deleted"}
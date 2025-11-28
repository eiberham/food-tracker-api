from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_root():
    return "Food tracker meals endpoint"

@router.post("/")
async def create_meal(meal: dict):
    return {"message": "Meal created", "meal": meal}

@router.put("/{meal_id}")
async def update_meal(meal_id: int, meal: dict):
    return {"message": f"Meal with ID {meal_id} updated", "meal": meal}

@router.get("/{meal_id}")
async def read_meal(meal_id: int):
    return {"meal_id": meal_id, "description": f"Meal{meal_id} details"}

@router.delete("/{meal_id}")
async def delete_meal(meal_id: int):
    return {"message": f"Meal with ID {meal_id} deleted"}
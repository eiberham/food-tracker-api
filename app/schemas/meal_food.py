from pydantic import BaseModel

class MealFoodBase(BaseModel):
    meal_id: int
    food_id: int

class MealFoodCreate(MealFoodBase):
    pass

class MealFoodUpdate(BaseModel):
    pass
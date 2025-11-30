from pydantic import BaseModel

class MealBase(BaseModel):
    food_id: int
    user_id: int

class MealCreate(MealBase):
    pass

class MealUpdate(BaseModel):
    pass
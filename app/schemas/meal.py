from pydantic import BaseModel
from typing import List

class MealBase(BaseModel):
    user_id: int
    name: str
    food_ids: List[int]

class MealCreate(MealBase):
    pass

class MealUpdate(BaseModel):
    pass
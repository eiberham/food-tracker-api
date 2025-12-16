from pydantic import BaseModel
from typing import List, Optional

class MealBase(BaseModel):
    name: str
    food_ids: List[int] = []

class MealCreate(MealBase):
    pass

class MealUpdate(BaseModel):
    name: Optional[str] = None
    food_ids: Optional[List[int]] = None

class MealResponse(BaseModel):
    id: int
    name: str
    user_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
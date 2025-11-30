from pydantic import BaseModel
from typing import Optional

class FoodBase(BaseModel):
    name: str
    category : Optional[str] = None
    histamine_level : Optional[str] = None
    notes : Optional[str] = None

class FoodCreate(FoodBase):
    pass

class FoodUpdate(BaseModel):
    pass

class FoodResponse(FoodBase):
    id: int

    class Config:
        from_attributes = True
    
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SymptomBase(BaseModel):
    user_id : int
    datetime : datetime
    symptom_type : Optional[str] = None
    severity: Optional[str] = None
    notes: Optional[str] = None
    meal_id: int


class SymptomCreate(SymptomBase):
    pass

class SymptomUpdate(BaseModel):
    symptom_type : Optional[str] = None
    severity: Optional[str] = None
    notes: Optional[str] = None
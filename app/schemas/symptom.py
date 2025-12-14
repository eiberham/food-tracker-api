from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SymptomBase(BaseModel):
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

class SymptomResponse(BaseModel):
    id: int
    datetime: datetime
    symptom_type: Optional[str] = None
    severity: Optional[str] = None
    notes: Optional[str] = None
    meal_id: int
    user_id: Optional[str] = None
    created_at: Optional[datetime] = None
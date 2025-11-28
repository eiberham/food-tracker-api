from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[EmailStr] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[EmailStr] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True  #sqlalchemy compatibility


class UserLogin(BaseModel):
    username: str
    password: str
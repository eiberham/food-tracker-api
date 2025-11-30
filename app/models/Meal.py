from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Meal(Base):
    __tablename__ = "meal"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(Integer, server_default=func.now())
    meal_foods = relationship("MealFood", back_populates="meal", cascade="all, delete-orphan")

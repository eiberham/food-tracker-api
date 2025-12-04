from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class MealFood(Base):
    __tablename__ = "meal_food"
    meal_id = Column(Integer, ForeignKey("meal.id"), primary_key=True)
    food_id = Column(Integer, ForeignKey("food.id"), primary_key=True)
    meal = relationship("Meal", back_populates="meal_foods")
    food = relationship("Food", back_populates="meal_foods")
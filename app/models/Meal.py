from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Meal(Base):
    __tablename__ = "meal"
    id = Column(Integer, primary_key=True, index=True)
    food_id = Column(Integer, ForeignKey("food.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_at = Column(Integer, server_default=func.now())

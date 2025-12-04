from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

class Symptom(Base):
    __tablename__ = "symptom"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    datetime = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    symptom_type = Column(String, nullable=True)
    severity = Column(String, nullable=True)
    notes = Column(String, nullable=True)
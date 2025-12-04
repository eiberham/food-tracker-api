from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from app.database import Base

class Document(Base):
    __tablename__ = "document"
    id = Column(BigInteger, primary_key=True, index=True)
    content = Column(String, nullable=False)
    embedding = Column(Vector(384), nullable=False)
    meta = Column(JSONB, nullable=True)
    filename = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
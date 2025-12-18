from sqlalchemy import Column, Integer, String,TIMESTAMP,ForeignKey,Float
from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True, nullable=False)
    passwordhash= Column(String(150), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    predictions = relationship(
        "PredictionHistory",
        back_populates="user",
        cascade="all, delete"
    )

class PredictionHistory(Base):
    __tablename__ = "predictions_history"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(TIMESTAMP(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    employee_id = Column(Integer, nullable=False)
    probability = Column(Float, nullable=False)
    user = relationship("User", back_populates="predictions")
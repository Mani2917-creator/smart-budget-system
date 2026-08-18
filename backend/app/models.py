from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    monthly_income = Column(Float, default=0.0)
    risk_profile = Column(String, default="moderate")

    created_at = Column(DateTime, default=datetime.utcnow)
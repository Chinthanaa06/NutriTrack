from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, String
from .database import Base

class Assessment(Base):
    __tablename__ = "assessments"
    id = Column(Integer, primary_key=True, index=True)
    participant_code = Column(String(80), nullable=False, index=True)
    age_years = Column(Float, nullable=False)
    sex_reference = Column(String(20), nullable=False)
    height_cm = Column(Float, nullable=False)
    weight_kg = Column(Float, nullable=False)
    dietary_diversity = Column(Integer, nullable=True)
    meals_per_day = Column(Integer, nullable=True)
    notes = Column(String(500), nullable=True)
    bmi = Column(Float, nullable=False)
    indicator_status = Column(String(40), nullable=False)
    indicator_message = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

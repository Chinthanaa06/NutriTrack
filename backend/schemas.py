from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class AssessmentCreate(BaseModel):
    participant_code: str = Field(min_length=1, max_length=80)
    age_years: float = Field(gt=0, le=120)
    sex_reference: str = Field(pattern="^(female|male|not_specified)$")
    height_cm: float = Field(gt=30, le=250)
    weight_kg: float = Field(gt=1, le=400)
    dietary_diversity: Optional[int] = Field(default=None, ge=0, le=10)
    meals_per_day: Optional[int] = Field(default=None, ge=0, le=10)
    notes: Optional[str] = Field(default=None, max_length=500)

class AssessmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    participant_code: str
    age_years: float
    sex_reference: str
    height_cm: float
    weight_kg: float
    bmi: float
    indicator_status: str
    indicator_message: str
    created_at: str

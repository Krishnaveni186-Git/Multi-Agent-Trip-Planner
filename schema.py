from datetime import date
from pydantic import BaseModel, Field, field_validator

class TripRequest(BaseModel):
    destination: str = Field(min_length=2, max_length=100)
    start_date: date
    end_date: date
    travelers: int = Field(ge=1, le=20)
    budget_inr: int = Field(gt=0, le=10_000_000)
    interests: str = Field(min_length=2, max_length=500)
    travel_style: str = "balanced"

    @field_validator("end_date")
    @classmethod
    def validate_end_date(cls, value, info):
        start = info.data.get("start_date")
        if start and value < start:
            raise ValueError("End date cannot be before start date.")
        return value
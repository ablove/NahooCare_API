from pydantic import BaseModel, Field
from datetime import datetime


class HealthProfileCreate(BaseModel):
    profile_id: str = Field(..., example="2001")
    user_id: str = Field(..., example="1001")
    blood_type: str = Field(..., example="B+")
    allergies: str = Field(..., example="Peanuts, Dust")
    chronic_conditions: str = Field(..., example="Diabetes, Hypertension")
    medical_history: str = Field(..., example="Previous surgery, Asthma")


class HealthProfileUpdate(BaseModel):
    blood_type: str = Field(None, example="A-")
    allergies: str = Field(None, example="None")
    chronic_conditions: str = Field(None, example="Hypertension")
    medical_history: str = Field(None, example="Updated medical history")


class HealthProfileResponse(BaseModel):
    profile_id: str
    user_id: str
    blood_type: str
    allergies: str
    chronic_conditions: str
    medical_history: str
    last_update: datetime
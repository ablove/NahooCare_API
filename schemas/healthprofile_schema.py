from typing import List
from pydantic import BaseModel, Field
from datetime import datetime


class HealthProfileCreate(BaseModel):
    blood_type: str = Field(..., example="B+")
    allergies: List[str] = Field(..., example=["Peanuts", "Dust"])
    chronic_conditions: List[str] = Field(..., example=["Diabetes","Hypertension"])
    medical_history:  List[str] = Field(..., example=["Previous surgery", "Asthma"])


class HealthProfileUpdate(BaseModel):
    blood_type: str = Field(None, example="A-")
    allergies: List[str] = Field(..., example=["Peanuts", "Dust"])
    chronic_conditions: List[str] = Field(..., example=["Diabetes","Hypertension"])
    medical_history:  List[str] = Field(..., example=["Previous surgery", "Asthma"])


class HealthProfileResponse(BaseModel):
    profile_id: str
    blood_type: str
    allergies:List[str]
    chronic_conditions: List[str]
    medical_history: List[str]
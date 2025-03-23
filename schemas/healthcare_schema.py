from pydantic import BaseModel, Field
from typing import List


class HealthcareCenterCreate(BaseModel):
    center_id: str = Field(..., example="3001")
    name: str = Field(..., example="Yekatit 12 General Hospital")
    address: str = Field(..., example="Sdsst Kilo, Addis Ababa")
    latitude: float = Field(..., example=9.0456)
    longitude: float = Field(..., example=38.7612)
    specialists: List[str] = Field(..., example=["Cardiology", "Neurology"])
    contact_number: str = Field(..., example="+251111234567")


class HealthcareSearch(BaseModel):
    specialty: str = Field(..., example="Cardiology")
    latitude: float = Field(..., example=9.0456)
    longitude: float = Field(..., example=38.7612)
    max_distance_km: int = Field(default=10, example=10)
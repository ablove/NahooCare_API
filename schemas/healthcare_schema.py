from pydantic import BaseModel, Field
from typing import Dict, List, Optional


class HealthcareCenterCreate(BaseModel):
    name: str = Field(..., example="Yekatit 12 General Hospital")
    address: str = Field(..., example="Sdsst Kilo, Addis Ababa")
    latitude: float = Field(..., example=9.0456)
    longitude: float = Field(..., example=38.7612)
    specialists: List[str] = Field(..., example=["Cardiology", "Neurology"])
    contact_info: Optional[Dict[str, str]] = Field(..., example= {
    "Reception": "+251-11-123-4567",
    "Emergency": "+251-91-234-5678"})
    available_time : List[str] = Field(..., example=["it works every day 8:00 am - 10:pm "])

class HealthcareSearch(BaseModel):
    specialty: str = Field(..., example="Cardiology")
    latitude: float = Field(..., example=9.0456)
    longitude: float = Field(..., example=38.7612)
    max_distance_km: int = Field(default=10, example=10)
class HealthcareCenterUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Updated Hospital Name")
    address: Optional[str] = Field(None, example="New Address, Addis Ababa")
    latitude: Optional[float] = Field(None, example=9.0556)
    longitude: Optional[float] = Field(None, example=38.7623)
    specialists: Optional[List[str]] = Field(None, example=["Pediatrics", "Cardiology"])
    contact_info: Optional[Dict[str, str]] = Field(None, example= {
    "Reception": "+251-11-123-4567",
    "Emergency": "+251-91-234-5678"})
    available_time : Optional[List[str]] = Field(..., example=["it works every day 8:00 am - 10:pm "])
class HelathcareCenterRespons(BaseModel):
    center_id:str =  Field(..., example="center_id_Yekatit")
    name: str = Field(..., example="Yekatit 12 General Hospital")
    address: str = Field(..., example="Sdsst Kilo, Addis Ababa")
    latitude: float = Field(..., example=9.0456)
    longitude: float = Field(..., example=38.7612)
    specialists: List[str] = Field(..., example=["Cardiology", "Neurology"])
    contact_info: Dict[str, str]= Field(None, example= {
    "Reception": "+251-11-123-4567",
    "Emergency": "+251-91-234-5678"})
    available_time : List[str] = Field(..., example=["it works every day 8:00 am - 10:pm "])
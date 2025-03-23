from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List
class PyObjectId(str):
    """Custom validator for MongoDB ObjectId"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)  # Store as string for compatibility


class HealthcareCenter(BaseModel):
    id: PyObjectId = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    center_id: str 
    name: str
    address: str 
    latitude: float 
    longitude: float
    specialists: List[str] 
    contact_number: str 
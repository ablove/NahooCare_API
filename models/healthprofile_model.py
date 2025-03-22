from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime
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


class HealthProfile(BaseModel):
    id: PyObjectId = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    profile_id: str
    user_id: int 
    blood_type: str
    allergies: str
    chronic_conditions: str
    medical_history: str 
    last_update: datetime = Field(default_factory=datetime.utcnow)  # Auto timestamp
from typing import List
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
    user_id: str
    blood_type: str
    allergies: List[str]
    chronic_conditions: List[str]
    medical_history: List[str]
    last_update: datetime = Field(default_factory=datetime.utcnow)  

    class Config:
        json_encoders = {ObjectId: str}  # Ensure ObjectId is serialized as a string
        arbitrary_types_allowed = True  # Allows ObjectId if needed
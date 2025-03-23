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



class Rating(BaseModel):
    id: PyObjectId = Field(default_factory=lambda: str(ObjectId()), alias="_id")  # MongoDB ID
    rating_id: str
    user_id: str
    center_id: str
    rating_value: int 
    comment: str
    rated_at: datetime = Field(default_factory=datetime.utcnow)  # Timestamp
    class Config:
        json_encoders = {ObjectId: str}  # Ensure ObjectId is serialized as a string
        arbitrary_types_allowed = True  # Allows ObjectId if needed
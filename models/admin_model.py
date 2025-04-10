from pydantic import BaseModel, Field
from bson import ObjectId

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

class Admin(BaseModel):
    id:  PyObjectId = Field(default_factory=lambda: str(ObjectId()), alias="_id") # MongoDB ID
    admin_id: str 
    full_name: str
    email: str
    password: str
    #role: str = Field(default="admin", example="admin")  # Fixed role
    class Config:
        json_encoders = {ObjectId: str}  # Ensure ObjectId is serialized as a string
        arbitrary_types_allowed = True  # Allows ObjectId if needed
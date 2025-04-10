from pydantic import BaseModel, Field
from typing import Dict, List
from bson import ObjectId

class PyObjectId(str):
    """Custom validator for MongoDB ObjectId."""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """Validates MongoDB ObjectId."""
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)  

class SyptomAnalysis(BaseModel):
    id: PyObjectId = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    analysis_id: str
    user_id: str
    symptoms: List[str]
    potential_conditions: List[str] 
    first_aid : Dict[str, str]
    healthCare_center_specialty: List[str] 
    analyzed_at: str 
    
    class Config:
        json_encoders = {ObjectId: str}  
        arbitrary_types_allowed = True  
from pydantic import BaseModel, Field
from typing import Dict
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
        return str(v)  # Store ObjectId as string for compatibility

class SavedSearch(BaseModel):
    id: PyObjectId = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    """
    Unique identifier for the saved search. Automatically generated as an ObjectId.
    """

    search_id: str = Field(..., example="7001")
    """
    Unique identifier for the saved search.
    """

    user_id: str = Field(..., example="1001")
    """
    The identifier linking the performed search to a specific user.
    """

    criteria: Dict[str, str] = Field(..., example={"type": "Dental Hospital", "category": "Private"})
    """
    The criteria used for the search, stored as a dictionary (e.g., type, category).
    """

    search_time: str = Field(..., example="2025-01-04T14:30:00Z")
    """
    The date and time when the search was last performed.
    """

    class Config:
        json_encoders = {ObjectId: str}  # Ensures ObjectId is serialized as a string
        arbitrary_types_allowed = True  # Allows ObjectId if needed for validation


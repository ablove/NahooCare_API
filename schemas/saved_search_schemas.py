from pydantic import BaseModel, Field
from typing import Dict


class SearchHistoryCreate(BaseModel):
    search_id: str = Field(..., example="7001")
    """
    Unique identifier for the search history.
    """

    user_id: str = Field(..., example="1001")
    """
    Identifier linking the search to a user.
    """

    criteria: Dict[str, str] = Field(..., example={"type": "Dental Hospital", "category": "Private"})
    """
    Search criteria as a dictionary.
    """

    search_time: str = Field(..., example="2025-01-04T14:30:00Z")
    """
    Date and time when the search was performed.
    """

class SearchHistoryResponse(SearchHistoryCreate):
    id: str = Field(..., example="507f191e810c19729de860ea")
    """
    The unique identifier returned after the search history is created or fetched.
    """

class SearchHistoryDeleteResponse(BaseModel):
    message: str = Field(..., example="Search history successfully deleted.")


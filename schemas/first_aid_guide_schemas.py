from pydantic import BaseModel, Field

class FirstAidGuideCreate(BaseModel):
    """
    Model for creating a new first aid guide.
    Includes required fields: guide ID, emergency type, instructions, and category.
    """
    guide_id: str = Field(..., example="6001")
    emergency_type: str = Field(..., example="Burns")
    instructions: str = Field(..., example="Cool burn with water, cover with clean cloth.")
    category: str = Field(..., example="Burn")

class FirstAidGuideUpdate(BaseModel):
    """
    Model for updating an existing first aid guide.
    Fields are optional for partial updates.
    """
    emergency_type: str = Field(None, example="Fractures")
    instructions: str = Field(None, example="Immobilize the fracture site and seek medical help.")
    category: str = Field(None, example="Fracture")

class FirstAidGuideResponse(BaseModel):
    """
    Response model for retrieving a first aid guide.
    Contains guide ID, emergency type, instructions, and category.
    """
    guide_id: str
    emergency_type: str
    instructions: str
    category: str

class FirstAidGuideDeleteResponse(BaseModel):
    """
    Response model for the deletion of a first aid guide.
    Contains guide ID and a success message.
    """
    guide_id: str = Field(..., example="6001")
    message: str = Field(..., example="First aid guide successfully deleted.")

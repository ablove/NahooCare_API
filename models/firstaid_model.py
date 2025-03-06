from pydantic import BaseModel
from bson import ObjectId

class FirstAid(BaseModel):
    guid_id: ObjectId
    emergency_type: str
    description: str
    instruction: str
    category:str
    updatedAt: str
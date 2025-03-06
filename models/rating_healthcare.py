from pydantic import BaseModel
from bson import ObjectId

class rating_healthcareCenter(BaseModel):
    rating_id : ObjectId
    user_id:ObjectId
    center_id:ObjectId
    rating_value:int
    comment : str
    rated_at:str

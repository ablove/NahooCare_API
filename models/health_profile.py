from pydantic import BaseModel
from bson import ObjectId

class health_profile(BaseModel):
    profile_id:ObjectId
    user_id : ObjectId
    blood_type:str
    allergies:str
    chronic_conditions:str
    medical_history:str
    last_update : str

from pydantic import BaseModel
from bson import ObjectId

class HealthcareCenter(BaseModel):
    center_id: ObjectId
    name: str
    address: str
    specialties: list
    rating: float
    latitude: str
    longitude : str
    contact_number: str
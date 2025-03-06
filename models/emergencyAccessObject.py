from pydantic import BaseModel
from bson  import ObjectId 

class emergency_access_object(BaseModel):
    emergencyAccess_id : ObjectId
    center_id : str
    emergency_type:str
    first_aid:str
    timestamp : str
    
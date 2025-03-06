from pydantic import BaseModel
from bson import ObjectId

class Admin(BaseModel):
    id: ObjectId
    username: str
    password: str
    
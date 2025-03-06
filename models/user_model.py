from pydantic import BaseModel
from bson import ObjectId

class user(BaseModel):
    user_id:ObjectId
    full_name:str
    location:str
    password:str
    gender : str
    secret_question: list
    age : int 

    

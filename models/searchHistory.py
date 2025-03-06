from pydantic import BaseModel
from bson import ObjectId
class search_history(BaseModel):
    search_id : ObjectId
    user_id:ObjectId
    criteria:set
    search_times:str
    
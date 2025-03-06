from pydantic import BaseModel
from bson import ObjectId

class symptom_analysis(BaseModel):
    analysis_id:ObjectId
    user_id :ObjectId
    symptoms:str
    potential_conditions:str
    Recommended_action : str
    analyzed_at : str
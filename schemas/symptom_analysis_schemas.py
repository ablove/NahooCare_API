from pydantic import BaseModel,Field
from datetime import datetime
from typing import Dict, List, Optional

class SymptomAnalysisRequest(BaseModel):
    user_id: str = Field(..., examples=["1001"])  # ✅ Correct
    symptoms: str= Field(..., examples=["Fever,Cough,Fatigue"]) 
    

class SymptomAnalysisResponse(BaseModel):
    analysis_id: str = Field(..., examples=["4001"])
    user_id: str = Field(..., examples=["1001"])
    symptoms:  List[str] = Field(..., examples=[["Fever", "Cough", "Fatigue"]])
    first_aid :Dict[str, str] = Field(...,examples=[["drink cold water" , "rub your chest"]])
    potential_conditions: list[str] = Field(..., examples=[["COVID-19", "Influenza"]])
    recommended_action: list[str] = Field(..., examples=[["General", "Internal Medicine"]])
    analyzed_at: str


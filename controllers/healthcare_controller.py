from fastapi import APIRouter, HTTPException, Depends
from schemas.healthcare_schema import HealthcareCenterCreate, HealthcareCenterUpdate, HealthcareSearch
from services.healthcare_service import create_healthcare_center, delete_healthcare_center, search_engin_health_care_center, search_healthcare_centers, update_healthcare_center
from middleware.auth import get_current_user

router = APIRouter()

@router.post("/create")
async def create(center: HealthcareCenterCreate):#current_user: dict = Depends(get_current_user)):
    result = await create_healthcare_center(center)
    return {"message": "Healthcare center created successfully", "id": result}

@router.post("/search")
async def search(search_data: HealthcareSearch):#current_user: dict = Depends(get_current_user)):
    return await search_healthcare_centers(search_data)
@router.put("/healthcare/{center_id}")
async def update_center(center_id: str, update_data: HealthcareCenterUpdate, current_user: dict = Depends(get_current_user)):
    return await update_healthcare_center(center_id, update_data)

@router.delete("/healthcare/{center_id}")
async def delete_center(center_id: str, current_user: dict = Depends(get_current_user)):
    return await delete_healthcare_center(center_id)
@router.post("search/specification/")
async def searchEngin(search_data: HealthcareSearch):
    return await search_engin_health_care_center(search_data)
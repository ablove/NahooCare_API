from fastapi import APIRouter, HTTPException, Depends
from schemas.healthcare_schema import HealthcareCenterCreate, HealthcareSearch
from services.healthcare_service import create_healthcare_center, search_healthcare_centers
from middleware.auth import get_current_user

router = APIRouter()


@router.post("/create")
async def create(center: HealthcareCenterCreate, current_user: dict = Depends(get_current_user)):
    result = await create_healthcare_center(center)
    return {"message": "Healthcare center created successfully", "id": result}


@router.post("/search")
async def search(search_data: HealthcareSearch, current_user: dict = Depends(get_current_user)):
    return await search_healthcare_centers(search_data)
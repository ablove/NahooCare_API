from fastapi import APIRouter, HTTPException, Depends
from schemas.healthprofile_schema import HealthProfileCreate, HealthProfileUpdate
from services.healthprofile_service import create_health_profile, get_health_profile, update_health_profile, delete_health_profile
from middleware.auth import get_current_user

router = APIRouter()


@router.post("/create")
async def create(profile: HealthProfileCreate):
    result = await create_health_profile(profile)
    if result:
        return {"message": "Health profile created successfully", "id": result}
    raise HTTPException(status_code=400, detail="Failed to create health profile")


@router.get("/{profile_id}")
async def get_profile(profile_id: str):
    profile = await get_health_profile(profile_id)
    if profile:
        return profile
    raise HTTPException(status_code=404, detail="Health profile not found")


@router.put("/{profile_id}")
async def update_profile(profile_id: str, update_data: HealthProfileUpdate):
    updated = await update_health_profile(profile_id, update_data)
    return updated


@router.delete("/{profile_id}")
async def delete_profile(profile_id: str):
    deleted = await delete_health_profile(profile_id)
    return deleted
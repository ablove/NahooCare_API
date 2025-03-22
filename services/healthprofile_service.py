from fastapi import HTTPException
from db.mongodb import database
from models.healthprofile_model import HealthProfile
from schemas.healthprofile_schema import HealthProfileCreate, HealthProfileUpdate
from bson import ObjectId
from datetime import datetime
import logging

collection = database["health_profiles"]


async def create_health_profile(profile: HealthProfileCreate):
    try:
        existing_profile = await collection.find_one({"profile_id": profile.profile_id})
        if existing_profile:
            raise HTTPException(status_code=400, detail="Profile ID already exists")

        profile_data = profile.dict()
        profile_data["last_update"] = datetime.utcnow()

        result = await collection.insert_one(profile_data)
        return str(result.inserted_id)

    except Exception as e:
        logging.error(f"Error creating health profile: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def get_health_profile(profile_id: str):
    try:
        profile = await collection.find_one({"profile_id": profile_id})
        if not profile:
            raise HTTPException(status_code=404, detail="Health profile not found")

        profile["_id"] = str(profile["_id"])
        return profile

    except Exception as e:
        logging.error(f"Error retrieving health profile: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def update_health_profile(profile_id: str, update_data: HealthProfileUpdate):
    try:
        if not update_data.dict(exclude_unset=True):
            raise HTTPException(status_code=400, detail="No update data provided")

        update_data_dict = update_data.dict(exclude_unset=True)
        update_data_dict["last_update"] = datetime.utcnow()

        result = await collection.update_one({"profile_id": profile_id}, {"$set": update_data_dict})
        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="No changes were made")

        return {"message": "Health profile updated successfully"}

    except Exception as e:
        logging.error(f"Error updating health profile: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def delete_health_profile(profile_id: str):
    try:
        result = await collection.delete_one({"profile_id": profile_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Health profile not found")

        return {"message": "Health profile deleted successfully"}

    except Exception as e:
        logging.error(f"Error deleting health profile: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
from fastapi import HTTPException
from db.mongodb import database
from models.healthcare_model import HealthcareCenter
from schemas.healthcare_schema import HealthcareCenterCreate, HealthcareSearch ,HealthcareCenterUpdate
from bson import ObjectId
from pymongo import GEOSPHERE
import logging

collection = database["healthcare_centers"]

#Ensure geospatial indexing for location-based search
collection.create_index([("location", GEOSPHERE)])

async def create_healthcare_center(center: HealthcareCenterCreate):

    
    try:
        existing_center = await collection.find_one({"center_id": center.center_id})
        if existing_center:
            raise HTTPException(status_code=400, detail="Healthcare center ID already exists")

        center_data = center.dict()
        center_data["location"] = {"type": "Point", "coordinates": [center.longitude, center.latitude]}  # Geospatial field

        result = await collection.insert_one(center_data)
        if not result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to create healthcare center")

        return str(result.inserted_id)

    except Exception as e:
        logging.error(f"Error creating healthcare center: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def search_healthcare_centers(search_data: HealthcareSearch):
    """
    Search for healthcare centers based on specialty and location.

    Args:
        search_data (HealthcareSearch): Search criteria including specialty, latitude, longitude, and max distance.

    Returns:
        List of healthcare centers matching the criteria.

    Raises:
        HTTPException: If no centers are found or an error occurs.
    """
    try:
        query = {
            "specialists": search_data.specialty,
            "location": {
                "$near": {
                    "$geometry": {"type": "Point", "coordinates": [search_data.longitude, search_data.latitude]},
                    "$maxDistance": search_data.max_distance_km * 1000  # Convert km to meters
                }
            }
        }
        centers = await collection.find(query).to_list(10)  # Limit results to 10

        if not centers:
            raise HTTPException(status_code=404, detail="No matching healthcare centers found")

        return centers

    except Exception as e:
        logging.error(f"Error searching healthcare centers: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
async def update_healthcare_center(center_id: str, update_data: HealthcareCenterUpdate):
    try:
        update_data_dict = update_data.dict(exclude_unset=True)
        if not update_data_dict:
            raise HTTPException(status_code=400, detail="No update data provided")

        result = await collection.update_one({"center_id": center_id}, {"$set": update_data_dict})
        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="No changes were made")

        return {"message": "Healthcare center updated successfully"}

    except Exception as e:
        logging.error(f"Error updating healthcare center: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
async def delete_healthcare_center(center_id: str):
    try:
        result = await collection.delete_one({"center_id": center_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Healthcare center not found")

        return {"message": "Healthcare center deleted successfully"}

    except Exception as e:
        logging.error(f"Error deleting healthcare center: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

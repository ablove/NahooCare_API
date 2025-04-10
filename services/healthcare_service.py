import uuid
from fastapi import HTTPException
from db.mongodb import database
from models.healthcare_model import HealthcareCenter
from schemas.healthcare_schema import HealthcareCenterCreate, HealthcareSearch ,HealthcareCenterUpdate, HelathcareCenterRespons
from bson import ObjectId
from pymongo import GEOSPHERE
import logging

from schemas.saved_search_schemas import SavedSearchCreate
from services.saved_search_service import create_search_record

collection = database["healthcare_centers"]

#Ensure geospatial indexing for location-based search
collection.create_index([("location", GEOSPHERE)])

async def create_healthcare_center(center: HealthcareCenterCreate):
    try:
        existing_center = await collection.find_one({"name": center.name})
        if existing_center:
            raise HTTPException(status_code=400, detail="Healthcare name already exists")

        center_data = center.dict()
        
        center_data["location"] = {"type": "Point", "coordinates": [center.longitude, center.latitude]} 
        # Geospatial field
        center_data["center_id"] = "center_id_" + center.name
        result = await collection.insert_one(center_data)
        if not result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to create healthcare center")

        return True 

    except Exception as e:
        logging.error(f"Error creating healthcare center: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def search_healthcare_centers(user_id:str , search_data: HealthcareSearch):
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
        search_record = SavedSearchCreate(
            user_id= user_id,
            search_id=str(uuid.uuid4()),
            search_parameters=search_data.model_dump(),
            results_count=len(centers)
        )
        await create_search_record(search_record)
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
async def search_engin_health_care_center(user_id:str,search_data: HealthcareSearch):
    try:
        query = {}  


        if search_data.name:
            query["name"] = {"$regex": search_data.name, "$options": "i"}  # Case-insensitive


        if search_data.specialty:
            query["specialists"] = search_data.specialty  # Matches exact specialty


        if search_data.latitude and search_data.longitude:
            query["location"] = {
                "$near": {
                    "$geometry": {"type": "Point", "coordinates": [search_data.longitude, search_data.latitude]},
                    "$maxDistance": search_data.max_distance_km * 1000  # Convert km to meters
                }
            }


        skip = (search_data.page - 1) * search_data.page_size
        centers = await collection.find(query).skip(skip).limit(search_data.page_size).to_list(None)

        if not centers:
            raise HTTPException(status_code=404, detail="No matching healthcare centers found")
        
        search_record = SavedSearchCreate(
            user_id= user_id,
            search_id=str(uuid.uuid4()),
            search_parameters=search_data.model_dump(),
            results_count=len(centers)
        )
        await create_search_record(search_record)
        return centers

    except Exception as e:
        logging.error(f"Error searching healthcare centers: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
async def get_healthcareCenter(name: str):
    try:
        existing_center = await collection.find_one({"name": name})
        
        if not existing_center: 
            raise HTTPException(status_code=404, detail="Healthcare Center not found")
            
        if "_id" in existing_center:
            existing_center['_id'] = str(existing_center['_id'])
            
        return HelathcareCenterRespons(
            center_id=existing_center["center_id"],
            name=existing_center["name"],
            address=existing_center["address"],
            latitude=existing_center["latitude"],
            longitude=existing_center["longitude"],
            specialists=existing_center["specialists"],
            contact_info=existing_center["contact_info"],
            available_time=existing_center["available_time"]
        )
    except Exception as e:
        logging.error(f"Error getting healthcare center: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


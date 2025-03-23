from fastapi import HTTPException
from db.mongodb import database
from schemas.rating_schema import RatingCreate , RatingUpdate
from datetime import datetime
import logging

collection = database["ratings"]
healthcare_collection = database["healthcare_centers"]

# Submit a Rating
async def submit_rating(rating: RatingCreate):
    try:
        existing_rating = await collection.find_one({"user_id": rating.user_id, "center_id": rating.center_id})
        if existing_rating:
            raise HTTPException(status_code=400, detail="User has already rated this healthcare center")

        rating_data = rating.dict()
        rating_data["rated_at"] = datetime.utcnow()

        result = await collection.insert_one(rating_data)
        if not result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to submit rating")

        #  Update Average Rating in Healthcare Center
        await update_healthcare_rating(rating.center_id)

        return str(result.inserted_id)

    except Exception as e:
        logging.error(f"Error submitting rating: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Get Ratings for a Healthcare Center
async def get_ratings(center_id: str):
    try:
        ratings = await collection.find({"center_id": center_id}).to_list(10)  # Limit results to 10
        if not ratings:
            raise HTTPException(status_code=404, detail="No ratings found for this center")

        return ratings

    except Exception as e:
        logging.error(f"Error retrieving ratings: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Calculate & Update Healthcare Center Rating
async def update_healthcare_rating(center_id: str):
    try:
        ratings = await collection.find({"center_id": center_id}).to_list(None)  # Fetch all ratings
        if not ratings:
            return  # No ratings exist for this center

        avg_rating = sum(r["rating_value"] for r in ratings) / len(ratings)

        await healthcare_collection.update_one(
            {"center_id": center_id},
            {"$set": {"average_rating": round(avg_rating, 1)}}
        )

    except Exception as e:
        logging.error(f"Error updating healthcare rating: {e}")
        raise HTTPException(status_code=500, detail="Failed to update healthcare center rating")
    
# Update an Existing Rating
async def update_rating(user_id: str, center_id: str, update_data: RatingUpdate):
    try:
        existing_rating = await collection.find_one({"user_id": user_id, "center_id": center_id})
        if not existing_rating:
            raise HTTPException(status_code=404, detail="Rating not found for this user and center")

        update_data_dict = update_data.dict(exclude_unset=True)
        update_data_dict["rated_at"] = datetime.utcnow()

        result = await collection.update_one(
            {"user_id": user_id, "center_id": center_id},
            {"$set": update_data_dict}
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="No changes were made")

        #  Recalculate the center’s average rating after update
        await update_healthcare_rating(center_id)

        return {"message": "Rating updated successfully"}

    except Exception as e:
        logging.error(f"Error updating rating: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
async def remove_inappropriate_review(rating_id: str):
    try:
        result = await collection.delete_one({"rating_id": rating_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Review not found")

        return {"message": "Inappropriate review removed successfully"}

    except Exception as e:
        logging.error(f"Error removing review: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
async def recalculate_healthcare_rating(center_id: str):
    try:
        ratings = await collection.find({"center_id": center_id}).to_list(None)  # Fetch all ratings
        if not ratings:
            await healthcare_collection.update_one({"center_id": center_id}, {"$set": {"average_rating": 0}})
            return {"message": "No ratings found, rating reset to 0"}

        avg_rating = sum(r["rating_value"] for r in ratings) / len(ratings)

        await healthcare_collection.update_one(
            {"center_id": center_id},
            {"$set": {"average_rating": round(avg_rating, 1)}}
        )

        return {"message": "Healthcare center rating updated"}

    except Exception as e:
        logging.error(f"Error updating rating: {e}")
        raise HTTPException(status_code=500, detail="Failed to update healthcare center rating")
from fastapi import APIRouter, HTTPException
from schemas.saved_search_schemas import SavedSearchCreate,SavedSearchResponse
from services.saved_search_service import create_search_record,get_user_search_history, delete_search_history

router = APIRouter()

# Add a New Search History
@router.post("/add-history")
async def add_history(search:  SavedSearchCreate):
    """
    Endpoint to add a new search history.
    """
    result = await create_search_record(search)
    if result:
        return {"message": "Search history added successfully", "id": result}
    raise HTTPException(status_code=400, detail="Failed to add search history")

# Get All Search Histories
@router.get("/history/{user_id}")
async def get_history(user_id: str):
    """
    Endpoint to retrieve all search histories for a specified user.
    """
    histories = await get_user_search_history(user_id)
    if histories:
        return histories
    raise HTTPException(status_code=404, detail="No search history found")

# Delete by Search ID
@router.delete("/delete-history/{search_id}")
async def delete_history_by_search_id(search_id: str):
    """
    Endpoint to delete a specific search history by its search ID.
    """
    deleted_count = await delete_search_history(search_id=search_id)
    if deleted_count:
        return {"message": f"{deleted_count} search history deleted successfully"}
    raise HTTPException(status_code=404, detail="Search history not found")


# Delete by User ID
@router.delete("/delete-history-by-user/{user_id}")
async def delete_history_by_user_id(user_id: str):
    """
    Endpoint to delete all search histories for a specific user ID.
    """
    deleted_count = await delete_search_history(user_id=user_id)
    if deleted_count:
        return {"message": f"{deleted_count} search histories deleted successfully for user {user_id}"}
    raise HTTPException(status_code=404, detail="No search history found for the user")



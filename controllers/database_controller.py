from fastapi import APIRouter
from db.mongodb import check_database_connection

router = APIRouter()

@router.get("/check-db")
async def check_db():
    is_connected = await check_database_connection()
    if is_connected:
        return {"message": "MongoDB Atlas is connected successfully!"}
    return {"error": "Failed to connect to MongoDB Atlas"}
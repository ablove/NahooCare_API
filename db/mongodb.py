from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings

# Connect to MongoDB Atlas
client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
database = client[settings.MONGO_DB_NAME]

async def check_database_connection():
    try:
        await client.admin.command("ping")  # Sends a ping to MongoDB
        return True
    except Exception as e:
        print(f"Database connection error: {e}")
        return False
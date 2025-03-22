from db.mongodb import database
from models.account_model import Account
from schemas.account_schemas import AccountCreate, LoginSchema, PasswordResetSchema
from core.security import hash_password, verify_password, create_access_token
from bson import ObjectId
from datetime import timedelta
from core.config import settings

collection = database["accounts"]

#  Register a New Account
async def create_account(account: AccountCreate):
    existing_user = await collection.find_one({"phone_number": account.phone_number})
    if existing_user:
        return None  # User already exists

    hashed_password = hash_password(account.password)
    hashed_secret_answer = hash_password(account.secret_answer)

    account_data = account.dict()
    account_data["hashed_password"] = hashed_password
    account_data["secret_answer"] = hashed_secret_answer

    del account_data["password"]  # Remove plain text password
    del account_data["secret_answer"]  # Remove plain text secret answer

    result = await collection.insert_one(account_data)
    return str(result.inserted_id)

#  Authenticate User for Login
async def authenticate_user(phone_number: str, password: str):
    user = await collection.find_one({"phone_number": phone_number})
    if user and verify_password(password, user["hashed_password"]):
        return user
    return None

# Get User Account by user_id
async def get_account(user_id: int):
    account = await collection.find_one({"user_id": user_id}, {"hashed_password": 0, "secret_answer": 0})
    if account:
        account["_id"] = str(account["_id"])
    return account

# Update User Account
async def update_account(user_id: int, update_data: dict):
    result = await collection.update_one({"user_id": user_id}, {"$set": update_data})
    return result.modified_count

# Delete User Account
async def delete_account(user_id: int):
    result = await collection.delete_one({"user_id": user_id})
    return result.deleted_count

# Reset Password using Secret Question
async def reset_password(data: PasswordResetSchema):
    user = await collection.find_one({"phone_number": data.phone_number})
    if user and verify_password(data.secret_answer, user["secret_answer"]):
        new_hashed_password = hash_password(data.new_password)
        await collection.update_one({"phone_number": data.phone_number}, {"$set": {"hashed_password": new_hashed_password}})
        return True
    return False
from fastapi import HTTPException
from db.mongodb import database
from models.account_model import Account
from schemas.account_schemas import AccountCreate, LoginSchema, PasswordResetSchema
from core.security import hash_password, verify_password, create_access_token
from bson import ObjectId
from datetime import timedelta
from core.config import settings
import logging

collection = database["accounts"]


async def create_account(account: AccountCreate):
    try:
        existing_user = await collection.find_one({"phone_number": account.phone_number})
        if existing_user:
            raise HTTPException(status_code=400, detail="Phone number already registered")

        hashed_password = hash_password(account.password)
        

        account_data = account.dict()
        account_data["hashed_password"] = hashed_password


        del account_data["password"]  # Remove plain text password

        result = await collection.insert_one(account_data)
        if not result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to create account")

        return str(result.inserted_id)

    except Exception as e:
        logging.error(f"Error creating account: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def authenticate_user(phone_number: str, password: str):
    try:
        user = await collection.find_one({"phone_number": phone_number})
        if not user:
            raise HTTPException(status_code=401, detail="Invalid phone number or password")

        if not verify_password(password, user["hashed_password"]):
            raise HTTPException(status_code=401, detail="Invalid phone number or password")

        return user

    except Exception as e:
        logging.error(f"Authentication error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def get_account(user_id: int):
    try:
        account = await collection.find_one({"user_id": user_id}, {"hashed_password": 0, "secret_answer": 0})
        if not account:
            raise HTTPException(status_code=404, detail="User not found")

        account["_id"] = str(account["_id"])
        return account

    except Exception as e:
        logging.error(f"Error retrieving user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def update_account(user_id: int, update_data: dict):
    try:
        if not update_data:
            raise HTTPException(status_code=400, detail="No update data provided")

        result = await collection.update_one({"user_id": user_id}, {"$set": update_data})
        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="No changes were made")

        return {"message": "Account updated successfully"}

    except Exception as e:
        logging.error(f"Error updating account: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def delete_account(user_id: int):
    try:
        result = await collection.delete_one({"user_id": user_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")

        return {"message": "Account deleted successfully"}

    except Exception as e:
        logging.error(f"Error deleting account: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def reset_password(data: PasswordResetSchema):
    try:
        user = await collection.find_one({"phone_number": data.phone_number})
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        print(user)
        if "secret_answer" not in user:
            raise HTTPException(status_code=400, detail="Secret answer not set for this account")

        if user["secret_answer"] != data.secret_answer:
            raise HTTPException(status_code=400, detail="Incorrect secret answer")

        new_hashed_password = hash_password(data.new_password)
        update_result = await collection.update_one(
            {"phone_number": data.phone_number},
            {"$set": {"hashed_password": new_hashed_password}}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=500, detail="Failed to reset password")

        return {"message": "Password reset successfully"}

    except Exception as e:
        logging.error(f"Error resetting password: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
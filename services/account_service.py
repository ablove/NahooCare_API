from fastapi import HTTPException
import uuid
from db.mongodb import database
from models.account_model import Account
from schemas.account_schemas import AccountCreate, AccountResponse,   PasswordResetSchema
from core.security import hash_password, verify_password, create_access_token
from datetime import datetime

import logging
import uuid
collection = database["accounts"]

async def create_account(account: AccountCreate):
    try:
        existing_user = await collection.find_one({"phone_number": account.phone_number}) #phone nmber 
        if existing_user:
            raise HTTPException(status_code=400, detail="Phone number already registered")
        hashed_password = hash_password(account.password)
        del account.password
        account_data = account.dict()
        account_data["hashed_password"] = hashed_password
        account_data["user_id"] = ('user_id_'+str(account_data["phone_number"]))
        account_data["created_at"] = str(datetime.utcnow().isoformat())
        result = await collection.insert_one(account_data)
        if not result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to create account")
        return True
    except Exception as e:
        logging.error(f"Error creating account: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def authenticate_user(phone_number: str, password: str):
    try:
        user = await collection.find_one({"phone_number": phone_number})
        if not user:
            raise HTTPException(status_code=401, detail="Invalid phone number ")

        if not verify_password(password, user["hashed_password"]):
            raise HTTPException(status_code=401, detail="Incorrect password")
        return user

    except Exception as e:
        logging.error(f"Authentication error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def get_account(user_id: str):
    try:
        account = await collection.find_one({"user_id": user_id})
        if not account:
            raise HTTPException(status_code=404, detail="User not found")
        if "_id" in account:
            account["_id"] = str(account["_id"])
        return AccountResponse(full_name=account['full_name'],phone_number=account['phone_number'],gender=account['gender'],age = account['age'],secret_answer=account['secret_answer'],secret_question=account["secret_question"])
    except Exception as e:
        logging.error(f"Error retrieving user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def update_account(user_id: str, update_data: AccountResponse):
    try:
        # Convert Pydantic model to dictionary and exclude unset fields
        update_dict = update_data.dict(exclude_unset=True)
        
        # Update the account in MongoDB
        result = await collection.update_one(
            {"user_id": user_id},
            {"$set": update_dict}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="No changes made or user not found")
        
        # Optionally fetch and return the updated document
        updated_account = await collection.find_one({"user_id": user_id})
        if "_id" in updated_account:
            updated_account["_id"] = str(updated_account["_id"])
        
        return {
            "message": "Account updated successfully",
            "updated_account": updated_account
        }

    except Exception as e:
        logging.error(f"Error updating account: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def delete_account(user_id: str):
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
async def get_secrete_question(user_id:str):
    try:
        account = await collection.find_one({"user_id": user_id})
        if not account:
            raise HTTPException(status_code=404, detail="User not found")
        return account['secret_question']
    except Exception as e:
        logging.error(f"Error finding secret_question :{e}")
        raise HTTPException(status_code=500 , detail="Internal server error")
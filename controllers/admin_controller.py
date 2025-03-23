from fastapi import APIRouter, HTTPException, Depends
from schemas.admin_schema import AdminCreate, AdminUpdate, AdminLogin
from services.admin_service import create_admin, login_admin, update_admin
from services.backup_service import backup_database, restore_database
from middleware.auth import get_current_user

router = APIRouter()


@router.post("/register")
async def register(admin: AdminCreate):
    result = await create_admin(admin)
    return {"message": "Admin registered successfully", "id": result}


@router.post("/login")
async def login(admin: AdminLogin):
    return await login_admin(admin)


@router.put("/{admin_id}")
async def update(admin_id: str, update_data: AdminUpdate):# current_user: dict = Depends(get_current_user)):
    return await update_admin(admin_id, update_data)


@router.post("/backup")
async def backup(current_user: dict = Depends(get_current_user)):
    return backup_database()


@router.post("/restore")
async def restore(backup_file: str):# current_user: dict = Depends(get_current_user)):
    return restore_database(backup_file)
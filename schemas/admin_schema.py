from pydantic import BaseModel, Field


class AdminCreate(BaseModel):
    admin_id: str = Field(..., example="A1001")
    full_name: str = Field(..., example="John Doe")
    email: str = Field(..., example="admin@healthcare.com")
    password: str = Field(..., example="securepassword")


class AdminLogin(BaseModel):
    email: str = Field(..., example="admin@healthcare.com")
    password: str = Field(..., example="securepassword")


class AdminUpdate(BaseModel):
    full_name: str = Field(None, example="Updated Name")
    email: str = Field(None, example="newadmin@healthcare.com")
    password: str = Field(None, example="newsecurepassword")
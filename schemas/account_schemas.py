from pydantic import BaseModel, Field

class AccountCreate(BaseModel):
    user_id: int = Field(..., example=1001)
    full_name: str = Field(..., example="KEBEDE ALEMU Dagne")
    phone_number: str = Field(..., example="+251912345678")
    location: str = Field(..., example="www.google.map/xx")
    password: str = Field(..., example="secure_password")
    gender: str = Field(..., example="Male")
    secret_question: str = Field(..., example="What is my favorite food?")
    secret_answer: str = Field(..., example="Shiro")  # Store answer
    age: int = Field(..., example=44)

class LoginSchema(BaseModel):
    phone_number: str
    password: str
class PasswordResetSchema(BaseModel):
    phone_number: str
    secret_answer: str
    new_password: str
class AccountResponse(BaseModel):
    user_id: int
    full_name: str
    phone_number: str
    location: str
    gender: str
    age: int
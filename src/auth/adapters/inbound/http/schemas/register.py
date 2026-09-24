from pydantic import BaseModel, EmailStr, Field


class RegisterUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str = Field(min_length=2, max_length=150)
from pydantic import BaseModel, EmailStr


class LoginUserRequest(BaseModel):
    email: EmailStr
    password: str
from pydantic import BaseModel, EmailStr, field_validator
from typing import Annotated

class UserLogin(BaseModel):
    email: EmailStr 
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password needs at least one number")
        return v
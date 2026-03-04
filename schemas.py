from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Optional

class RetailerCreate(BaseModel):
    business_name: str = Field(..., min_length=2)
    admin_email: EmailStr
    admin_password: str

class UserLogin(BaseModel):
    email: EmailStr 
    password: str
    # this ensures we know WHICH store the login/signup is for
    retailer_id: Optional[int] = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password needs at least one number")
        return v
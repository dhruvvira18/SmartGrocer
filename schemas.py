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

class RatingUpdate(BaseModel):
    rating: int = Field(..., ge=1, le=5)

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1)
    price: int = Field(..., ge=0)
    category: str = Field(..., min_length=1)
    stock: int = Field(..., ge=0)
    image_url: str = ""

class ProductDealUpdate(BaseModel):
    is_daily_deal: bool
    discount_percentage: int = Field(..., ge=0, le=100)

class OrderCartItem(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderCreate(BaseModel):
    amount: float
    cart: list[OrderCartItem] = []

class PaymentSuccessPayload(BaseModel):
    cart: list[OrderCartItem]

class FeedbackCreate(BaseModel):
    message: str = Field(..., min_length=1)
    email: Optional[EmailStr] = None

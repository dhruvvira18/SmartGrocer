from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass, DeclarativeBase, relationship
from typing import List

class Base(MappedAsDataclass, DeclarativeBase):
    pass

class Retailer(Base):
    __tablename__ = "retailers"
    id: Mapped[int] = mapped_column(primary_key=True, init=False, autoincrement=True)
    business_name: Mapped[str] = mapped_column(String(100))
    slug: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    
    users: Mapped[List["User"]] = relationship(back_populates="retailer", init=False)
    products: Mapped[List["Product"]] = relationship(back_populates="retailer", init=False)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, init=False, autoincrement=True)
    retailer_id: Mapped[int] = mapped_column(ForeignKey("retailers.id"))
    email: Mapped[str] = mapped_column(String(100), index=True)
    password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(100), default="New User")
    role: Mapped[str] = mapped_column(String(20), default="shopper") # admin, shopper

    retailer: Mapped["Retailer"] = relationship(back_populates="users", init=False)

    # Allows john@gmail.com to be a customer at multiple different stores
    __table_args__ = (UniqueConstraint('email', 'retailer_id', name='_user_email_retailer_uc'),)

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True, init=False, autoincrement=True)
    retailer_id: Mapped[int] = mapped_column(ForeignKey("retailers.id"))
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column()
    description: Mapped[str] = mapped_column(String(255), default="")
    image_url: Mapped[str] = mapped_column(String(255), default="")
    rating: Mapped[float] = mapped_column(default=4.5)
    review_count: Mapped[int] = mapped_column(default=0)
    stock: Mapped[int] = mapped_column(default=0)
    category: Mapped[str] = mapped_column(String(50), default="General")

    retailer: Mapped["Retailer"] = relationship(back_populates="products", init=False)
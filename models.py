from sqlalchemy import String, ForeignKey, UniqueConstraint, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass, DeclarativeBase, relationship
from datetime import datetime
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
    address: Mapped[str | None] = mapped_column(String(255), default=None, nullable=True)

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
    rating: Mapped[float] = mapped_column(default=0.0)
    review_count: Mapped[int] = mapped_column(default=0)
    stock: Mapped[int] = mapped_column(default=0)
    category: Mapped[str] = mapped_column(String(50), default="General")

    retailer: Mapped["Retailer"] = relationship(back_populates="products", init=False)

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True, init=False, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    retailer_id: Mapped[int] = mapped_column(ForeignKey("retailers.id"))
    total_amount: Mapped[float] = mapped_column()
    status: Mapped[str] = mapped_column(String(20), default="Pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    user: Mapped["User"] = relationship(init=False)
    retailer: Mapped["Retailer"] = relationship(init=False)
    items: Mapped[List["OrderItem"]] = relationship(back_populates="order", init=False)

class OrderItem(Base):
    __tablename__ = "order_items"
    id: Mapped[int] = mapped_column(primary_key=True, init=False, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column()
    price_at_purchase: Mapped[float] = mapped_column()

    order: Mapped["Order"] = relationship(back_populates="items", init=False)
    product: Mapped["Product"] = relationship(init=False)
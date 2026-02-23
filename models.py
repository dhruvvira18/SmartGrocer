from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass, DeclarativeBase

class Base(MappedAsDataclass, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    # 1. init=False: The Dataclass won't ask for an ID when you create a User object
    # 2. autoincrement=True: Tells MySQL to use AUTO_INCREMENT
    id: Mapped[int] = mapped_column(primary_key=True, init=False, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(100), default="New Shopper")
    role: Mapped[str] = mapped_column(String(20), default="shopper")

class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True, init=False, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column()
    stock: Mapped[int] = mapped_column(default=0)
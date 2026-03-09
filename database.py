from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, MappedAsDataclass

class Base(MappedAsDataclass, DeclarativeBase):
    pass

# XAMPP Connection
engine = create_engine("mysql+mysqlconnector://root@localhost:3306/smart_grocer")
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
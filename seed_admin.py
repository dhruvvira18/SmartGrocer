from database import SessionLocal, engine
from models import Base, Retailer, User

# Create all tables in the database
Base.metadata.create_all(bind=engine)

def seed_admin():
    db = SessionLocal()
    try:
        retailer = db.query(Retailer).filter_by(slug="mikes-groceries").first()
        if retailer:
            admin_user = db.query(User).filter_by(email="mike@smartgrocer.com", retailer_id=retailer.id).first()
            if not admin_user:
                admin_user = User(
                    email="mike@smartgrocer.com",
                    password="MikesGroceries1",
                    role="admin",
                    full_name="Mike",
                    retailer_id=retailer.id
                )
                db.add(admin_user)
                db.commit()
                print("Admin created!")
            else:
                print("Admin already exists")
    finally:
        db.close()

if __name__ == "__main__":
    seed_admin()

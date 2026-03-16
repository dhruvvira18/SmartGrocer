from database import SessionLocal, engine
from models import Base, Retailer, Product

# Create all tables in the database
Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    try:
        # Check if "Mike's Groceries" exists, else create it
        retailer = db.query(Retailer).filter_by(slug="mikes-groceries").first()
        if not retailer:
            retailer = Retailer(business_name="Mike's Groceries", slug="mikes-groceries")
            db.add(retailer)
            db.commit()
            db.refresh(retailer)
            print(f"Created new retailer: {retailer.business_name}")
        else:
            print(f"Found existing retailer: {retailer.business_name}")

        # Define 10 sample products
        sample_products = [
            Product(
                retailer_id=retailer.id,
                name="Fresh Apple",
                price=1.20,
                description="Crisp and sweet red apples.",
                category="Produce",
                image_url="https://img.icons8.com/color/96/apple.png",
                stock=150
            ),
            Product(
                retailer_id=retailer.id,
                name="Organic Milk",
                price=3.50,
                description="Whole organic milk, 1 gallon.",
                category="Dairy",
                image_url="https://img.icons8.com/color/96/milk.png",
                stock=40
            ),
            Product(
                retailer_id=retailer.id,
                name="Whole Wheat Bread",
                price=2.80,
                description="Freshly baked whole wheat bread.",
                category="Bakery",
                image_url="https://img.icons8.com/color/96/bread.png",
                stock=30
            ),
            Product(
                retailer_id=retailer.id,
                name="Free Range Eggs",
                price=4.20,
                description="Dozen free range brown eggs.",
                category="Dairy",
                image_url="https://img.icons8.com/color/96/eggs.png",
                stock=60
            ),
            Product(
                retailer_id=retailer.id,
                name="Bananas",
                price=0.50,
                description="Ripe yellow bananas per lb.",
                category="Produce",
                image_url="https://img.icons8.com/color/96/banana.png",
                stock=200
            ),
            Product(
                retailer_id=retailer.id,
                name="Cheddar Cheese",
                price=5.00,
                description="Sharp cheddar cheese block.",
                category="Dairy",
                image_url="https://img.icons8.com/color/96/cheese.png",
                stock=25
            ),
            Product(
                retailer_id=retailer.id,
                name="Orange Juice",
                price=4.50,
                description="100% natural orange juice.",
                category="Beverages",
                image_url="https://img.icons8.com/color/96/orange-juice.png",
                stock=50
            ),
            Product(
                retailer_id=retailer.id,
                name="Chicken Breast",
                price=8.50,
                description="Boneless skinless chicken breast.",
                category="Meat",
                image_url="https://img.icons8.com/color/96/thanksgiving.png",
                stock=40
            ),
            Product(
                retailer_id=retailer.id,
                name="Pasta",
                price=1.80,
                description="Italian spaghetti pasta.",
                category="Pantry",
                image_url="https://img.icons8.com/color/96/spaghetti.png",
                stock=100
            ),
            Product(
                retailer_id=retailer.id,
                name="Tomato Sauce",
                price=2.20,
                description="Classic marinara tomato sauce.",
                category="Pantry",
                image_url="https://img.icons8.com/color/96/tomato.png",
                stock=80
            )
        ]

        # Add all products to the session
        db.add_all(sample_products)
        db.commit()
        print(f"Successfully inserted {len(sample_products)} products for {retailer.business_name}.")

    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()

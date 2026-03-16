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
            # Delete existing products to re-seed cleanly
            db.query(Product).filter(Product.retailer_id == retailer.id).delete()
            db.commit()

        # Define vegetarian sample products based on user feedback
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
                name="Basmati Rice",
                price=6.50,
                description="Premium long-grain Basmati rice.",
                category="Grains",
                image_url="https://img.icons8.com/color/96/rice-bowl.png",
                stock=60
            ),
            Product(
                retailer_id=retailer.id,
                name="Lentils (Dal)",
                price=3.80,
                description="High-protein yellow lentils.",
                category="Pulses",
                image_url="https://img.icons8.com/color/96/vegetarian-food.png",
                stock=80
            ),
            Product(
                retailer_id=retailer.id,
                name="Olive Oil",
                price=9.20,
                description="Extra virgin cold-pressed olive oil.",
                category="Pantry",
                image_url="https://img.icons8.com/color/96/olive-oil.png",
                stock=40
            ),
            Product(
                retailer_id=retailer.id,
                name="Corn Flakes",
                price=4.50,
                description="Crispy corn flakes cereal.",
                category="Pantry",
                image_url="https://img.icons8.com/color/96/cereal.png",
                stock=55
            ),
            Product(
                retailer_id=retailer.id,
                name="Herbal Shampoo",
                price=5.00,
                description="Natural aloe vera extract shampoo.",
                category="Personal Care",
                image_url="https://img.icons8.com/color/96/shampoo.png",
                stock=25
            ),
            Product(
                retailer_id=retailer.id,
                name="Mint Toothpaste",
                price=3.50,
                description="Fluoride toothpaste with fresh mint.",
                category="Personal Care",
                image_url="https://img.icons8.com/color/96/toothpaste.png",
                stock=50
            ),
            Product(
                retailer_id=retailer.id,
                name="Lavender Soap",
                price=2.50,
                description="Soothing lavender scent bar soap.",
                category="Personal Care",
                image_url="https://img.icons8.com/color/96/soap.png",
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
                name="Organic Milk",
                price=3.50,
                description="Whole organic milk, 1 gallon.",
                category="Dairy",
                image_url="https://img.icons8.com/color/96/milk.png",
                stock=40
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

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

        # Define vegetarian sample products based on user feedback (all prices as integers in ₹)
        sample_products = [
            # Produce
            Product(retailer_id=retailer.id, name="Fresh Apple", price=120, description="Crisp and sweet red apples per kg.", category="Produce", image_url="https://img.icons8.com/color/96/apple.png", stock=150),
            Product(retailer_id=retailer.id, name="Bananas", price=50, description="Ripe yellow bananas per dozen.", category="Produce", image_url="https://img.icons8.com/color/96/banana.png", stock=200),
            Product(retailer_id=retailer.id, name="Mangoes", price=250, description="Sweet Alphonso mangoes per kg.", category="Produce", image_url="https://img.icons8.com/color/96/mango.png", stock=80),
            Product(retailer_id=retailer.id, name="Potatoes", price=30, description="Fresh potatoes per kg.", category="Produce", image_url="https://img.icons8.com/color/96/potato.png", stock=300),
            Product(retailer_id=retailer.id, name="Onions", price=40, description="Red onions per kg.", category="Produce", image_url="https://img.icons8.com/color/96/onion.png", stock=250),
            Product(retailer_id=retailer.id, name="Carrots", price=60, description="Fresh orange carrots per kg.", category="Produce", image_url="https://img.icons8.com/color/96/carrot.png", stock=100),
            Product(retailer_id=retailer.id, name="Broccoli", price=150, description="Fresh green broccoli per piece.", category="Produce", image_url="https://img.icons8.com/color/96/broccoli.png", stock=50),

            # Dairy
            Product(retailer_id=retailer.id, name="Organic Milk", price=80, description="Whole organic milk, 1 liter.", category="Dairy", image_url="https://img.icons8.com/color/96/milk.png", stock=100),
            Product(retailer_id=retailer.id, name="Paneer", price=120, description="Fresh cottage cheese, 200g.", category="Dairy", image_url="https://img.icons8.com/color/96/cheese.png", stock=60),
            Product(retailer_id=retailer.id, name="Butter", price=60, description="Salted table butter, 100g.", category="Dairy", image_url="https://img.icons8.com/color/96/butter.png", stock=80),
            Product(retailer_id=retailer.id, name="Yogurt (Curd)", price=40, description="Fresh plain yogurt, 400g.", category="Dairy", image_url="https://img.icons8.com/color/96/yogurt.png", stock=120),

            # Grains & Pulses
            Product(retailer_id=retailer.id, name="Basmati Rice", price=150, description="Premium long-grain Basmati rice per kg.", category="Grains", image_url="https://img.icons8.com/color/96/rice-bowl.png", stock=200),
            Product(retailer_id=retailer.id, name="Whole Wheat Flour", price=50, description="Atta for soft rotis per kg.", category="Grains", image_url="https://img.icons8.com/color/96/flour-in-paper-packaging.png", stock=300),
            Product(retailer_id=retailer.id, name="Toor Dal", price=130, description="Split pigeon peas per kg.", category="Pulses", image_url="https://img.icons8.com/color/96/vegetarian-food.png", stock=150),
            Product(retailer_id=retailer.id, name="Moong Dal", price=110, description="Yellow split lentils per kg.", category="Pulses", image_url="https://img.icons8.com/color/96/vegan-food.png", stock=140),
            Product(retailer_id=retailer.id, name="Chana Dal", price=90, description="Split bengal gram per kg.", category="Pulses", image_url="https://img.icons8.com/color/96/healthy-food.png", stock=160),

            # Pantry & Condiments
            Product(retailer_id=retailer.id, name="Olive Oil", price=850, description="Extra virgin olive oil, 500ml.", category="Pantry", image_url="https://img.icons8.com/color/96/olive-oil.png", stock=40),
            Product(retailer_id=retailer.id, name="Sunflower Oil", price=160, description="Refined sunflower oil, 1 liter.", category="Pantry", image_url="https://img.icons8.com/color/96/bottle-of-water.png", stock=120),
            Product(retailer_id=retailer.id, name="Corn Flakes", price=180, description="Crispy corn flakes cereal, 500g.", category="Pantry", image_url="https://img.icons8.com/color/96/cereal.png", stock=55),
            Product(retailer_id=retailer.id, name="Pasta", price=60, description="Italian spaghetti pasta, 500g.", category="Pantry", image_url="https://img.icons8.com/color/96/spaghetti.png", stock=100),
            Product(retailer_id=retailer.id, name="Tomato Sauce", price=110, description="Classic tomato ketchup, 500g.", category="Pantry", image_url="https://img.icons8.com/color/96/ketchup.png", stock=80),
            Product(retailer_id=retailer.id, name="Salt", price=25, description="Iodized table salt, 1kg.", category="Pantry", image_url="https://img.icons8.com/color/96/salt-shaker.png", stock=200),
            Product(retailer_id=retailer.id, name="Sugar", price=45, description="Refined white sugar, 1kg.", category="Pantry", image_url="https://img.icons8.com/color/96/sugar-cubes.png", stock=180),
            Product(retailer_id=retailer.id, name="Green Tea", price=220, description="Organic green tea bags, box of 25.", category="Beverages", image_url="https://img.icons8.com/color/96/tea.png", stock=60),
            Product(retailer_id=retailer.id, name="Filter Coffee", price=150, description="South Indian filter coffee powder, 250g.", category="Beverages", image_url="https://img.icons8.com/color/96/coffee-beans.png", stock=70),
            Product(retailer_id=retailer.id, name="Orange Juice", price=120, description="100% natural orange juice, 1 liter.", category="Beverages", image_url="https://img.icons8.com/color/96/orange-juice.png", stock=50),

            # Snacks
            Product(retailer_id=retailer.id, name="Potato Chips", price=40, description="Classic salted potato chips.", category="Snacks", image_url="https://img.icons8.com/color/96/potato-chips.png", stock=120),
            Product(retailer_id=retailer.id, name="Digestive Biscuits", price=50, description="Healthy digestive biscuits, 250g.", category="Snacks", image_url="https://img.icons8.com/color/96/cookies.png", stock=150),
            Product(retailer_id=retailer.id, name="Mixed Nuts", price=450, description="Premium roasted mixed nuts, 200g.", category="Snacks", image_url="https://img.icons8.com/color/96/nut.png", stock=40),

            # Personal Care
            Product(retailer_id=retailer.id, name="Herbal Shampoo", price=180, description="Natural aloe vera extract shampoo, 200ml.", category="Personal Care", image_url="https://img.icons8.com/color/96/shampoo.png", stock=45),
            Product(retailer_id=retailer.id, name="Anti-Dandruff Shampoo", price=220, description="Clinical strength anti-dandruff shampoo, 200ml.", category="Personal Care", image_url="https://img.icons8.com/color/96/shampoo.png", stock=40),
            Product(retailer_id=retailer.id, name="Mint Toothpaste", price=90, description="Fluoride toothpaste with fresh mint, 150g.", category="Personal Care", image_url="https://img.icons8.com/color/96/toothpaste.png", stock=100),
            Product(retailer_id=retailer.id, name="Lavender Soap", price=45, description="Soothing lavender scent bar soap, 100g.", category="Personal Care", image_url="https://img.icons8.com/color/96/soap.png", stock=120),
            Product(retailer_id=retailer.id, name="Sandalwood Soap", price=60, description="Premium sandalwood bar soap, 100g.", category="Personal Care", image_url="https://img.icons8.com/color/96/soap.png", stock=80),
            Product(retailer_id=retailer.id, name="Hand Wash", price=110, description="Antibacterial liquid hand wash, 250ml.", category="Personal Care", image_url="https://img.icons8.com/color/96/liquid-soap.png", stock=90),

            # Household
            Product(retailer_id=retailer.id, name="Dishwashing Liquid", price=80, description="Lemon scented dishwashing liquid, 500ml.", category="Household", image_url="https://img.icons8.com/color/96/washing-machine.png", stock=100),
            Product(retailer_id=retailer.id, name="Laundry Detergent", price=250, description="Front load laundry detergent powder, 1kg.", category="Household", image_url="https://img.icons8.com/color/96/washing-machine.png", stock=80),
            Product(retailer_id=retailer.id, name="Floor Cleaner", price=150, description="Pine scented surface cleaner, 1 liter.", category="Household", image_url="https://img.icons8.com/color/96/mop.png", stock=70),
            Product(retailer_id=retailer.id, name="Paper Towels", price=120, description="Absorbent kitchen paper rolls, pack of 2.", category="Household", image_url="https://img.icons8.com/color/96/toilet-paper.png", stock=150)
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

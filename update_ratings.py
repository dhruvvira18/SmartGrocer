from database import engine, SessionLocal
import models

db = SessionLocal()
products = db.query(models.Product).all()
for i, p in enumerate(products):
    if p.name == "Mangoes":
        p.rating = 5.0
    elif p.name == "Bananas":
        p.rating = 4.5
    elif p.name == "Fresh Apple":
        p.rating = 4.0
    elif p.name == "Potatoes":
        p.rating = 4.8
    else:
        p.rating = 3.0
db.commit()
print("Ratings updated!")

import sys
from pathlib import Path
from typing import Annotated

BASE_DIR = Path(__file__).resolve().parent 
ROOT_DIR = BASE_DIR.parent 
sys.path.append(str(ROOT_DIR))

from fastapi import FastAPI, Form, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import ValidationError, EmailStr

import models
from database import engine, get_db
from schemas import UserLogin, ProductCreate

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
DbSession = Annotated[Session, Depends(get_db)]

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/admin/{slug}/inventory", response_class=HTMLResponse)
async def inventory(slug: str, request: Request, db: DbSession):
    retailer = db.query(models.Retailer).filter(models.Retailer.slug == slug).first()
    if not retailer:
        raise HTTPException(status_code=404, detail="Retailer not found")

    products = db.query(models.Product).filter(models.Product.retailer_id == retailer.id).all()

    return templates.TemplateResponse("inventory.html", {"request": request, "retailer": retailer, "products": products})

@app.post("/admin/{slug}/inventory", response_class=HTMLResponse)
async def add_product(
    slug: str,
    request: Request,
    db: DbSession,
    name: Annotated[str, Form()],
    price: Annotated[int, Form()],
    category: Annotated[str, Form()],
    stock: Annotated[int, Form()],
    image_url: Annotated[str, Form()] = ""
):
    retailer = db.query(models.Retailer).filter(models.Retailer.slug == slug).first()
    if not retailer:
        raise HTTPException(status_code=404, detail="Retailer not found")

    try:
        product_data = ProductCreate(
            name=name,
            price=price,
            category=category,
            stock=stock,
            image_url=image_url
        )

        new_product = models.Product(
            retailer_id=retailer.id,
            name=product_data.name,
            price=product_data.price,
            category=product_data.category,
            stock=product_data.stock,
            image_url=product_data.image_url
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        # redirect back to GET inventory with success
        return RedirectResponse(url=f"/admin/{slug}/inventory", status_code=303)

    except ValidationError as e:
        products = db.query(models.Product).filter(models.Product.retailer_id == retailer.id).all()
        return templates.TemplateResponse("inventory.html", {
            "request": request,
            "retailer": retailer,
            "products": products,
            "error": e.errors()[0]["msg"]
        })

@app.get("/admin/{slug}/dashboard", response_class=HTMLResponse)
async def dashboard(slug: str, request: Request, db: DbSession):
    retailer = db.query(models.Retailer).filter(models.Retailer.slug == slug).first()
    if not retailer:
        raise HTTPException(status_code=404, detail="Retailer not found")
    return templates.TemplateResponse("dashboard.html", {"request": request, "retailer": retailer})

@app.post("/login")
async def admin_login(
    request: Request,
    db: DbSession,
    email: Annotated[EmailStr, Form()], 
    password: Annotated[str, Form()]
):
    try:
        credentials = UserLogin(email=email, password=password)
        user = db.query(models.User).filter(
            models.User.email == credentials.email,
            models.User.role == "admin"
        ).first()
        
        if user and user.password == credentials.password:
            retailer = db.query(models.Retailer).filter(models.Retailer.id == user.retailer_id).first()
            if not retailer:
                return templates.TemplateResponse("login.html", {"request": request, "error": "Retailer associated with this admin not found."})
            return RedirectResponse(url=f"/admin/{retailer.slug}/dashboard", status_code=303)
            
        return templates.TemplateResponse("login.html", {"request": request, "error": "Access Denied: Admin only."})
    except ValidationError as e:
        return templates.TemplateResponse("login.html", {"request": request, "error": e.errors()[0]["msg"]})
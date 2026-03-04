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
from schemas import UserLogin

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
DbSession = Annotated[Session, Depends(get_db)]

@app.get("/shop/{slug}", response_class=HTMLResponse)
async def store_front(slug: str, request: Request, db: DbSession):
    retailer = db.query(models.Retailer).filter(models.Retailer.slug == slug).first()
    if not retailer:
        raise HTTPException(status_code=404, detail="Store not found")
    return templates.TemplateResponse("login.html", {"request": request, "retailer": retailer})

@app.get("/shop/{slug}/index", response_class=HTMLResponse)
async def shop_index(slug: str, request: Request, db: DbSession):
    # Fetch retailer to ensure the store exists and get branding
    retailer = db.query(models.Retailer).filter(models.Retailer.slug == slug).first()
    if not retailer:
        raise HTTPException(status_code=404, detail="Store not found")
    
    # Fetch only THIS retailer's products
    products = db.query(models.Product).filter(models.Product.retailer_id == retailer.id).all()
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "retailer": retailer,
        "products": products
    })

@app.get("/shop/{slug}/check-user")
async def check_user(slug: str, email: str, db: DbSession):
    retailer = db.query(models.Retailer).filter(models.Retailer.slug == slug).first()
    user_exists = db.query(models.User).filter(
        models.User.email == email, 
        models.User.retailer_id == retailer.id
    ).first() is not None
    
    return {"exists": user_exists}

@app.post("/shop/{slug}/login")
async def login_or_signup(
    slug: str,
    request: Request,
    db: DbSession,
    email: Annotated[EmailStr, Form()], 
    password: Annotated[str, Form()],
    full_name: Annotated[str | None, Form()] = None,
    confirm_password: Annotated[str | None, Form()] = None
):
    retailer = db.query(models.Retailer).filter(models.Retailer.slug == slug).first()
    user = db.query(models.User).filter(
        models.User.email == email, 
        models.User.retailer_id == retailer.id
    ).first()

    if user:
        if user.password == password:
            return RedirectResponse(url=f"/shop/{slug}/index", status_code=303)
        
        # ERROR: Incorrect Password
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "retailer": retailer, 
            "error": "Incorrect password.",
            "email_val": email,
            "show_step2": True,  # General flag to stay in Step 2
            "is_signup": False   # Specific flag: this is a returning user
        })

    if not user:
        if not confirm_password or password != confirm_password:
            return templates.TemplateResponse("login.html", {
                "request": request, 
                "retailer": retailer, 
                "error": "Passwords do not match.",
                "email_val": email,        # Pass the email back
                "show_signup": True        # Tell the UI to stay on Step 2
            })
        
        new_user = models.User(
            email=email,
            password=password,
            full_name=full_name or "New Shopper",
            retailer_id=retailer.id,
            role="shopper"
        )
        db.add(new_user)
        db.commit()
        return RedirectResponse(url=f"/shop/{slug}/index", status_code=303)
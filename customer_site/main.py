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
from schemas import UserLogin, RatingUpdate, OrderCreate
import os
import time

from dotenv import load_dotenv
import razorpay

load_dotenv(ROOT_DIR / ".env")

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "rzp_test_SXTskXDYRZKbMw")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "XZiu70Deo7oXCU4rU2Q8Ryiu")

# Use your Test Keys from Razorpay Dashboard > Settings > API Keys
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
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
    
    # Check session
    shopper_id = request.cookies.get("shopper_id")
    user = None
    if shopper_id:
        try:
            user = db.query(models.User).filter(models.User.id == int(shopper_id)).first()
        except ValueError:
            pass

    # Fetch only THIS retailer's products
    products = db.query(models.Product).filter(models.Product.retailer_id == retailer.id).all()

    # Fetch unique categories for this retailer
    categories = db.query(models.Product.category).filter(
        models.Product.retailer_id == retailer.id
    ).distinct().all()
    categories = [c[0] for c in categories]
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "retailer": retailer,
        "products": products,
        "categories": categories,
        "user": user
    })

@app.get("/shop/{slug}/profile", response_class=HTMLResponse)
async def shop_profile(slug: str, request: Request, db: DbSession):
    retailer = db.query(models.Retailer).filter(models.Retailer.slug == slug).first()
    if not retailer:
        raise HTTPException(status_code=404, detail="Store not found")

    shopper_id = request.cookies.get("shopper_id")
    if not shopper_id:
        return RedirectResponse(url=f"/shop/{slug}", status_code=303)

    try:
        user = db.query(models.User).filter(models.User.id == int(shopper_id)).first()
    except ValueError:
        return RedirectResponse(url=f"/shop/{slug}", status_code=303)

    if not user:
        return RedirectResponse(url=f"/shop/{slug}", status_code=303)

    msg = request.query_params.get("msg")
    err = request.query_params.get("err")

    return templates.TemplateResponse("profile.html", {
        "request": request,
        "retailer": retailer,
        "user": user,
        "success": msg,
        "error": err
    })

@app.post("/shop/{slug}/profile")
async def update_profile(
    slug: str,
    request: Request,
    db: DbSession,
    full_name: Annotated[str, Form()],
    email: Annotated[EmailStr, Form()],
    address: Annotated[str | None, Form()] = None
):
    retailer = db.query(models.Retailer).filter(models.Retailer.slug == slug).first()
    if not retailer:
        raise HTTPException(status_code=404, detail="Store not found")

    shopper_id = request.cookies.get("shopper_id")
    if not shopper_id:
        return RedirectResponse(url=f"/shop/{slug}", status_code=303)

    try:
        user = db.query(models.User).filter(models.User.id == int(shopper_id)).first()
    except ValueError:
        return RedirectResponse(url=f"/shop/{slug}", status_code=303)

    if not user:
        return RedirectResponse(url=f"/shop/{slug}", status_code=303)

    # Check if new email is already taken by someone else
    if email != user.email:
        existing_user = db.query(models.User).filter(
            models.User.email == email,
            models.User.retailer_id == retailer.id
        ).first()
        if existing_user:
            return RedirectResponse(url=f"/shop/{slug}/profile?err=Email+is+already+in+use+by+another+account.", status_code=303)

    user.full_name = full_name
    user.email = email
    user.address = address
    db.commit()

    return RedirectResponse(url=f"/shop/{slug}/profile?msg=Profile+updated+successfully.", status_code=303)

@app.get("/shop/{slug}/logout")
async def logout(slug: str):
    response = RedirectResponse(url=f"/shop/{slug}", status_code=303)
    response.delete_cookie("shopper_id")
    return response

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
            response = RedirectResponse(url=f"/shop/{slug}/index", status_code=303)
            response.set_cookie(key="shopper_id", value=str(user.id), httponly=True)
            return response
        
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
        response = RedirectResponse(url=f"/shop/{slug}/index", status_code=303)
        response.set_cookie(key="shopper_id", value=str(new_user.id), httponly=True)
        return response

@app.post("/shop/{slug}/product/{product_id}/rate")
async def rate_product(
    slug: str,
    product_id: int,
    rating_data: RatingUpdate,
    db: DbSession
):
    retailer = db.query(models.Retailer).filter(models.Retailer.slug == slug).first()
    if not retailer:
        raise HTTPException(status_code=404, detail="Store not found")

    product = db.query(models.Product).filter(
        models.Product.id == product_id,
        models.Product.retailer_id == retailer.id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Calculate new average rating
    total_rating_sum = (product.rating * product.review_count) + rating_data.rating
    product.review_count += 1
    product.rating = total_rating_sum / product.review_count

    db.commit()
    db.refresh(product)

    return {"rating": product.rating, "review_count": product.review_count}

@app.post("/shop/{slug}/create-order")
async def create_order(slug: str, order_data: OrderCreate, db: DbSession):
    retailer = db.query(models.Retailer).filter(models.Retailer.slug == slug).first()
    if not retailer:
        raise HTTPException(status_code=404, detail="Store not found")

    # Amount must be in paise (1 INR = 100 paise) [cite: 11]
    amount_paise = int(round(order_data.amount * 100))

    data = {
        "amount": amount_paise,
        "currency": "INR",
        "receipt": f"receipt_{slug}_{int(time.time())}",
        "payment_capture": 1
    }

    try:
        razorpay_order = client.order.create(data=data)
        return {
            "order_id": razorpay_order['id'],
            "amount": amount_paise,
            "key_id": RAZORPAY_KEY_ID
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
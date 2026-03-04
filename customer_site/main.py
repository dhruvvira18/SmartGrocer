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

@app.post("/shop/{slug}/login")
async def login_or_signup(
    slug: str,
    request: Request,
    db: DbSession,
    email: Annotated[EmailStr, Form()], 
    password: Annotated[str, Form()]
):
    retailer = db.query(models.Retailer).filter(models.Retailer.slug == slug).first()
    try:
        credentials = UserLogin(
            email=email,
            password=password,
            retailer_id=retailer.id
        )
        user = db.query(models.User).filter(
            models.User.email == credentials.email, 
            models.User.retailer_id == retailer.id
        ).first()
        
        # INLINE ONBOARDING LOGIC
        if not user:
            # If user doesn't exist at this store, create them (Signup)
            new_user = models.User(
                email=credentials.email,
                password=credentials.password, # TODO: Hash this in production!
                retailer_id=retailer.id,
                role="shopper"
            )
            db.add(new_user)
            db.commit()
            return RedirectResponse(url=f"/shop/{slug}/index", status_code=303)

        if user.password == credentials.password:
            return RedirectResponse(url=f"/shop/{slug}/index", status_code=303)
            
        return templates.TemplateResponse("login.html", {"request": request, "retailer": retailer, "error": "Incorrect password."})

    except ValidationError as e:
        return templates.TemplateResponse("login.html", {"request": request, "retailer": retailer, "error": e.errors()[0]["msg"]})
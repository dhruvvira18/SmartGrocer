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

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

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
            return RedirectResponse(url="/dashboard", status_code=303)
            
        return templates.TemplateResponse("login.html", {"request": request, "error": "Access Denied: Admin only."})
    except ValidationError as e:
        return templates.TemplateResponse("login.html", {"request": request, "error": e.errors()[0]["msg"]})
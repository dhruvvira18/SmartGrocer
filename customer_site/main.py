import sys
from pathlib import Path
from typing import Annotated

# 1. Setup absolute paths
# This finds the directory where main.py lives (customer_site)
BASE_DIR = Path(__file__).resolve().parent 
# This finds the root directory (the parent of customer_site)
ROOT_DIR = BASE_DIR.parent 

# Add root to sys.path so we can import database, models, schemas
sys.path.append(str(ROOT_DIR))

from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import ValidationError, EmailStr

import models
from database import engine, get_db
from schemas import UserLogin

models.Base.metadata.create_all(bind=engine)

# 2. Mounting and Templates using absolute paths
app = FastAPI()

# This tells FastAPI: "Look for 'static' right next to this main.py file"
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# This tells Jinja2: "Look for 'templates' right next to this main.py file"
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Modern Type Aliases
DbSession = Annotated[Session, Depends(get_db)]

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # This renders the login page as the default home view
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/index", response_class=HTMLResponse)
async def index(request: Request):
    # This renders the index page
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/login")
async def login(
    request: Request,
    db: DbSession,
    # We use Form() to extract the data, but label the type for clarity
    email: Annotated[EmailStr, Form()], 
    password: Annotated[str, Form()]
):
    try:
        # Pass the extracted form data into our validator
        credentials = UserLogin(email=email, password=password)
        
        user = db.query(models.User).filter(models.User.email == credentials.email).first()
        
        if user and user.password == credentials.password:
            return RedirectResponse(url="/index", status_code=303)
            
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "error": "Invalid email or password."
        })

    except ValidationError as e:
        # Grabbing the first error message from our Pydantic Schema
        error_msg = e.errors()[0]["msg"]
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "error": error_msg
        })
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
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
import models
engine = create_engine("sqlite:///./test_smartgrocer.db")
SessionLocal = sessionmaker(bind=engine)
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()
app = FastAPI()
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
DbSession = Annotated[Session, Depends(get_db)]
@app.get("/shop/{slug}/index", response_class=HTMLResponse)
async def shop_index(slug: str, request: Request, db: DbSession, category: str | None = None):
    retailer = db.query(models.Retailer).filter(models.Retailer.slug == slug).first()
    if not retailer: raise HTTPException(status_code=404, detail="Store not found")
    query = db.query(models.Product).filter(models.Product.retailer_id == retailer.id)
    products = query.all()
    categories = db.query(models.Product.category).filter(models.Product.retailer_id == retailer.id).distinct().all()
    categories = [c[0] for c in categories]
    return templates.TemplateResponse("index.html", {"request": request, "retailer": retailer, "products": products, "categories": categories, "active_category": category})

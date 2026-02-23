import re
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
PASS_PATTERN = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    if not re.fullmatch(EMAIL_PATTERN, email) or not re.fullmatch(PASS_PATTERN, password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid format."})
    
    # Customer Mock Auth
    if email == "shopper@gmail.com" and password == "Shopper123":
        return RedirectResponse(url="/", status_code=303)
    
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials."})
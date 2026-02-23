from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def admin_login(request: Request, email: str = Form(...), password: str = Form(...)):
    # Admin Mock Auth
    if email == "admin@smartgrocer.com" and password == "AdminPass123":
        return RedirectResponse(url="/dashboard", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Unauthorized Access."})

@app.get("/dashboard")
async def dashboard(request: Request):
    # This is where the Inventory and CRM features will live
    return templates.TemplateResponse("dashboard.html", {"request": request})
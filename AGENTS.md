## 1. Project Identity & Goal
You are an expert **FastAPI Backend Engineer** working on a Retail/ERP system called **SmartGrocer** (inspired by RetailWhizz). The goal is a professional, high-performance grocery management system.

## 2. Core Technical Stack
* **Language:** Python 3.13+
* **Framework:** FastAPI (Modern 2026 standards)
* **ORM:** SQLAlchemy 2.0 (using `MappedAsDataclass` and `DeclarativeBase`)
* **Validation:** Pydantic v2
* **Database:** MySQL (MariaDB via XAMPP)
* **Template Engine:** Jinja2

---

## 3. Coding Standards & Constraints

### A. Dependency Injection
* **Strict Rule:** Always use `typing.Annotated` for dependencies and form fields.
* **Incorrect:** `db: Session = Depends(get_db)`
* **Correct:** `db: Annotated[Session, Depends(get_db)]`

### B. SQLAlchemy 2.0 Models
* All models must inherit from `Base(MappedAsDataclass, DeclarativeBase)`.
* Use `Mapped[]` and `mapped_column()` for type hinting.
* Set `init=False` on primary keys to allow the database to handle `AUTO_INCREMENT`.
* **MySQL Compatibility:** Always specify `String(length)` (e.g., `String(100)`) for VARCHAR columns used as indexes or unique keys.

### C. Pydantic Validation
* Use `EmailStr` for all email fields.
* **Regex Restriction:** Do NOT use regex look-aheads (e.g., `(?=...)`) as the Rust-based `pydantic-core` does not support them.
* Use `@field_validator` for logic like password strength or SKU formatting.

### D. File System & Pathing
* Use `pathlib.Path` for all directory handling.
* Maintain the split architecture: `customer_site/` and `admin_site/` share `models.py`, `schemas.py`, and `database.py` from the root.
* Use **absolute paths** for mounting static files and Jinja2 templates to prevent `RuntimeError`.

---

## 4. Operational Instructions
1. **Context Awareness:** Always check `root/models.py` before generating routes to ensure field name alignment.
2. **Database Sync:** Ensure `models.Base.metadata.create_all(bind=engine)` is called in the `main.py` entry point.
3. **Error Handling:** When catching `ValidationError`, extract the specific message using `e.errors()[0]["msg"]` to pass to the UI templates.
4. **Environment:** Assume the app is executed from the project root using `python -m uvicorn customer_site.main:app`.

## 5. Multi-Tenancy & SaaS Rules
* **Tenant Isolation:** Every query for Products, Users, or Orders MUST include a filter for `retailer_id`.
* **Slug-Based Routing:** Customer sites must use the `{slug}` parameter to identify the retailer context.
* **Composite Uniqueness:** User emails are unique *per retailer*, not globally.

## 6. Registration & Auth Logic
* **Inline Onboarding:** The customer login flow is a hybrid. If the email doesn't exist for that retailer, automatically create a 'shopper' account.
* **Admin Security:** Admin accounts must be created through a controlled onboarding flow, not the public customer login.

## 7. Mobile-First & PWA Standards
* **Responsive UI:** Templates must use mobile-first CSS (Bootstrap/Tailwind).
* **PWA Assets:** Maintain `manifest.json` and `service-worker.js` in `/static` to support "Add to Home Screen" functionality.
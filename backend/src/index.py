# backend/src/index.py
import os
import threading
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import the router we exported in sales_routes.py
from .routes.sales_routes import router as sales_router

from .utils.db import engine, Base

app = FastAPI(title="Truestate API")

# CORS: allow all or specify origins via env var
origins = os.getenv("CORS_ORIGINS", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origins] if origins != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include router under /api/sales
app.include_router(sales_router, prefix="/api/sales")

# Ensure DB tables exist
Base.metadata.create_all(bind=engine)

# OPTIONAL: if you have automatic import on startup logic, keep it here.
def _run_import_in_background():
    try:
        from .import_csv import import_sales, CSV_PATH
        print("Background import started. CSV:", CSV_PATH)
        total = import_sales()
        print("Background import completed. Total rows:", total)
    except Exception as e:
        print("Background import failed:", e)

@app.on_event("startup")
def on_startup():
    # Only start background import if IMPORT_ON_STARTUP env var true
    import_flag = os.getenv("IMPORT_ON_STARTUP", "false").lower() in ("1", "true", "yes")
    if not import_flag:
        print("IMPORT_ON_STARTUP not set; skipping automatic import.")
        return

    # quick check whether DB already has rows
    try:
        from .utils.db import SessionLocal
        from .models.sales_model import Sale
        db = SessionLocal()
        count = db.query(Sale).count()
        db.close()
    except Exception:
        count = 0

    if count and count > 0:
        print("DB already populated, skipping import (count=", count, ")")
        return

    t = threading.Thread(target=_run_import_in_background, daemon=True)
    t.start()

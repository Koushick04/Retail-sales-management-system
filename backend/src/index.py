# backend/src/index.py
import os
import threading
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .utils.db import engine, Base
from .routes.sales_routes import router as sales_router
from .import_csv import import_sales, CSV_PATH

app = FastAPI(title="Truestate API")

# CORS: allow your frontend on Render or localhost
origins = os.getenv("CORS_ORIGINS", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origins] if origins != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sales_router, prefix="/api/sales")

# Ensure DB created (safe)
Base.metadata.create_all(bind=engine)

def _run_import_in_background():
    try:
        print("Background import started. CSV:", CSV_PATH)
        total = import_sales()
        print("Background import completed. Total rows:", total)
    except Exception as e:
        print("Background import failed:", e)

@app.on_event("startup")
def on_startup():
    # If IMPORT_ON_STARTUP=true and DB empty, start import in a background thread.
    import_flag = os.getenv("IMPORT_ON_STARTUP", "false").lower() in ("1", "true", "yes")
    if not import_flag:
        print("IMPORT_ON_STARTUP not set; skipping automatic import.")
        return

    # Basic check: if table has any rows, skip import
    try:
        from .utils.db import SessionLocal
        from .models.sales_model import Sale
        db = SessionLocal()
        count = db.query(Sale).count()
        db.close()
    except Exception as e:
        print("DB count check failed, proceeding to import anyway:", e)
        count = 0

    if count and count > 0:
        print("DB already has rows (count=", count, "); skipping import.")
        return

    # Start import in background thread so server starts quickly
    t = threading.Thread(target=_run_import_in_background, daemon=True)
    t.start()

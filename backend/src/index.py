# backend/src/index.py
"""
Entrypoint for the FastAPI app.

This version uses absolute imports for the 'src' package so it matches the
usual Render start command:
    uvicorn src.index:app --host 0.0.0.0 --port $PORT

Behavior:
- Adds CORS middleware (controlled by CORS_ORIGINS env var; default "*")
- Includes the sales router imported from src.routes.sales_routes
- Ensures DB tables are created via Base.metadata.create_all
- Optionally starts a background CSV import when IMPORT_ON_STARTUP is true
  (only if the import function is present and the DB is empty)
- Exposes a simple /health endpoint
"""

import os
import threading
import logging
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# NOTE: using absolute imports (src.*) so uvicorn src.index:app works reliably.
from src.utils.db import engine, Base  # must define engine, Base, SessionLocal in src/utils/db.py
from src.routes.sales_routes import router as sales_router  # ensure router variable exists in this module

# import_csv is optional; wrap in try/except so missing file won't crash startup
import_available = True
try:
    from src.import_csv import import_sales, CSV_PATH  # import_sales() -> returns total rows imported
except Exception as e:
    import_available = False
    import_sales = None
    CSV_PATH = None
    logging.getLogger("uvicorn.error").warning("import_csv not available: %s", e)


# Create app
app = FastAPI(title="Truestate API")

# Configure logging (uvicorn will use this logger)
logger = logging.getLogger("uvicorn.error")

# CORS configuration. If CORS_ORIGINS contains a comma-separated list, split it.
# Default: allow all origins (dev). In production set to your frontend URL(s).
_raw_origins = os.getenv("CORS_ORIGINS", "*")
if _raw_origins.strip() == "*" or not _raw_origins:
    allow_origins = ["*"]
else:
    # support comma-separated values
    allow_origins = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers (prefixing /api where appropriate)
# The sales router itself already sets internal prefix like "/sales" if you want,
# but we keep a top-level prefix "/api" here so endpoints become /api/sales/...
app.include_router(sales_router, prefix="/api/sales")

# Health route
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}


# Ensure DB tables are created (safe; idempotent)
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables ensured via Base.metadata.create_all()")
except Exception as e:
    logger.exception("Failed to run Base.metadata.create_all(): %s", e)


# Helper to run import in background thread
def _run_import_in_background():
    """
    Runs the import_sales() function in a background thread and logs progress.
    This function is intentionally defensive: it catches and logs all exceptions.
    """
    if not import_available or import_sales is None:
        logger.warning("CSV import not available, skipping background import.")
        return

    try:
        logger.info("Background import started. CSV path: %s", CSV_PATH)
        total = import_sales()
        logger.info("Background import completed. Total rows imported: %s", total)
    except Exception as exc:
        logger.exception("Background import failed: %s", exc)


@app.on_event("startup")
def on_startup():
    """
    Startup event:
    - If IMPORT_ON_STARTUP (env) is set truthy and the DB appears empty, run import in background.
    - The DB emptiness check is a best-effort; if it fails we proceed to import as a fallback.
    """
    import_flag = os.getenv("IMPORT_ON_STARTUP", "false").lower() in ("1", "true", "yes")
    if not import_flag:
        logger.info("IMPORT_ON_STARTUP not set; skipping automatic import.")
        return

    if not import_available or import_sales is None:
        logger.warning("IMPORT_ON_STARTUP requested but import function not available; skipping.")
        return

    # Best-effort check: see if sales table has rows. If not, trigger import.
    count = 0
    try:
        # Import SessionLocal lazily to avoid circular imports at module import time
        from src.utils.db import SessionLocal
        from src.models.sales_model import Sale  # ensure this matches your model module/name

        db = SessionLocal()
        try:
            count = db.query(Sale).count()
        finally:
            db.close()
    except Exception as e:
        # If the count check fails, log and default to attempting import (safer for demos).
        logger.exception("DB count check failed; will attempt import anyway. Error: %s", e)
        count = 0

    if count and count > 0:
        logger.info("DB already contains %d rows; skipping import.", count)
        return

    # Launch background thread to import so the webserver can start quickly.
    t = threading.Thread(target=_run_import_in_background, daemon=True)
    t.start()
    logger.info("Started CSV import in background thread.")


# Optionally expose an admin endpoint to trigger import manually (careful in prod).
# Uncomment the following if you want an HTTP endpoint to trigger import:
#
# from fastapi import BackgroundTasks
#
# @app.post("/admin/import-csv", tags=["Admin"])
# def admin_import_csv(background_tasks: BackgroundTasks):
#     if not import_available or import_sales is None:
#         return {"ok": False, "reason": "import not available"}
#     background_tasks.add_task(_run_import_in_background)
#     return {"ok": True, "message": "Import started in background"}
#
# NOTE: Protect this endpoint (auth) in production; do not leave it open.


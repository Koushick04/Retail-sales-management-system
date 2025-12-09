# backend/src/routes/admin_routes.py
from fastapi import APIRouter, BackgroundTasks, HTTPException
from starlette.responses import JSONResponse

from ..import_csv import import_sales, CSV_PATH

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.post("/import")
def trigger_import(background_tasks: BackgroundTasks):
    """
    Trigger CSV import in background.
    This endpoint is intentionally unprotected for quick testing on Render.
    For production, secure it with auth.
    """
    try:
        # Schedule import to run in the background (non-blocking)
        background_tasks.add_task(_run_import)
        return JSONResponse({"status": "import_started", "csv": str(CSV_PATH)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def _run_import():
    try:
        print("Manual import started. CSV:", CSV_PATH)
        total = import_sales()
        print("Manual import finished. rows:", total)
    except Exception as e:
        print("Manual import failed:", e)

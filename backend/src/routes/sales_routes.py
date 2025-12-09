# backend/src/routes/sales_routes.py
from typing import Any
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from ..utils.db import SessionLocal
from ..services.sales_service import get_sales  # adjust if your service function name differs
from ..models.sales_schema import SaleOut  # optional: if you use pydantic response models

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=dict[str, Any])
def list_sales(request: Request, db: Session = Depends(get_db)):
    """
    Query params are passed through request.query_params (search, filters, page, limit, sort, etc.)
    The get_sales service should accept (db, params) and return (items, total).
    """
    params = dict(request.query_params)
    items, total = get_sales(db, params)
    # If you use Pydantic SaleOut you can convert; otherwise return plain dicts:
    try:
        data = [SaleOut.model_validate(item).model_dump() for item in items]
    except Exception:
        # fallback if SaleOut not configured: assume items are ORM objects and serialize manually
        data = []
        for s in items:
            data.append({
                "id": getattr(s, "id", None),
                "transaction_id": getattr(s, "transaction_id", None),
                "date": getattr(s, "date", None),
                "customer_id": getattr(s, "customer_id", None),
                "customer_name": getattr(s, "customer_name", None),
                "phone_number": getattr(s, "phone_number", None),
                "gender": getattr(s, "gender", None),
                "age": getattr(s, "age", None),
                "product_category": getattr(s, "product_category", None),
                "quantity": getattr(s, "quantity", None),
                "total_amount": getattr(s, "total_amount", None),
                "final_amount": getattr(s, "final_amount", None),
                "customer_region": getattr(s, "customer_region", None),
                "product_id": getattr(s, "product_id", None),
                "employee_name": getattr(s, "employee_name", None),
                "payment_method": getattr(s, "payment_method", None),
            })
    return {"data": data, "total": total}

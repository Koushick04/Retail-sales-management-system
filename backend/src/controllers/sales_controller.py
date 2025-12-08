from typing import Any

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from ..utils.db import SessionLocal
from ..services.sales_service import get_sales
from ..models.sales_model import Sale   # 👈 import the ORM model

# If you still want to keep SaleOut for other use-cases, you can keep this import,
# but it's no longer required in list_sales.
# from ..models.sales_schema import SaleOut


router = APIRouter()


def get_db():
    """Provide a DB session to each request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Helper: convert ORM object -> plain dict with all fields we care about
def sale_to_dict(sale: Sale) -> dict:
    return {
        "id": sale.id,
        "transaction_id": sale.transaction_id,
        "date": sale.date.isoformat() if sale.date else None,
        "customer_id": sale.customer_id,
        "customer_name": sale.customer_name,
        "phone_number": sale.phone_number,
        "gender": sale.gender,
        "age": sale.age,
        "product_category": sale.product_category,
        "quantity": sale.quantity,
        "total_amount": sale.total_amount,
        "final_amount": sale.final_amount,
        "customer_region": sale.customer_region,
        "product_id": sale.product_id,
        "employee_name": sale.employee_name,
        "payment_method": sale.payment_method,
    }


@router.get("/", response_model=dict[str, Any])
def list_sales(request: Request, db: Session = Depends(get_db)):
    """
    Main endpoint: /api/sales

    - reads all query params (search, filters, page, sort, etc.)
    - calls service layer to get matching records + total count
    - returns plain dicts with all fields including transaction_id
    """
    # All query params (search, filters, pagination)
    params = dict(request.query_params)

    # ORM objects + total count
    items, total = get_sales(db, params)

    # Convert each ORM Sale object to a simple dict
    data = [sale_to_dict(item) for item in items]

    return {"data": data, "total": total}

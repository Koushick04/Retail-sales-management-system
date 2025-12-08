# backend/src/services/sales_service.py

from datetime import datetime
from typing import Any, Dict, List, Tuple

from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..models.sales_model import Sale


def parse_int(value: Any, default: int | None = None) -> int | None:
    try:
        if value is None:
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def parse_date(value: str | None) -> datetime | None:
    if not value:
        return None
    # Expecting "YYYY-MM-DD"
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return None


def get_sales(db: Session, params: Dict[str, Any]) -> Tuple[List[Sale], int]:
    """
    Core service to fetch sales with:
    - search (name / phone / product)
    - filters (regions, gender, categories, payment_methods, date range)
    - sorting
    - pagination

    Returns: (items, total_count)
    """
    page = parse_int(params.get("page"), 1) or 1
    limit = parse_int(params.get("limit"), 10) or 10

    query = db.query(Sale)

    # ------------------------
    # Search (customer/product/phone)
    # ------------------------
    search = (params.get("search") or "").strip()
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            (Sale.customer_name.ilike(pattern))
            | (Sale.phone_number.ilike(pattern))
            | (Sale.product_name.ilike(pattern))
        )

    # ------------------------
    # Filters: regions, gender, categories, payment methods
    # ------------------------

    # Regions (comma-separated: "North,South")
    regions_str = params.get("regions")
    if regions_str:
        regions = [r.strip() for r in regions_str.split(",") if r.strip()]
        if regions:
            query = query.filter(Sale.customer_region.in_(regions))

    # Gender (comma-separated) – using "gender" key
    genders_str = params.get("gender") or params.get("genders")
    if genders_str:
        genders = [g.strip() for g in genders_str.split(",") if g.strip()]
        if genders:
            query = query.filter(Sale.gender.in_(genders))

    # Product categories (comma-separated)
    categories_str = params.get("categories")
    if categories_str:
        categories = [c.strip() for c in categories_str.split(",") if c.strip()]
        if categories:
            query = query.filter(Sale.product_category.in_(categories))
                # Product tags (comma-separated)
    tags_str = params.get("tags")
    if tags_str:
        tags = [t.strip() for t in tags_str.split(",") if t.strip()]
        if tags:
            query = query.filter(Sale.tags.in_(tags))


    # Payment methods (comma-separated)
    pay_str = params.get("payment_methods")
    if pay_str:
        payment_methods = [p.strip() for p in pay_str.split(",") if p.strip()]
        if payment_methods:
            query = query.filter(Sale.payment_method.in_(payment_methods))

    # ------------------------
    # Date range (start_date, end_date)
    # ------------------------
    start_date = parse_date(params.get("start_date"))
    end_date = parse_date(params.get("end_date"))

    if start_date and end_date:
        query = query.filter(and_(Sale.date >= start_date, Sale.date <= end_date))
    elif start_date:
        query = query.filter(Sale.date >= start_date)
    elif end_date:
        query = query.filter(Sale.date <= end_date)

    # ------------------------
    # Sorting
    # ------------------------
    sort_field = params.get("sort_field") or "date"
    sort_order = params.get("sort_order") or "desc"

    sort_fields_map = {
        "date": Sale.date,
        "final_amount": Sale.final_amount,
        "quantity": Sale.quantity,
        "customer_name": Sale.customer_name,  # 👈 NEW: sort by customer name
    }

    sort_column = sort_fields_map.get(sort_field, Sale.date)

    if sort_order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    # ------------------------
    # Pagination
    # ------------------------
    total = query.count()
    items = (
        query.offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return items, total

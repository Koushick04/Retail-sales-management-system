# backend/src/import_csv.py
import os
import csv
from pathlib import Path
from sqlalchemy.exc import SQLAlchemyError
from .utils.db import SessionLocal, engine, Base
from .models.sales_model import Sale

# Determine CSV path (env CSV_PATH overrides default)
PROJECT_ROOT = Path(__file__).resolve().parent.parent  # backend/
DEFAULT_CSV = PROJECT_ROOT / "data" / "sales_data.csv"
CSV_PATH = Path(os.getenv("CSV_PATH", str(DEFAULT_CSV)))

BATCH_SIZE = 5000

# Ensure tables exist (safe to call multiple times)
Base.metadata.create_all(bind=engine)

def import_sales(progress_callback=None):
    """
    Import CSV rows into DB using bulk_save_objects batches.
    progress_callback(total_inserted) optional for logging/progress.
    Returns total inserted count.
    """
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV file not found: {CSV_PATH}")

    session = SessionLocal()
    total_inserted = 0
    try:
        with CSV_PATH.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            batch = []
            for row in reader:
                # Map CSV columns -> model fields (exact header names expected)
                sale = Sale(
                    transaction_id=row.get("Transaction ID"),
                    date=row.get("Date"),
                    customer_id=row.get("Customer ID"),
                    customer_name=row.get("Customer Name"),
                    phone_number=row.get("Phone Number"),
                    gender=row.get("Gender"),
                    age=int(row["Age"]) if row.get("Age") else None,
                    customer_region=row.get("Customer Region"),
                    customer_type=row.get("Customer Type"),
                    product_id=row.get("Product ID"),
                    product_name=row.get("Product Name"),
                    brand=row.get("Brand"),
                    product_category=row.get("Product Category"),
                    tags=row.get("Tags"),
                    quantity=int(row["Quantity"]) if row.get("Quantity") else None,
                    price_per_unit=float(row["Price per Unit"]) if row.get("Price per Unit") else None,
                    discount_percentage=float(row["Discount Percentage"]) if row.get("Discount Percentage") else None,
                    total_amount=float(row["Total Amount"]) if row.get("Total Amount") else None,
                    final_amount=float(row["Final Amount"]) if row.get("Final Amount") else None,
                    payment_method=row.get("Payment Method"),
                    order_status=row.get("Order Status"),
                    delivery_type=row.get("Delivery Type"),
                    store_id=row.get("Store ID"),
                    store_location=row.get("Store Location"),
                    salesperson_id=row.get("Salesperson ID"),
                    employee_name=row.get("Employee Name"),
                )
                batch.append(sale)

                if len(batch) >= BATCH_SIZE:
                    session.bulk_save_objects(batch)
                    session.commit()
                    total_inserted += len(batch)
                    if progress_callback:
                        progress_callback(total_inserted)
                    else:
                        print(f"Inserted rows so far: {total_inserted}")
                    batch.clear()
            # final remaining
            if batch:
                session.bulk_save_objects(batch)
                session.commit()
                total_inserted += len(batch)
                if progress_callback:
                    progress_callback(total_inserted)
                else:
                    print(f"Inserted rows so far: {total_inserted}")

        return total_inserted

    except SQLAlchemyError as e:
        session.rollback()
        print("Database error:", e)
        raise
    finally:
        session.close()

def main():
    print("Working dir:", os.getcwd())
    print("Using CSV file:", CSV_PATH)
    total = import_sales()
    print("Import finished. Total rows inserted:", total)

if __name__ == "__main__":
    main()

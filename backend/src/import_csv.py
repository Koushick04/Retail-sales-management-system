import os
import csv
from pathlib import Path

from sqlalchemy.exc import SQLAlchemyError

from .utils.db import SessionLocal, engine, Base
from .models.sales_model import Sale

# --------------------------------------------------------------------
# 1. Figure out which CSV to use
#    - LOCAL / Docker: use full data file data/sales_data.csv
#    - RENDER: set env CSV_PATH=data/sales_data_render.csv
# --------------------------------------------------------------------

# /opt/render/project/src  (when running on Render)
# C:\...\backend\src       (when running locally)
SRC_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SRC_DIR.parent   # this is backend/ folder

DEFAULT_CSV = PROJECT_ROOT / "data" / "sales_data.csv"

CSV_PATH = Path(os.getenv("CSV_PATH", str(DEFAULT_CSV)))

print("Working dir:", os.getcwd())
print("Using CSV file:", CSV_PATH)

# make sure tables exist (harmless if already created)
Base.metadata.create_all(bind=engine)

BATCH_SIZE = 5000


def import_sales():
    session = SessionLocal()
    total_inserted = 0

    if not CSV_PATH.exists():
        print("❌ CSV file not found:", CSV_PATH)
        return

    try:
        with CSV_PATH.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            batch = []

            for row in reader:
                # map CSV columns -> SQLAlchemy model fields
                sale = Sale(
                    transaction_id=row["Transaction ID"],
                    date=row["Date"],  # SQLAlchemy will cast string to date
                    customer_id=row["Customer ID"],
                    customer_name=row["Customer Name"],
                    phone_number=row["Phone Number"],
                    gender=row["Gender"],
                    age=int(row["Age"]) if row["Age"] else None,
                    customer_region=row["Customer Region"],
                    customer_type=row["Customer Type"],
                    product_id=row["Product ID"],
                    product_name=row["Product Name"],
                    brand=row["Brand"],
                    product_category=row["Product Category"],
                    tags=row["Tags"],
                    quantity=int(row["Quantity"]) if row["Quantity"] else None,
                    price_per_unit=float(row["Price per Unit"])
                    if row["Price per Unit"]
                    else None,
                    discount_percentage=float(row["Discount Percentage"])
                    if row["Discount Percentage"]
                    else None,
                    total_amount=float(row["Total Amount"])
                    if row["Total Amount"]
                    else None,
                    final_amount=float(row["Final Amount"])
                    if row["Final Amount"]
                    else None,
                    payment_method=row["Payment Method"],
                    order_status=row["Order Status"],
                    delivery_type=row["Delivery Type"],
                    store_id=row["Store ID"],
                    store_location=row["Store Location"],
                    salesperson_id=row["Salesperson ID"],
                    employee_name=row["Employee Name"],
                )

                batch.append(sale)

                # insert batch
                if len(batch) >= BATCH_SIZE:
                    session.bulk_save_objects(batch)
                    session.commit()
                    total_inserted += len(batch)
                    print(f"Inserted rows so far: {total_inserted}")
                    batch.clear()

            # insert any remaining rows
            if batch:
                session.bulk_save_objects(batch)
                session.commit()
                total_inserted += len(batch)
                print(f"Inserted rows so far: {total_inserted}")

        print("✅ Import finished. Total rows inserted:", total_inserted)

    except SQLAlchemyError as e:
        session.rollback()
        print("❌ Database error during import:", e)

    finally:
        session.close()


def main():
    import_sales()


if __name__ == "__main__":
    main()

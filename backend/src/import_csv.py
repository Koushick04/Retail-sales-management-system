# backend/src/import_csv.py

import os
import csv
import requests
from io import StringIO
from sqlalchemy.exc import SQLAlchemyError
from .utils.db import SessionLocal, engine, Base
from .models.sales_model import Sale

CSV_URL = os.getenv("CSV_URL")  # URL to RAW CSV on GitHub
BATCH_SIZE = 5000

# Make sure tables exist
Base.metadata.create_all(bind=engine)


def import_sales(progress_callback=None):
    """
    Downloads CSV from GitHub RAW link and imports into Neon DB.
    Uses batch inserts for speed.
    """
    if not CSV_URL:
        raise Exception("CSV_URL environment variable is not set!")

    print("Downloading CSV from:", CSV_URL)

    # Download CSV
    response = requests.get(CSV_URL)
    response.raise_for_status()

    csv_text = response.text
    reader = csv.DictReader(StringIO(csv_text))

    session = SessionLocal()
    total_inserted = 0
    batch = []

    try:
        for row in reader:
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
                print(f"Inserted rows so far: {total_inserted}")
                batch.clear()

        # Insert remaining rows
        if batch:
            session.bulk_save_objects(batch)
            session.commit()
            total_inserted += len(batch)
            print(f"Inserted rows so far: {total_inserted}")

        print("Total rows inserted:", total_inserted)
        return total_inserted

    except SQLAlchemyError as e:
        session.rollback()
        print("DB Error:", e)
        raise
    finally:
        session.close()


def main():
    print("Using CSV URL:", CSV_URL)
    total = import_sales()
    print("Import finished. Total rows inserted:", total)


if __name__ == "__main__":
    main()

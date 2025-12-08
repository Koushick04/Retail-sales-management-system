import os
import csv
from datetime import datetime
from .utils.db import SessionLocal
from .models.sales_model import Sale

CSV_PATH = "data/sales_data.csv"
CHUNK_SIZE = 5000  # rows per batch


def parse_int(value, default=None):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def parse_float(value, default=None):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def parse_date(value, default=None):
    if not value:
        return default
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except (ValueError, TypeError):
            continue
    return default


def import_sales():
    print("Working dir:", os.getcwd())
    print("Looking for CSV at:", os.path.abspath(CSV_PATH))
    print("File exists?", os.path.exists(CSV_PATH))

    if not os.path.exists(CSV_PATH):
        print("❌ CSV file not found. Check path and volume mapping.")
        return

    db = SessionLocal()
    total_rows = 0
    batch = []

    try:
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for i, row in enumerate(reader, start=1):
                # Show first 3 rows for debugging
                if i <= 3:
                    print("Sample row", i, ":", row)

                sale = Sale(
                    transaction_id=row["Transaction ID"],
                    customer_id=row.get("Customer ID"),
                    customer_name=row.get("Customer Name"),
                    phone_number=row.get("Phone Number"),
                    gender=row.get("Gender"),
                    age=parse_int(row.get("Age")),
                    customer_region=row.get("Customer Region"),

                    product_id=row.get("Product ID"),
                    product_name=row.get("Product Name"),
                    brand=row.get("Brand"),
                    product_category=row.get("Product Category"),
                    tags=row.get("Tags") or "",

                    quantity=parse_int(row.get("Quantity")),
                    price_per_unit=parse_float(row.get("Price per Unit")),
                    discount_percentage=parse_float(row.get("Discount Percentage")),
                    total_amount=parse_float(row.get("Total Amount")),
                    final_amount=parse_float(row.get("Final Amount")),

                    date=parse_date(row.get("Date")),
                    payment_method=row.get("Payment Method"),
                    order_status=row.get("Order Status"),
                    delivery_type=row.get("Delivery Type"),
                    store_id=row.get("Store ID"),
                    store_location=row.get("Store Location"),
                    salesperson_id=row.get("Salesperson ID"),
                    employee_name=row.get("Employee Name"),
                )

                batch.append(sale)

                # When batch reaches CHUNK_SIZE, insert and clear it
                if len(batch) >= CHUNK_SIZE:
                    db.bulk_save_objects(batch)
                    db.commit()
                    total_rows += len(batch)
                    print(f"Inserted rows so far: {total_rows}")
                    batch.clear()

            # Insert any remaining rows
            if batch:
                db.bulk_save_objects(batch)
                db.commit()
                total_rows += len(batch)

        print("✅ Import finished. Total rows inserted:", total_rows)

    finally:
        db.close()


if __name__ == "__main__":
    import_sales()

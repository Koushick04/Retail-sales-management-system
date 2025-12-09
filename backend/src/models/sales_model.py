# backend/src/models/sales_model.py

from sqlalchemy import Column, Integer, String, Float, Date, Text
from ..utils.db import Base

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, index=True)
    date = Column(String)  # keep string to avoid parsing issues; you can use Date if you want
    customer_id = Column(String, index=True)
    customer_name = Column(String, index=True)
    phone_number = Column(String)
    gender = Column(String)
    age = Column(Integer)
    customer_region = Column(String)
    customer_type = Column(String)

    # Product fields
    product_id = Column(String, index=True)
    product_name = Column(String)
    brand = Column(String)
    product_category = Column(String)
    tags = Column(Text)  # Tags may be long, store as Text

    # Sales / price fields
    quantity = Column(Integer)
    price_per_unit = Column(Float)
    discount_percentage = Column(Float)
    total_amount = Column(Float)
    final_amount = Column(Float)

    # Operational fields
    payment_method = Column(String)
    order_status = Column(String)
    delivery_type = Column(String)
    store_id = Column(String)
    store_location = Column(String)
    salesperson_id = Column(String)
    employee_name = Column(String)

from sqlalchemy import Column, Integer, String, Float, Date
from ..utils.db import Base

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, index=True)


    # Customer Fields
    customer_id = Column(String, index=True)
    customer_name = Column(String, index=True)
    phone_number = Column(String, index=True)
    gender = Column(String, index=True)
    age = Column(Integer)
    customer_region = Column(String, index=True)

    # Product Fields
    product_id = Column(String, index=True)
    product_name = Column(String, index=True)
    brand = Column(String, index=True)
    product_category = Column(String, index=True)
    tags = Column(String)  # comma-separated tags

    # Sales Fields
    quantity = Column(Integer)
    price_per_unit = Column(Float)
    discount_percentage = Column(Float)
    total_amount = Column(Float)
    final_amount = Column(Float)

    # Operational Fields
    date = Column(Date, index=True)
    payment_method = Column(String, index=True)
    order_status = Column(String)
    delivery_type = Column(String)
    store_id = Column(String, index=True)
    store_location = Column(String)
    salesperson_id = Column(String, index=True)
    employee_name = Column(String)

from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict

class SaleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # Pydantic v2 way

    id: int
    customer_id: Optional[str]
    customer_name: Optional[str]
    phone_number: Optional[str]
    gender: Optional[str]
    age: Optional[int]
    customer_region: Optional[str]

    product_id: Optional[str]
    product_name: Optional[str]
    brand: Optional[str]
    product_category: Optional[str]
    tags: Optional[str]

    quantity: Optional[int]
    price_per_unit: Optional[float]
    discount_percentage: Optional[float]
    total_amount: Optional[float]
    final_amount: Optional[float]

    date: Optional[date]
    payment_method: Optional[str]
    order_status: Optional[str]
    delivery_type: Optional[str]
    store_id: Optional[str]
    store_location: Optional[str]
    salesperson_id: Optional[str]
    employee_name: Optional[str]

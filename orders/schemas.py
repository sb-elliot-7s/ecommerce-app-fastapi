from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from products.schemas import ProductSchema


class CreateAddressSchema(BaseModel):
    country: Optional[str]
    city: str
    street: Optional[str]
    house_number: Optional[str]
    apartment_number: Optional[str]
    zipcode: Optional[str]


class AddressSchema(CreateAddressSchema):
    id: int
    user_id: int


class OrderProductSchema(BaseModel):
    id: int
    order_id: int
    quantity: int = 1
    product: ProductSchema


class PlacedOrderSchema(BaseModel):
    id: int
    user_id: int
    created: datetime
    is_ordered: bool
    total_price: float
    order_products: list[OrderProductSchema]
    shipping_address: Optional[AddressSchema]

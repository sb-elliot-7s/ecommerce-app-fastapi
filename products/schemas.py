from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum
from fastapi import Form, Query


class Color(str, Enum):
    BLACK = 'BLACK'
    WHITE = 'WHITE'
    RED = 'RED'
    GREEN = 'GREEN'
    BLUE = 'BLUE'
    YELLOW = 'YELLOW'
    GREY = 'GREY'


class Gender(str, Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'


class Brand(str, Enum):
    PERFORMANCE = 'PERFORMANCE'
    ORIGINALS = 'ORIGINALS'
    SPORTSWEAR = 'SPORTSWEAR'


class Material(str, Enum):
    LEATHER = 'LEATHER'
    TEXTILE = 'TEXTILE'
    SYNTHETIC = 'SYNTHETIC'


class Category(str, Enum):
    SNEAKERS = 'SNEAKERS'
    TRAINERS = 'TRAINERS'
    LOAFERS = 'LOAFERS'


class CreateOrUpdateProductSchema(BaseModel):
    category: Optional[Category] = Category.SNEAKERS.value
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str]
    price: Optional[float] = Field(None, gt=0.0)
    color: Optional[Color] = Color.WHITE.value
    gender: Optional[Gender] = Gender.MALE.value
    brand: Optional[Brand] = Brand.ORIGINALS.value
    material: Optional[Material] = Material.LEATHER.value

    @classmethod
    def as_form(cls, category: Optional[Category] = Form(Category.SNEAKERS.value),
                title: Optional[str] = Form(None),
                description: Optional[str] = Form(None),
                price: Optional[float] = Form(None),
                color: Optional[Color] = Form(Color.WHITE.value),
                gender: Optional[Gender] = Form(Gender.MALE.value),
                brand: Optional[Brand] = Form(Brand.ORIGINALS.value),
                material: Optional[Material] = Form(Material.LEATHER.value)):
        return cls(category=category, title=title, description=description, price=price, color=color, gender=gender, brand=brand, material=material)


class QueryProductSchema(BaseModel):
    category: Optional[list[Category]] = Category.SNEAKERS.value
    color: Optional[list[Color]] = Color.WHITE.value
    gender: Optional[list[Gender]] = Gender.MALE.value
    brand: Optional[list[Brand]] = Brand.ORIGINALS.value
    material: Optional[list[Material]] = Material.LEATHER.value

    @classmethod
    def as_query(cls, category: Optional[list[Category]] = Query(None),
                 color: Optional[list[Color]] = Query(None),
                 gender: Optional[list[Gender]] = Query(None),
                 brand: Optional[list[Brand]] = Query(None),
                 material: Optional[list[Material]] = Query(None)):
        return cls(category=category, color=color, gender=gender, brand=brand, material=material)


class QueryPriceSchema(BaseModel):
    min_price: Optional[float]
    max_price: Optional[float]

    @classmethod
    def as_query(cls, min_price: Optional[float] = Query(None), max_price: Optional[float] = Query(None)):
        return cls(min_price=min_price, max_price=max_price)


class ImageSchema(BaseModel):
    id: int
    photo: str
    product_id: int

    class Config:
        orm_mode = True


class ProductSchema(CreateOrUpdateProductSchema):
    id: int
    created: datetime
    updated: datetime
    is_active: bool = True
    user_id: int
    images: list[ImageSchema]

    class Config:
        orm_mode = True
        use_enum_values = True
        json_encoders = {datetime: lambda v: v.strftime('%Y-%m-%d %H:%M')}


class FavoriteSchema(BaseModel):
    user_id: int
    products: list[ProductSchema]

from database import Base
import sqlalchemy as _sql
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.dialects.postgresql import ENUM


class Product(Base):
    __tablename__ = 'products'

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.String(length=255), nullable=False)
    description = _sql.Column(_sql.String, nullable=True)
    price = _sql.Column(_sql.Numeric(12, 2))
    category = _sql.Column(ENUM('SNEAKERS', 'TRAINERS', 'LOAFERS', name='category', create_type=False), nullable=False, default='SNEAKERS')
    color = _sql.Column(ENUM('BLACK', 'WHITE', 'RED', 'BLUE', 'GREEN', 'YELLOW', 'GREY', name='color', create_type=False), nullable=False,
                        default='WHITE')
    gender = _sql.Column(ENUM('MALE', 'FEMALE', name='gender', create_type=False), nullable=False, default='MALE')
    brand = _sql.Column(ENUM('PERFORMANCE', 'ORIGINALS', 'SPORTSWEAR', name='brand', create_type=False), nullable=True, default='ORIGINALS')
    material = _sql.Column(ENUM('LEATHER', 'TEXTILE', 'SYNTHETIC', name='material', create_type=False), nullable=False, default='LEATHER')
    is_active = _sql.Column(_sql.Boolean, default=True)
    created = _sql.Column(_sql.DateTime, default=datetime.now)
    updated = _sql.Column(_sql.DateTime, default=datetime.now, onupdate=datetime.now)

    user_id = _sql.Column(_sql.Integer, _sql.ForeignKey('users.id'))

    images = relationship('Image', backref='product',cascade='all, delete', lazy='joined')
    order_products = relationship('OrderProduct', backref='product', cascade='all, delete', lazy='joined')
    favorites = relationship('Favorite', cascade='all, delete', backref='product', lazy='joined')

    def __repr__(self) -> str:
        return f'Product: {self.title} {self.price}'


class Image(Base):
    __tablename__ = 'images'

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    photo = _sql.Column(_sql.String)
    product_id = _sql.Column(_sql.Integer, _sql.ForeignKey('products.id'))

    def __repr__(self) -> str:
        return f'Image: {self.photo}'


class Favorite(Base):
    __tablename__ = 'favorites'

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    user_id = _sql.Column(_sql.Integer, _sql.ForeignKey('users.id'))
    product_id = _sql.Column(_sql.Integer, _sql.ForeignKey('products.id'))
    is_favorite = _sql.Column(_sql.Boolean, default=False)

    def __repr__(self) -> str:
        return f'Favorite product == {self.product_id} from {self.user_id}'

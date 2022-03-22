from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from database import Base
from sqlalchemy.orm import relationship
import sqlalchemy as _sql


class PlacedOrder(Base):
    __tablename__ = 'placed_orders'

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    user_id = _sql.Column(_sql.Integer, _sql.ForeignKey('users.id'))
    created = _sql.Column(_sql.DateTime, default=datetime.now)
    is_ordered = _sql.Column(_sql.Boolean, default=False)
    shipping_address = _sql.Column(_sql.Integer, _sql.ForeignKey('addresses.id'))

    order_products = relationship('OrderProduct', backref='order', cascade='all, delete', lazy='joined')

    @hybrid_property
    def get_total_price(self):
        return sum(product.get_total_product_price for product in self.order_products)

    def __repr__(self) -> str:
        return f'Order: {self.id}'


class OrderProduct(Base):
    __tablename__ = 'order_products'

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    order_id = _sql.Column(_sql.Integer, _sql.ForeignKey('placed_orders.id'))
    product_id = _sql.Column(_sql.Integer, _sql.ForeignKey('products.id'))
    quantity = _sql.Column(_sql.Integer, default=1)

    @hybrid_property
    def get_total_product_price(self):
        return self.quantity * self.product.price 

    def __repr__(self) -> str:
        return f'OrderProduct: {self.id}'


class Address(Base):
    __tablename__ = 'addresses'

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    country = _sql.Column(_sql.String(length=100), nullable=True)
    city = _sql.Column(_sql.String(length=100))
    street = _sql.Column(_sql.String(length=100), nullable=True)
    house_number = _sql.Column(_sql.String(length=20), nullable=True)
    apartment_number = _sql.Column(_sql.String(length=100), nullable=True)
    zipcode = _sql.Column(_sql.String(length=100), nullable=True)

    placed_orders = relationship(PlacedOrder, backref='address', cascade='all, delete', lazy='joined')

    def __repr__(self) -> str:
        return f'Address: {self.id}'

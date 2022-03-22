from database import Base

import sqlalchemy as _sql
from sqlalchemy.orm import relationship
from datetime import datetime
from orders.models import PlacedOrder

class User(Base):
    __tablename__ = 'users'
    
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    first_name = _sql.Column(_sql.String(length=100), nullable=True)
    last_name = _sql.Column(_sql.String(length=100), nullable=True)
    email = _sql.Column(_sql.String, unique=True)
    password = _sql.Column(_sql.String)
    description = _sql.Column(_sql.String, nullable=True)
    is_active = _sql.Column(_sql.Boolean, default=True)
    created = _sql.Column(_sql.DateTime, default=datetime.now)
    updated = _sql.Column(_sql.DateTime, default=datetime.now, onupdate=datetime.now)

    is_admin = _sql.Column(_sql.Boolean, default=False)

    orders = relationship(PlacedOrder, backref='user', cascade='all, delete', lazy='joined')
    favorites = relationship('Favorite', cascade='all, delete', backref='user', lazy='joined')
    products = relationship('Product', backref='user', cascade='all, delete', lazy='joined')

    def __repr__(self) -> str:
        return f'User: {self.id} {self.first_name} {self.last_name}'

    
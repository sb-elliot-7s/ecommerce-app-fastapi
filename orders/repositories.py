from products.models import Product
from users.models import User
from .interfaces.repositories_interface import OrderRepositoryInterface
from .models import PlacedOrder, OrderProduct, Address
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from .schemas import PlacedOrderSchema, OrderProductSchema
from sqlalchemy.orm import joinedload
from fastapi import HTTPException, status


class OrderRepository(OrderRepositoryInterface):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def _get_order(self, user: User):
        result = await self._session.execute(select(PlacedOrder).options(joinedload(PlacedOrder.order_products).joinedload(OrderProduct.product)).where(PlacedOrder.user_id == user.id, PlacedOrder.is_ordered == False))
        if not (_order := result.scalars().first()): 
            return None
        return _order

    async def _get_order_or_none(self, user: User):
        _order:PlacedOrder = await self._get_order(user=user)
        if not _order: 
            raise HTTPException(detail='Placed Order not found', status_code=status.HTTP_404_NOT_FOUND)
        return _order

    async def get_order_products(self, user: User):
        _order = await self._get_order_or_none(user=user)
        total_price = _order.get_total_price
        products = [OrderProductSchema(product=p.product, quantity=p.quantity, id=p.id, order_id=p.order_id) for p in _order.order_products]
        return PlacedOrderSchema(id=_order.id, user_id=_order.user_id, created=_order.created, is_ordered=_order.is_ordered,
                                 order_products=products, total_price=total_price)

    async def add_to_cart(self, product_id: int, user: User):
        _order = await self._get_order(user=user)
        if not _order:
            _ = await self._session.execute(insert(PlacedOrder).values(user_id=user.id, is_ordered=False))
            await self._session.commit()
        _order = await self._get_order(user=user)
        product_res = await self._session.execute(select(Product).where(Product.id == product_id))
        product = product_res.scalars().first()
        order_product_result = await self._session.execute(select(OrderProduct)
                                                           .where(OrderProduct.order_id == _order.id, OrderProduct.product_id == product.id))
        op = order_product_result.scalars().first()
        if op:
            op.quantity += 1
            await self._session.commit()
            await self._session.refresh(op)
            return op
        else:
            order_product_result = await self._session.execute(insert(OrderProduct)
                                                               .values(order_id=_order.id, product_id=product.id).returning(OrderProduct))
            await self._session.commit()
            return order_product_result.first()

    async def remove_from_cart(self, order_product_id: int, user: User):
        _order = await self._get_order_or_none(user=user)
        order_product_result = await self._session.execute(select(OrderProduct)
                                                           .where(OrderProduct.id == order_product_id, OrderProduct.order_id == _order.id))
        _order_product = order_product_result.scalars().first()
        if not _order_product: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Order Product not found')
        if _order_product.quantity > 1:
            _order_product.quantity -= 1
            await self._session.commit()
        else:
            await self._session.delete(_order_product)
            await self._session.commit()

    async def add_shipping_address_and_payment(self, shipping_address: dict, user: User):
        _order: PlacedOrder = await self._get_order_or_none(user=user)
        result = await self._session.execute(insert(Address).values(**shipping_address).returning(Address.id))
        await self._session.commit()
        shipping_address_id = result.scalar()
        _order.shipping_address = shipping_address_id
        
        # --> add payment system <--

        _order.is_ordered = True
        await self._session.commit()

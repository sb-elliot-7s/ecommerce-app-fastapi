from fastapi import APIRouter, Depends, status
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from permissions import GetUser
from users.models import User
from users.token_service import TokenService
from .services import OrderService
from .repositories import OrderRepository
from .schemas import PlacedOrderSchema, CreateAddressSchema


orders_routers = APIRouter(prefix='/orders', tags=['orders'])

@orders_routers.post('/payment')
async def add_shipping_address_and_fake_pay_order(shipping_address: CreateAddressSchema, db: AsyncSession = Depends(get_db),
                                               user: User = Depends(GetUser(token_service=TokenService()))):
    return await OrderService(repository=OrderRepository(session=db)).payment_order(user=user, shipping_address=shipping_address)


@orders_routers.get('/', status_code=status.HTTP_200_OK, response_model=PlacedOrderSchema)
async def get_order(db: AsyncSession = Depends(get_db), user: User = Depends(GetUser(token_service=TokenService()))):
    return await OrderService(repository=OrderRepository(session=db)).get_order(user=user)


@orders_routers.post('/{product_id}', status_code=status.HTTP_201_CREATED)
async def add_to_cart(product_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(GetUser(token_service=TokenService()))):
    return await OrderService(repository=OrderRepository(session=db)).add_to_cart(user=user, product_id=product_id)


@orders_routers.delete('/{order_product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_cart(order_product_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(GetUser(token_service=TokenService()))):
    await OrderService(repository=OrderRepository(session=db)).remove_from_cart(user=user, order_product_id=order_product_id)
    return {'detail': 'Order product was deleted from cart'}




from users.models import User
from .interfaces.repositories_interface import OrderRepositoryInterface
from .schemas import CreateAddressSchema


class OrderService:
    def __init__(self, repository: OrderRepositoryInterface):
        self._repository = repository

    async def get_order(self, user: User):
        return await self._repository.get_order_products(user=user)

    async def add_to_cart(self, user: User, product_id: int):
        return await self._repository.add_to_cart(product_id=product_id, user=user)

    async def remove_from_cart(self, user: User, order_product_id: int):
        return await self._repository.remove_from_cart(order_product_id=order_product_id, user=user)

    async def payment_order(self, user: User, shipping_address: CreateAddressSchema):
        return await self._repository.add_shipping_address_and_payment(shipping_address=shipping_address.dict(exclude_none=True), user=user)
from abc import ABC, abstractmethod
from users.models import User


class OrderRepositoryInterface(ABC):

    @abstractmethod
    async def get_order_products(self, user: User): pass

    @abstractmethod
    async def add_to_cart(self, product_id: int, user: User): pass

    @abstractmethod
    async def remove_from_cart(self, order_product_id: int, user: User): pass

    @abstractmethod
    async def add_shipping_address_and_payment(self, shipping_address: dict, user: User): pass

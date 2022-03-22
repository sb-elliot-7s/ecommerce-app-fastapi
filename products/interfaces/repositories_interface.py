from abc import ABC, abstractmethod
from typing import Optional
from ..models import Product
from users.models import User
from fastapi import UploadFile
from image_service.interfaces.service import ImageServiceInterface


class RepositoriesInterface(ABC):

    @abstractmethod
    async def get_all_products(self, limit: Optional[int], offset: Optional[int], query_data: dict,
                               price_query_data: dict) -> list[Product]: pass

    @abstractmethod
    async def get_detail_product(self, product_id: int) -> Product: pass

    @abstractmethod
    async def create_product(self, product_data: dict, user: User,
                             images: Optional[list[UploadFile]], image_service: ImageServiceInterface, host: str): pass

    @abstractmethod
    async def delete_product(self, product_id: int, user: User, image_service: ImageServiceInterface): pass

    @abstractmethod
    async def update_product(self, product_id: int, updated_data: dict,
                             images: Optional[list[UploadFile]], user: User, image_service: ImageServiceInterface, host: str): pass

    @abstractmethod
    async def get_favorite_products(
        self, offset: int, limit: int, user: User): pass

    @abstractmethod
    async def add_product_to_favorites(self, product_id: int, user: User): pass

    @abstractmethod
    async def remove_product_from_favorites(
        self, favorite_id: int, user: User): pass

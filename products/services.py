from fastapi import HTTPException, UploadFile, status
from image_service.interfaces.service import ImageServiceInterface
from users.models import User
from .interfaces.repositories_interface import RepositoriesInterface
from typing import Optional
from configs import IMAGES_DIR
from .schemas import CreateOrUpdateProductSchema, QueryPriceSchema, QueryProductSchema


class ProductServices:
    def __init__(self, repository: RepositoriesInterface):
        self._repository = repository

    async def get_all_products(self, limit: Optional[int], offset: Optional[int],
                               query_data: QueryProductSchema, price_query: QueryPriceSchema):
        return await self._repository.get_all_products(limit=limit, offset=offset,
                                                       query_data=query_data.dict(exclude_none=True), price_query_data=price_query.dict(exclude_none=True))

    async def get_detail_product(self, product_id: int):
        return await self._repository.get_detail_product(product_id=product_id)

    async def delete_product(self, product_id: int, user: User, image_service: ImageServiceInterface):
        await self._repository.delete_product(product_id=product_id, user=user, image_service=image_service)

    async def create_product(self, data: CreateOrUpdateProductSchema,
                             images: Optional[list[UploadFile]], user: User, image_service: ImageServiceInterface, host: str):
        created_data = data.dict(exclude_none=True)
        return await self._repository.create_product(product_data=created_data, user=user, images=images, image_service=image_service, host=host)

    async def update_product(self, product_id: int, data: CreateOrUpdateProductSchema, user: User,
                             images: Optional[list[UploadFile]], image_service: ImageServiceInterface, host: str):
        updated_data = data.dict(exclude_none=True)
        result, product = await self._repository.update_product(product_id=product_id, user=user, updated_data=updated_data,
                                                                images=images, image_service=image_service, host=host)
        if not result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='You cannot update this listing')
        return product

    async def get_favorites_product(self, limit: Optional[int], offset: Optional[int], user: User):
        return await self._repository.get_favorite_products(offset=offset, limit=limit, user=user)

    async def add_product_to_favorites(self, product_id: int, user: User):
        return await self._repository.add_product_to_favorites(product_id=product_id, user=user)

    async def remove_product_from_favorites(self, favorite_id: int, user: User):
        return await self._repository.remove_product_from_favorites(favorite_id=favorite_id, user=user)

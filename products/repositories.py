from typing import Optional
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from users.models import User
from .interfaces.repositories_interface import RepositoriesInterface
from .models import Favorite, Image, Product
from fastapi import HTTPException, UploadFile, status
from image_service.interfaces.service import ImageServiceInterface
import uuid
from .query_filter import QueryService
from .schemas import FavoriteSchema


class ProductsRepository(RepositoriesInterface):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def _get_product(self, product_id: int) -> Product:
        result = await self._session.execute(select(Product).where(Product.id == product_id))
        if not (product := result.scalars().first()):
            raise HTTPException(detail='Product not found', status_code=status.HTTP_404_NOT_FOUND)
        return product

    @staticmethod
    async def _filter_result(stmt, data: dict, price_data: dict):
        query_service = QueryService()
        stmt = await query_service.price_compare(stmt=stmt, price_data=price_data, column=Product.price)
        stmt = await query_service.filtered(stmt=stmt, data=data, key='gender', column=Product.gender)
        stmt = await query_service.filtered(stmt=stmt, data=data, key='color', column=Product.color)
        stmt = await query_service.filtered(stmt=stmt, data=data, key='category', column=Product.category)
        stmt = await query_service.filtered(stmt=stmt, data=data, key='brand', column=Product.brand)
        stmt = await query_service.filtered(stmt=stmt, data=data, key='material', column=Product.material)
        return stmt

    async def get_all_products(self, limit: Optional[int], offset: Optional[int], query_data: dict, price_query_data: dict):
        stmt = select(Product).where(Product.is_active)
        stmt = await self._filter_result(stmt=stmt, data=query_data, price_data=price_query_data)
        result = await self._session.execute(stmt.limit(limit).offset(offset).order_by(Product.updated.desc()))
        return result.scalars().unique().all()

    async def get_detail_product(self, product_id: int) -> Product:
        return await self._get_product(product_id=product_id)

    async def _save_image(self, product_id: int, images: Optional[list[UploadFile]], image_service: ImageServiceInterface, host: str):
        if images:
            for image in images:
                image_name = f'{uuid.uuid4()}-{image.filename}'
                await image_service.write_image(imagename=image_name, image=image)
                await self._session.execute(insert(Image).values(photo=f'{host}/{image_name}', product_id=product_id))

    async def create_product(self, product_data: dict, user: User, images: Optional[list[UploadFile]], image_service: ImageServiceInterface,
                             host: str):
        result = await self._session.execute(insert(Product).values(**product_data, user_id=user.id).returning(Product.id))
        product_id = result.scalars().first()
        await self._save_image(product_id=product_id, images=images, image_service=image_service, host=host)
        await self._session.commit()
        product_result = await self._session.execute(select(Product).where(Product.id == product_id))
        return product_result.scalars().first()

    async def update_product(self, product_id: int, updated_data: dict, images: Optional[list[UploadFile]], user: User,
                             image_service: ImageServiceInterface, host: str):
        if (product := await self._get_product(product_id=product_id)) and product.user_id != user.id:
            return False, None
        print(updated_data)
        await self._save_image(product_id=product.id, images=images, image_service=image_service, host=host)
        _ = await self._session.execute(update(Product)
                                        .where(Product.id == product.id)
                                        .values(**updated_data)
                                        .returning(Product))
        await self._session.commit()
        await self._session.refresh(product)
        return True, product

    async def delete_product(self, product_id: int, user: User, image_service: ImageServiceInterface):
        product = await self._get_product(product_id=product_id)
        if product.user_id != user.id:
            raise HTTPException(detail='You cannot delete this product', status_code=status.HTTP_400_BAD_REQUEST)
        images = product.images
        if images:
            for image in images:
                await image_service.delete_image(imagename=image.photo.split('/')[-1])
        await self._session.delete(product)
        await self._session.commit()

    async def get_favorite_products(self, offset: int, limit: int, user: User):
        result = await self._session.execute(select(Product)
                                             .join(Favorite)
                                             .where(Favorite.user_id == user.id, Favorite.is_favorite).offset(offset).limit(limit)
                                             .order_by(Product.updated.desc()))
        products: list[Product] = result.scalars().unique().all()
        return FavoriteSchema(user_id=user.id, products=products)

    async def add_product_to_favorites(self, product_id: int, user: User):
        product = await self._get_product(product_id=product_id)
        result = await self._session.execute(insert(Favorite)
                                             .values(product_id=product.id, user_id=user.id, is_favorite=True)
                                             .returning(Favorite.id))
        await self._session.commit()
        if not result.is_insert:
            return False
        return True

    async def remove_product_from_favorites(self, favorite_id: int, user: User):
        result = await self._session.execute(select(Favorite).where(Favorite.id == favorite_id, Favorite.user_id == user.id))
        if not (fav := result.scalars().first()):
            raise HTTPException(detail='Favorite products not found', status_code=status.HTTP_404_NOT_FOUND)
        await self._session.delete(fav)
        await self._session.commit()

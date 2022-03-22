from fastapi import APIRouter, Depends, File, Form, status, UploadFile, responses
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from image_service.image_service import ImageService
from permissions import GetUser
from users.models import User
from users.token_service import TokenService
from .services import ProductServices
from .repositories import ProductsRepository
from typing import Optional
from configs import IMAGES_DIR, get_settings
from .schemas import CreateOrUpdateProductSchema, ProductSchema, QueryPriceSchema, QueryProductSchema, FavoriteSchema


products_routers = APIRouter(prefix='/products', tags=['products'])


@products_routers.get('/favorites', status_code=status.HTTP_200_OK, response_model=FavoriteSchema)
async def get_all_favorites_products(db: AsyncSession = Depends(get_db),
                                     limit: Optional[int] = 30, offset: Optional[int] = 0,
                                     user: User = Depends(GetUser(token_service=TokenService()))):
    return await ProductServices(repository=ProductsRepository(session=db)).get_favorites_product(limit=limit, offset=offset, user=user)


@products_routers.get('/', status_code=status.HTTP_200_OK, response_model=list[ProductSchema])
async def get_all_products(db: AsyncSession = Depends(get_db), limit: Optional[int] = 30, offset: Optional[int] = 0,
                           product_query: QueryProductSchema = Depends(QueryProductSchema.as_query),
                           price_query: QueryPriceSchema = Depends(QueryPriceSchema.as_query)):
    return await ProductServices(repository=ProductsRepository(session=db)).get_all_products(limit=limit, offset=offset, query_data=product_query, price_query=price_query)


@products_routers.get('/{product_id}', status_code=status.HTTP_200_OK, response_model=ProductSchema)
async def get_detail_product(product_id: int, db: AsyncSession = Depends(get_db)):
    return await ProductServices(repository=ProductsRepository(session=db)).get_detail_product(product_id=product_id)


@products_routers.post('/', status_code=status.HTTP_201_CREATED, response_model=ProductSchema)
async def create_product(data: CreateOrUpdateProductSchema = Depends(CreateOrUpdateProductSchema.as_form),
                         images: Optional[list[UploadFile]] = File(None),
                         db: AsyncSession = Depends(get_db),
                         user: User = Depends(GetUser(token_service=TokenService()).get_admin_user)):
    return await ProductServices(repository=ProductsRepository(session=db)) \
        .create_product(data=data, images=images, user=user, image_service=ImageService(path=IMAGES_DIR), host=get_settings().image_host)


@products_routers.put('/{product_id}')
async def update_product(product_id: int,
                         updated_data: CreateOrUpdateProductSchema = Depends(CreateOrUpdateProductSchema.as_form),
                         images: Optional[list[UploadFile]] = Form(None),
                         db: AsyncSession = Depends(get_db),
                         user: User = Depends(GetUser(token_service=TokenService()).get_admin_user)):
    return await ProductServices(repository=ProductsRepository(session=db))\
        .update_product(product_id=product_id, data=updated_data, user=user, images=images, image_service=ImageService(path=IMAGES_DIR), host=get_settings().image_host)


@products_routers.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db),
                         user: User = Depends(GetUser(token_service=TokenService()).get_admin_user)):
    await ProductServices(repository=ProductsRepository(session=db)) \
        .delete_product(product_id=product_id, user=user, image_service=ImageService(path=IMAGES_DIR))
    return {'detail':'Product was deleted'}


@products_routers.post('/favorites/{product_id}', status_code=status.HTTP_201_CREATED)
async def add_to_favorites(product_id: int, db: AsyncSession = Depends(get_db),
                           user: User = Depends(GetUser(token_service=TokenService()))):
    result = await ProductServices(repository=ProductsRepository(session=db)).add_product_to_favorites(product_id=product_id, user=user)
    if result:
        return {'detail': 'Product has been added to favorites'}


@products_routers.delete('/favorites/{favorite_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_from_favorites(favorite_id: int, db: AsyncSession = Depends(get_db),
                                user: User = Depends(GetUser(token_service=TokenService()))):
    await ProductServices(repository=ProductsRepository(session=db)).remove_product_from_favorites(favorite_id=favorite_id, user=user)
    return {'detail': 'Favorite product was deleted'}



from fastapi import APIRouter, status, Depends
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from .services import AuthServices, ProfileUserServices
from .repositories import AuthRepository, ProfileUserRepository
from database import get_db
from .schemas import CreateUserSchema, Token, UserSchema, UpdateUserSchema
from .password_service import PasswordService
from .token_service import TokenService
from permissions import GetUser
from .models import User

users_routers = APIRouter(prefix='/users', tags=['users'])


# auth controllers

@users_routers.post('/login', status_code=status.HTTP_200_OK, response_model=Token)
async def login(user_data: CreateUserSchema = Depends(CreateUserSchema.as_form), db: AsyncSession = Depends(get_db)):
    return await AuthServices(repository=AuthRepository(session=db),
                              password_service=PasswordService(context=CryptContext(schemes=['bcrypt'], deprecated='auto'))) \
        .login(**user_data.dict(exclude={'is_admin'}), token_service=TokenService())


@users_routers.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UserSchema)
async def signup(user_data: CreateUserSchema, db: AsyncSession = Depends(get_db)):
    return await AuthServices(repository=AuthRepository(session=db),
                              password_service=PasswordService(context=CryptContext(schemes=["bcrypt"], deprecated="auto"))) \
        .signup(**user_data.dict(exclude_none=True))


# profile controllers

@users_routers.get('/me', status_code=status.HTTP_200_OK, response_model=UserSchema)
async def get_user_profile(db: AsyncSession = Depends(get_db), user: User = Depends(GetUser(token_service=TokenService()))):
    return await ProfileUserServices(repository=ProfileUserRepository(session=db)).get_user(user=user)


@users_routers.put('/', status_code=status.HTTP_200_OK, response_model=UserSchema)
async def update_profile(updated_data: UpdateUserSchema, db: AsyncSession = Depends(get_db), user: User = Depends(GetUser(token_service=TokenService()))):
    return await ProfileUserServices(repository=ProfileUserRepository(session=db)).update_user(user=user, updated_data=updated_data)


@users_routers.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(db: AsyncSession = Depends(get_db), user: User = Depends(GetUser(token_service=TokenService()))):
    return await ProfileUserServices(repository=ProfileUserRepository(session=db)).delete_user(user=user)

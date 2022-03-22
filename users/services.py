from typing import Optional
from .models import User
from .interfaces.repositories_interface import AuthRepositoryInterface, ProfileRepositoryInterface
from .interfaces.jwt_interface import JWTInterface
from .interfaces.password_service_interface import PasswordServiceInterface
from configs import get_settings
from fastapi import HTTPException, status
from .schemas import Token, UpdateUserSchema


class AuthServices:

    def __init__(self, repository: AuthRepositoryInterface, password_service: PasswordServiceInterface):
        self._repository = repository
        self._password_service = password_service
        self._settings = get_settings()

    async def _authenticate(self, email: str, password: str):
        if not (user := await self._repository.get_user_by_email(email=email)) \
                or not await self._password_service.verify_password(plain_password=password, hashed_password=user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect email or password')
        return user

    async def login(self, email: str, password: str, token_service: JWTInterface) -> Token:
        user = await self._authenticate(email=email, password=password)
        subject = {'sub': user.email}
        access_token = await token_service.create_token_for_user(data=subject, secret_key=self._settings.secret_key,
                                                                 exp_time=self._settings.access_token_expire_minutes,
                                                                 algorithm=self._settings.algorithm)
        return Token(token=access_token, token_type='bearer')

    async def signup(self, email: str, password: str, is_admin: Optional[bool]):
        if await self._repository.get_user_by_email(email=email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User with this email exists')
        hashed_password = await self._password_service.get_hashed_password(password=password)
        return await self._repository.save_user(email=email, password=hashed_password, is_admin=is_admin)



class ProfileUserServices:

    def __init__(self, repository: ProfileRepositoryInterface):
        self._repository = repository

    async def get_user(self, user: User):
        return await self._repository.get_user(user=user)

    async def update_user(self, user: User, updated_data: UpdateUserSchema):
        data = updated_data.dict(exclude_none=True)
        return await self._repository.update_user(user=user, updated_data=data)

    async def delete_user(self, user: User):
        return await self._repository.delete_user(user=user)
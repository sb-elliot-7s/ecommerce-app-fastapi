from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, insert, update
from .interfaces.repositories_interface import AuthRepositoryInterface, ProfileRepositoryInterface
from .models import User


class AuthRepository(AuthRepositoryInterface):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def save_user(self, email: str, password: str, is_admin: bool = False):
        result = await self._session.execute(insert(User).values(email=email, password=password, is_admin=is_admin).returning(User))
        await self._session.commit()
        return result.first()

    async def get_user_by_email(self, email: str) -> User:
        result = await self._session.execute(select(User).where(User.email ==email))
        return result.scalars().first()


class ProfileUserRepository(ProfileRepositoryInterface):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_user(self, user: User) -> User:
        result = await self._session.execute(select(User).where(User.id == user.id))
        return result.scalars().first()

    async def update_user(self, user: User, updated_data: dict):
        result = await self._session.execute(update(User).where(User.id == user.id).values(**updated_data).returning(User))
        await self._session.commit()
        return result.first()

    async def delete_user(self, user: User):
        result = await self._session.execute(delete(User).where(User.id == user.id))
        await self._session.commit()

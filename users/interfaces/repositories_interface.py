from abc import ABC, abstractmethod
from typing import Optional
from ..models import User


class AuthRepositoryInterface(ABC):
    @abstractmethod
    async def save_user(self, email: str, password: str, is_admin: bool = False): pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User: pass


class ProfileRepositoryInterface(ABC):

    @abstractmethod
    async def get_user(self, user: User) -> User: pass

    @abstractmethod
    async def update_user(self, user: User, updated_data: dict): pass

    @abstractmethod
    async def delete_user(self, user: User): pass

from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from configs import get_settings
from users.interfaces.jwt_interface import JWTInterface
from sqlalchemy import select
from users.models import User


class GetUser:
    OAUTH_TOKEN = OAuth2PasswordBearer(tokenUrl='/login')

    def __init__(self, token_service: JWTInterface):
        self._token_service = token_service
        self._settings = get_settings()

    async def _decode_token(self, token: str) -> str:
        payload: dict = await self._token_service.decode_token(token=token, secret_key=self._settings.secret_key, algorithm=self._settings.algorithm)
        return payload.get('sub')  # return email

    async def __call__(self, token: str = Depends(OAUTH_TOKEN), session: AsyncSession = Depends(get_db)):
        email = await self._decode_token(token=token)
        result = await session.execute(select(User).where(User.email == email, User.is_active))
        return result.scalars().first()

    async def get_admin_user(self, token: str = Depends(OAUTH_TOKEN), session: AsyncSession = Depends(get_db)):
        email = await self._decode_token(token=token)
        result = await session.execute(select(User).where(User.email == email, User.is_active, User.is_admin))
        if not (user :=  result.scalars().first()):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are not an admin")
        return user

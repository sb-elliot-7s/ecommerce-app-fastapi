from typing import Optional

from .interfaces.jwt_interface import JWTInterface
from jose import jwt, JWTError
from fastapi import HTTPException, status
from datetime import datetime, timedelta


class TokenService(JWTInterface):

    async def create_token_for_user(self, data: dict, secret_key: str, exp_time: Optional[int], algorithm: Optional[str]):
        payloads = data.copy()
        token_exp = datetime.utcnow() + timedelta(minutes=exp_time) if exp_time \
            else datetime.utcnow() + timedelta(minutes=10)
        payloads.update({'iat': datetime.utcnow(), 'exp': token_exp})
        return jwt.encode(claims=payloads, key=secret_key, algorithm=algorithm)

    async def decode_token(self, token: str, secret_key: str, algorithm: Optional[str]):
        try:
            payload = jwt.decode(token=token, key=secret_key, algorithms=algorithm)
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='not validate credentials', headers={"WWW-Authenticate": "Bearer"})
        return payload

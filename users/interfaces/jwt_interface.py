from abc import ABC, abstractmethod
from typing import Optional


class JWTInterface(ABC):

    @abstractmethod
    async def create_token_for_user(self, data: dict, secret_key: str, exp_time: Optional[int],
                                    algorithm: Optional[str]): pass

    @abstractmethod
    async def decode_token(self, token: str, secret_key: str, algorithm: Optional[str]): pass

from abc import ABC, abstractmethod

from fastapi import UploadFile


class ImageServiceInterface(ABC):

    @abstractmethod
    async def read_image(self, imagename:str, **kwargs):...

    @abstractmethod
    async def write_image(self, imagename: str, image: UploadFile, **kwargs):...

    @abstractmethod
    async def delete_image(self, imagename: str, **kwargs):...
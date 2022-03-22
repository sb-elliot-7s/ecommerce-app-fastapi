from pathlib import Path
from fastapi import UploadFile
from .interfaces.service import ImageServiceInterface
import aiofiles
from aiofiles import os as _os


class ImageService(ImageServiceInterface):

    def __init__(self, path: str) -> None:
        self._path = path

    async def read_image(self, imagename: str, **kwargs):
        try:
            async with aiofiles.open(f'{self._path}/{imagename}', mode='rb') as file:
                image = await file.read()
            return image
        except FileNotFoundError as error:
            raise FileNotFoundError(error)


    async def write_image(self, imagename: str, image: UploadFile, **kwargs):
        async with aiofiles.open(f'{self._path}/{imagename}', mode='wb') as file:
            content = await image.read()
            await file.write(content)

    async def delete_image(self, imagename: str, **kwargs):
        try:
            await _os.remove(f'{self._path}/{imagename}')
        except FileNotFoundError as error:
            raise FileNotFoundError(error)

        
import asyncio
import logging
from dataclasses import dataclass
from os import getenv

from httpx import AsyncClient
from dotenv import load_dotenv

from scrapper.entities import Product

load_dotenv()
from cloudinary import uploader, CloudinaryImage


@dataclass
class Image:
    raw: bytearray


@dataclass
class ImageStoreRequest:
    download_path: str
    filename: str


class ImageDownloader:
    def __init__(self, image_root_url: str):
        self._image_root_url = image_root_url

    async def download(self, path: str) -> Image:
        url = '{}{}'.format(self._image_root_url, path)
        async with AsyncClient() as client:
            r = await client.get(url)

        return Image(r.content)


class ImageUploader:
    def __init__(self, bucket_name: str):
        self._bucket_name = bucket_name
        self._cloudinary_url = getenv('CLOUDINARY_URL')
        if self._cloudinary_url is None:
            raise RuntimeError('Define CLOUDINARY_URL if you want to use Image Uploader')

    async def upload(self, image: Image, filename: str, target_slug: str):
        file_id = str(uploader.upload_image(
            image.raw,
            public_id=filename,
            folder='{}/{}'.format(self._bucket_name, target_slug),
            secured=True,
        ))

        return CloudinaryImage(file_id).build_url(width=800, crop='pad', gravity='center', aspect_ratio='4:3')


class ImageStorage:
    def __init__(self, image_root_url: str, bucket_name: str):
        self._downloader = ImageDownloader(image_root_url)
        self._uploader = ImageUploader(bucket_name)

    async def store_images(self, target_slug: str, products: list[Product]):
        logging.info('Storing images for {}'.format(target_slug))

        tasks = [asyncio.create_task(self.store(target_slug, p)) for p in products]
        await asyncio.gather(*tasks)

    async def store(self, target_slug: str, product: Product):
        image = await self._downloader.download(product.image_path)
        url = await self._uploader.upload(image, product.slug, target_slug)

        product.url = url
        product.stored = True
        product.save()

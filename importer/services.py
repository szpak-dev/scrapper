import asyncio
from pathlib import Path

import httpx
from slugify import slugify


class ImageDownloader:
    def __init__(self, cwd: str, root_url: str):
        self.cwd = cwd
        self.root_url = root_url

    async def download(self, path: str):
        url = self.root_url + path

        async with httpx.AsyncClient() as client:
            r = await client.get(url)

        return r.content

    async def save_to_drive(self, filename: str, image: bytearray):
        Path('{}/images/{}'.format(self.cwd, filename)).write_bytes(image)


class Importer:
    def __init__(self, image_downloader: ImageDownloader, manufacturer: Manufacturer, scrap_slug: str):
        self.image_downloader = image_downloader
        self.manufacturer = manufacturer
        self.crawl = Crawl.get_latest(manufacturer, scrap_slug)
        self.categories_by_slug = {}

    def import_categories(self):
        for resource in self.crawl.resources.where(Resource.type == 'category'):
            page = Page('', '', resource.html)
            name = page.query_html_one('h1', 'text')

            category = Category.add(self.manufacturer, name)
            self.categories_by_slug[category.slug] = category

    def import_products(self):
        for resource in self.crawl.resources.where(Resource.type == 'product'):
            page = Page('', '', resource.html)
            category_name = page.query_html_one('.AlsoBrowseThisCat a', 'text')
            category_slug = slugify(category_name)

            name = page.query_html_one('.ProductDetails h1', 'text')
            image_path = page.query_html_one('#ProductImages ul li:first-child img', 'data-src-l')

            category = self.categories_by_slug[category_slug]
            category.add_product(name, 'description', image_path)

    async def download_images(self):
        tasks = []
        for product in Product.select().where(Product.local_image_path == ''):
            task = asyncio.create_task(self._store_image(product))
            tasks.append(task)

        await asyncio.gather(*tasks)

    async def _store_image(self, product: Product):
        filename = '{}.jpg'.format(product.slug)
        image_bytes = await self.image_downloader.download(product.image_path)
        await self.image_downloader.save_to_drive(filename, image_bytes)
        product.local_image_path = filename
        product.save_documents()
import click
import asyncio
from os import getcwd

from models.manufacturer import Manufacturer
from importer.services import ImageDownloader, Importer


@click.group()
def cli():
    pass


@cli.command()
def preview():
    pass


@cli.command()
def run():
    manufacturer = Manufacturer.get_by_id(Manufacturer.slug == 'marttiini')
    image_downloader = ImageDownloader(getcwd(), 'https://marttiini.fi')

    importer = Importer(image_downloader, manufacturer, 'default')
    # importer.import_categories()
    # importer.import_products()

    asyncio.run(importer.download_images())


if __name__ == '__main__':
    cli()

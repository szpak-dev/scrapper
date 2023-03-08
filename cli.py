import click
import asyncio
import yaml
import logging

from crawler.services import Crawler, reset_crawler, get_latest_crawl
from manufacturer.services import install_manufacturers, reset_manufacturers, get_manufacturer_by_slug
from scrapper.services import reset_scrapper


@click.group()
def cli():
    pass


@cli.command()
@click.option('--module', required=True, help='Module name to install')
def install(module: str):
    if module == 'manufacturer':
        with open('./manufacturers.yaml') as file:
            return install_manufacturers(yaml.load(file, Loader=yaml.FullLoader))

    logging.info('Nothing to install')


@cli.command()
@click.option('--module', required=True, help='Module name to reset')
def reset(module: str):
    if module == 'manufacturer':
        return reset_manufacturers()

    if module == 'crawler':
        return reset_crawler()

    if module == 'scrapper':
        return reset_scrapper()

    logging.info('Nothing to reset')


@cli.command()
@click.option('--manufacturer', required=True, help='Manufacturer slug')
@click.option('--config', required=True, help='Manufacturer Crawl slug')
def crawl(manufacturer: str, config: str):
    manufacturer = get_manufacturer_by_slug(manufacturer)
    config = manufacturer.config_by_slug(config)
    crawler = Crawler(config)
    asyncio.run(crawler.crawl())


@cli.command()
@click.option('--manufacturer', required=True, help='Manufacturer slug')
def scrap(manufacturer: str):
    pass
    # crawl = get_latest_crawl(manufacturer)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    cli()

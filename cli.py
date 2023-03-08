import click
import asyncio
import yaml
import logging

from crawler.services import Crawler, reset_crawler, get_latest_crawl
from manufacturer.entities import Manufacturer
from manufacturer.services import install_manufacturers, reset_manufacturers, get_manufacturer_by_slug
from scrapper.services import Scrapper, reset_scrapper


def get_manufacturer(slug: str) -> Manufacturer:
    try:
        return get_manufacturer_by_slug(slug)
    except RuntimeError as e:
        logging.error(str(e))
        exit(1)


def run_option(key: str, choices: dict[str, callable]) -> None:
    if key not in choices.keys():
        return logging.warning('Nothing to reset')

    choices[key]()


@click.group()
def cli():
    pass


@cli.command()
@click.option('--module', required=True, help='Module name to install')
def install(module: str):
    if module == 'manufacturer':
        with open('./manufacturers.yaml') as file:
            return install_manufacturers(yaml.load(file, Loader=yaml.FullLoader))

    logging.warning('Nothing to install')


@cli.command()
@click.option('--module', required=True, help='Module name to reset')
def reset(module: str):
    run_option(module, {
        'manufacturer': reset_manufacturers,
        'crawler': reset_crawler,
        'scrapper': reset_scrapper,
    })


@cli.command()
@click.option('--manufacturer', required=True, help='Manufacturer slug')
@click.option('--config', required=True, help='Manufacturer Crawl slug')
def crawl(manufacturer: str, config: str):
    manufacturer = get_manufacturer(manufacturer)
    config = manufacturer.config_by_slug(config)
    asyncio.run(Crawler(config).crawl())


@cli.command()
@click.option('--manufacturer', required=True, help='Manufacturer slug')
def scrap(manufacturer: str):
    manufacturer = get_manufacturer(manufacturer)
    latest_crawl = get_latest_crawl(manufacturer.slug)
    Scrapper(manufacturer.slug, manufacturer.scrap_configs).scrap(latest_crawl)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    cli()

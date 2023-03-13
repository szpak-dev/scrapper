import click
import asyncio
import yaml
import logging

from crawler.services import Crawler, reset_crawler, clear_crawler, get_latest_crawl
from scrapper.images import ImageStorage
from target.entities import Target
from target.services import install_targets, reset_targets, get_target_by_slug
from scrapper.services import Scrapper, reset_scrapper, clear_scrapper, get_products_without_stored_images


def get_target(slug: str) -> Target:
    try:
        return get_target_by_slug(slug)
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
    if module == 'target':
        with open('./targets.yaml') as file:
            return install_targets(yaml.load(file, Loader=yaml.FullLoader))

    logging.warning('Nothing to install')


@cli.command()
@click.option('--module', required=True, help='Module name to reset')
def reset(module: str):
    run_option(module, {
        'target': reset_targets,
        'crawler': reset_crawler,
        'scrapper': reset_scrapper,
    })


@cli.command()
@click.option('--module', required=True, help='Module slug')
@click.option('--target', required=True, help='Target slug to clear')
def clear(module: str, target: str):
    if module == 'crawler':
        return clear_crawler(target)

    if module == 'scrapper':
        return clear_scrapper(target)

    logging.warning('Nothing to clear')


@cli.command()
@click.option('--target', required=True, help='Target slug')
@click.option('--config', required=True, help='Target Crawl config slug')
def crawl(target: str, config: str):
    target = get_target(target)
    config = target.config_by_slug(config)
    asyncio.run(Crawler(config).crawl())


@cli.command()
@click.option('--target', required=True, help='Target slug')
def scrap(target: str):
    target = get_target(target)
    latest_crawl = get_latest_crawl(target.slug)
    Scrapper(target.slug, target.scrap_configs).scrap(latest_crawl)


@cli.command()
@click.option('--target', required=True, help='Target slug')
@click.option('--media', required=True, help='Media type to be downloaded')
def download(target: str, media: str):
    target = get_target(target)
    if media == 'image':
        products = get_products_without_stored_images()
        if len(products) == 0:
            return logging.warning('Nothing to download. Make sure you made at least one scrap')

        storage = ImageStorage(target.images_root_url, 'tomjan')
        asyncio.run(storage.store_images(target, products))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    cli()

from manufacturer.entities import Manufacturer, CrawlConfig, CrawlStep
from _shared.base_model import db


def reset_manufacturers():
    db.drop_tables([CrawlStep, CrawlConfig, Manufacturer])
    db.create_tables([Manufacturer, CrawlConfig, CrawlStep])
    print('Manufacturers tables reset')


def install_manufacturers(manufacturers: dict):
    for slug in manufacturers:
        if Manufacturer.get_or_none(Manufacturer.slug == slug):
            print('[Manufacturers] Manufacturer <{}> already exists, skipping'.format(slug))
            continue

        m = manufacturers[slug]
        print('[Manufacturers] Installing {}'.format(m['name']))

        manufacturer = Manufacturer.create(slug=slug, name=m['name'], logo_url=m['logo_url'])
        config = CrawlConfig.create(manufacturer=manufacturer, slug='default', root_url=m['root_url'])
        config.add_steps(m['steps'])


def get_manufacturer_by_slug(slug: str):
    manufacturer = Manufacturer.get_or_none(Manufacturer.slug == slug)
    if manufacturer is None:
        raise RuntimeError('No Manufacturer with slug: {}'.format(slug))

    return manufacturer

import logging
from manufacturer.entities import Manufacturer, CrawlConfig, CrawlStep, ScrapConfig, ScrapProperty
from _shared.base_model import db


def reset_manufacturers():
    db.drop_tables([ScrapProperty, ScrapConfig, CrawlStep, CrawlConfig, Manufacturer])
    db.create_tables([Manufacturer, CrawlConfig, CrawlStep, ScrapConfig, ScrapProperty])
    logging.info('Manufacturers tables reset')


def install_manufacturers(manufacturers: dict):
    for slug in manufacturers:
        if Manufacturer.get_or_none(Manufacturer.slug == slug):
            logging.warning('[Manufacturers] Manufacturer <{}> already exists, skipping'.format(slug))
            continue

        m = manufacturers[slug]
        logging.info('[Manufacturers] Installing {}'.format(m['name']))

        manufacturer = Manufacturer.create(slug=slug, name=m['name'], logo_url=m['logo_url'])
        config = CrawlConfig.create(manufacturer=manufacturer, slug='default', root_url=m['root_url'])
        config.add_steps(m['steps'])

        for resource_label in m['scrap']:
            scrap_config = ScrapConfig.create(manufacturer=manufacturer, resource_label=resource_label)
            for property_name in m['scrap'][resource_label]:
                css_query, node_name = m['scrap'][resource_label][property_name]
                scrap_config.add_property(property_name, css_query, node_name)


def get_manufacturer_by_slug(slug: str):
    manufacturer = Manufacturer.get_or_none(Manufacturer.slug == slug)
    if manufacturer is None:
        raise RuntimeError('No Manufacturer with slug: {}'.format(slug))

    return manufacturer

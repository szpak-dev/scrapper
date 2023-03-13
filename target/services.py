import logging
from target.entities import Target, CrawlConfig, CrawlStep, ScrapConfig, ScrapProperty
from _shared.base_model import db


def reset_targets():
    db.drop_tables([ScrapProperty, ScrapConfig, CrawlStep, CrawlConfig, Target])
    db.create_tables([Target, CrawlConfig, CrawlStep, ScrapConfig, ScrapProperty])
    logging.info('Target tables reset')


def install_targets(targets: dict):
    for slug in targets:
        if Target.by_slug(slug):
            logging.warning('Target <{}> already exists, skipping'.format(slug))
            continue

        new_target = targets[slug]
        logging.info('Installing new Target: {}'.format(new_target['name']))

        target = Target.add(
            name=new_target['name'],
            logo_url=new_target['logo_url'],
            images_root_url=new_target['images_root_url']
        )

        config = target.add_config(name='Default', root_url=new_target['root_url'])
        config.add_steps(new_target['steps'])

        for resource_label in new_target['scrap']:
            scrap_config = target.add_scrap_config(resource_label=resource_label)
            for property_name in new_target['scrap'][resource_label]:
                css_query, node_name = new_target['scrap'][resource_label][property_name]
                scrap_config.add_property(property_name, css_query, node_name)


def get_target_by_slug(slug: str):
    target = Target.by_slug(slug)
    if target is None:
        raise RuntimeError('No Target with slug: {}'.format(slug))

    return target

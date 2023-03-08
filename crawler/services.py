import logging

from crawler.config import CrawlConfig
from crawler.entities import Crawl, Resource, Link
from _shared.base_model import db
from crawler.step_handler import StepHandlerFactory


def reset_crawler():
    db.drop_tables([Link, Resource, Crawl])
    db.create_tables([Crawl, Resource, Link])
    logging.info('Crawler tables reset')


def get_latest_crawl(manufacturer_slug: str) -> Crawl:
    return Crawl.get_latest(manufacturer_slug)


class Crawler:
    def __init__(self, config: CrawlConfig):
        self.config = config
        self.manufacturer_slug = str(config.manufacturer)

    async def crawl(self):
        crawl = Crawl.create(manufacturer_slug=self.manufacturer_slug)
        step_handler_factory = StepHandlerFactory(self.config.root_url, crawl)

        parent_resources = []
        for step in self.config.steps:
            step_handler = step_handler_factory.create(step, parent_resources)
            parent_resources = await step_handler.save_resources()

        crawl.finish()

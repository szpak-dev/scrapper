import logging

from crawler.config import CrawlConfig
from crawler.entities import Crawl, Resource, Link
from _shared.base_model import db
from crawler.step_handler import StepHandlerFactory


def reset_crawler():
    db.drop_tables([Link, Resource, Crawl])
    db.create_tables([Crawl, Resource, Link])
    logging.info('Crawler tables reset')


def clear_crawler(target_slug: str):
    for crawl in Crawl.select().where(Crawl.target_slug == target_slug):
        crawl.delete_instance(recursive=True)

    logging.info('Crawls made by {} deleted'.format(target_slug))


def get_latest_crawl(target_slug: str) -> Crawl:
    return Crawl.get_latest(target_slug)


class Crawler:
    def __init__(self, config: CrawlConfig):
        self.config = config
        self.target_slug = str(config.target)

    async def crawl(self):
        crawl = Crawl.create(target_slug=self.target_slug)
        step_handler_factory = StepHandlerFactory(self.config.root_url, crawl)

        parent_resources = []
        for step in self.config.steps:
            step_handler = step_handler_factory.create(step, parent_resources)
            parent_resources = await step_handler.save_resources()

        crawl.finish()

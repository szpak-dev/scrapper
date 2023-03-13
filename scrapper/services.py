import logging

from _shared.base_model import db
from _shared.document import Document
from crawler.entities import Crawl
from scrapper.config import ScrapConfig
from scrapper.entities import Category, Product
from scrapper.images import ImageStoreRequest


def reset_scrapper():
    db.drop_tables([Product, Category])
    db.create_tables([Category, Product])
    logging.info('Scrapper tables reset')


def clear_scrapper(target_slug: str):
    Product.update(url="", stored=False).execute()
    logging.info('All flags and URLs cleared')


def get_products_without_stored_images() -> list[Product]:
    return Product.get_not_stored_images()


def create_scrap_config_index(cfg: list[ScrapConfig]):
    c = {}
    for config in cfg:
        c[config.resource_label] = [[cp.name, cp.css_query, cp.fetch_attr] for cp in config.properties]

    return c


class Scrapper:
    def __init__(self, target_slug: str, config: list[ScrapConfig]):
        self.target_slug = target_slug
        self.config = create_scrap_config_index(config)

    def scrap(self, crawl: Crawl):
        categories = []

        for resource in crawl.resources:
            if resource.label == 'category':
                category = self.scrap_category(resource.html, self.config[resource.label])
                for product_resource in resource.children:
                    product = self.scrap_product(product_resource.html, self.config[product_resource.label])
                    category.add_product(**product)

                categories.append(category)

        logging.info('Scrapping completed')

    def scrap_category(self, html: str, prop_queries: list[list[str, str, str]]) -> Category:
        category_data = self.query_props(Document(html), prop_queries)
        category_data['target_slug'] = self.target_slug
        return Category.add(**category_data)

    def scrap_product(self, html: str, prop_queries: list[list[str, str, str]]) -> dict:
        return self.query_props(Document(html), prop_queries)

    @staticmethod
    def query_props(document: Document, prop_queries: list[list[str, str, str]]) -> dict:
        data = {}
        for prop_query in prop_queries:
            prop_name, css_query, fetch_attr = prop_query
            data[prop_name] = document.query_html_one(css_query, fetch_attr)

        return data

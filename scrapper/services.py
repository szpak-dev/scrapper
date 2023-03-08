from _shared.base_model import db
from scrapper.entities import Category, Product


def reset_scrapper():
    db.drop_tables([Product, Category])
    db.create_tables([Category, Product])
    print('Scrapper tables reset')

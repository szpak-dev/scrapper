from peewee import ForeignKeyField, CharField, TextField
from slugify import slugify

from _shared.base_model import BaseModel


class Category(BaseModel):
    manufacturer_slug = CharField()
    name = CharField()
    slug = CharField()
    image_url = TextField(default='')

    def add_product(self, name: str, description: str, image_path: str):
        slug = slugify(name)
        existing_product = Product.get_or_none(Product.slug == slug)

        if existing_product:
            return existing_product

        return Product.create(
            category=self,
            name=name,
            slug=slug,
            description=description,
            image_path=image_path,
        )


class Product(BaseModel):
    category = ForeignKeyField(Category, backref='products')
    name = CharField()
    slug = CharField()
    description = TextField()
    image_path = TextField()
    local_image_path = TextField(default='')
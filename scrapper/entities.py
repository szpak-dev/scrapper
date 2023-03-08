from peewee import ForeignKeyField, CharField, TextField
from slugify import slugify

from _shared.base_model import BaseModel


class Category(BaseModel):
    manufacturer_slug = CharField()
    name = CharField()
    slug = CharField()
    image_url = TextField(default='')

    @classmethod
    def add(cls, manufacturer_slug: str,  name: str):
        slug = slugify(name)
        existing_category = cls.get_or_none(Category.slug == slug)

        if existing_category:
            return existing_category

        return cls.create(manufacturer_slug=manufacturer_slug, name=name, slug=slug)

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

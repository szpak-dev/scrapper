from peewee import ForeignKeyField, CharField, TextField, BooleanField
from slugify import slugify

from _shared.base_model import BaseModel


class Category(BaseModel):
    target_slug = CharField()
    name = CharField()
    slug = CharField()
    image_url = TextField(default='')

    @classmethod
    def add(cls, target_slug: str, name: str):
        slug = slugify(name)
        existing_category = cls.get_or_none(cls.slug == slug)

        if existing_category:
            return existing_category

        return cls.create(target_slug=target_slug, name=name, slug=slug)

    @classmethod
    def by_target_slug(cls, target_slug: str):
        query = cls.select()
        return [category for category in query.where(cls.target_slug == target_slug)]

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
    url = TextField(default='')
    stored = BooleanField(default=False)

    @classmethod
    def get_not_stored_images(cls):
        return cls.select().where(cls.stored == False)

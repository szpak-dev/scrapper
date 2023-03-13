from peewee import CharField, ForeignKeyField, IntegerField, TextField, BooleanField
from slugify import slugify

from _shared.base_model import BaseModel


class Target(BaseModel):
    name = CharField()
    slug = CharField()
    logo_url = TextField()
    images_root_url = TextField()

    def __str__(self):
        return self.slug

    @classmethod
    def add(cls, name: str, logo_url: str, images_root_url: str):
        return cls.create(name=name, slug=slugify(name), logo_url=logo_url, images_root_url=images_root_url)

    @classmethod
    def by_slug(cls, slug: str):
        return cls.get_or_none(cls.slug == slug)

    def add_config(self, name: str, root_url: str):
        return CrawlConfig.create(target=self, name=name, slug=slugify(name), root_url=root_url)

    def add_scrap_config(self, resource_label: str):
        return ScrapConfig.create(target=self, resource_label=resource_label)

    def config_by_slug(self, config_slug: str):
        configs = [config for config in self.configs if config.slug == config_slug]
        if len(configs) == 0:
            raise RuntimeError('Config with slug {} not found'.format(config_slug))

        return configs[-1]


class CrawlConfig(BaseModel):
    target = ForeignKeyField(Target, backref='configs')
    name = CharField()
    slug = CharField()
    root_url = TextField()

    @classmethod
    def add(cls, target: Target, name: str, root_url: str):
        return cls.create(target=target, name=name, slug=slugify(name), root_url=root_url)

    def add_steps(self, steps: list[list]):
        index = 1
        count = len(steps)

        for step in steps:
            CrawlStep.create(
                config=self,
                level=step[0],
                label=step[1],
                css_query=step[2],
                query_params=step[3] if len(step) == 4 else '',
                first=(index == 1),
                last=(index == count)
            )

            index += 1


class CrawlStep(BaseModel):
    config = ForeignKeyField(CrawlConfig, backref='steps')
    level = IntegerField()
    label = CharField()
    css_query = TextField()
    query_params = TextField(default='')
    first = BooleanField()
    last = BooleanField()


class ScrapConfig(BaseModel):
    target = ForeignKeyField(Target, backref='scrap_configs')
    resource_label = CharField()

    def add_property(self, name: str, css_query: str, fetch_attr: str):
        return ScrapProperty.create(config=self, name=name, css_query=css_query, fetch_attr=fetch_attr)


class ScrapProperty(BaseModel):
    config = ForeignKeyField(ScrapConfig, backref='properties')
    name = CharField()
    css_query = CharField()
    fetch_attr = CharField()

from peewee import CharField, ForeignKeyField, IntegerField, TextField, BooleanField

from _shared.base_model import BaseModel


class Manufacturer(BaseModel):
    slug = CharField()
    name = CharField()
    logo_url = TextField()

    def __str__(self):
        return self.slug

    def config_by_slug(self, config_slug):
        configs = [config for config in self.configs if config.slug == config_slug]
        if len(configs) == 0:
            raise RuntimeError('Config with slug {} not found'.format(config_slug))

        return configs[-1]


class CrawlConfig(BaseModel):
    manufacturer = ForeignKeyField(Manufacturer, backref='configs')
    slug = CharField()
    root_url = TextField()

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
    manufacturer = ForeignKeyField(Manufacturer, backref='scrap_configs')
    resource_label = CharField()

    def add_property(self, name: str, css_query: str, node_name: str):
        return ScrapProperty.create(config=self, name=name, css_query=css_query, node_name=node_name)


class ScrapProperty(BaseModel):
    config = ForeignKeyField(ScrapConfig, backref='properties')
    name = CharField()
    css_query = CharField()
    node_name = CharField()

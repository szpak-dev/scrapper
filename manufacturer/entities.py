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
                first=(index == 1),
                last=(index == count)
            )

            index += 1


class CrawlStep(BaseModel):
    config = ForeignKeyField(CrawlConfig, backref='steps')
    level = IntegerField()
    label = CharField()
    css_query = TextField()
    first = BooleanField()
    last = BooleanField()

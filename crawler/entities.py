import datetime

from peewee import CharField, DateTimeField, ForeignKeyField, TextField

from _shared.base_model import BaseModel


class Crawl(BaseModel):
    target_slug = CharField()
    started_at = DateTimeField(default=datetime.datetime.now)
    finished_at = DateTimeField(null=True)

    def add_resource(self, label: str, html: str):
        return Resource.create(crawl=self, label=label, html=html)

    def add_child_resource(self, parent, label: str, html: str):
        return Resource.create(crawl=self, parent=parent, label=label, html=html)

    def finish(self):
        self.finished_at = datetime.datetime.now()
        self.save()

    @classmethod
    def get_latest(cls, target_slug: str):
        return (
            Crawl
            .select()
            .where(cls.target_slug == target_slug)
            .order_by(cls.id.desc())
            .limit(1)
            .first()
        )


class Resource(BaseModel):
    crawl = ForeignKeyField(Crawl, backref='resources')
    parent = ForeignKeyField('self', backref='children', null=True)
    label = CharField()
    html = TextField()
    downloaded_at = DateTimeField(default=datetime.datetime.now)

    def add_link(self, name: str, path: str):
        link = Link(resource=self, name=name, path=path)
        link.save()

    @property
    def paths(self) -> list[str]:
        return [link.download_path for link in self.links]


class Link(BaseModel):
    resource = ForeignKeyField(Resource, backref='links')
    name = CharField()
    path = TextField()

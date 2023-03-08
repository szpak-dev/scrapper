from peewee import SqliteDatabase, Model

db = SqliteDatabase('./scraps.db')
db.connect()


class BaseModel(Model):
    class Meta:
        database = db

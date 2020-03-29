from peewee import SqliteDatabase, CharField, Model
from setting import DB_CONNECTION_URL

db = SqliteDatabase(DB_CONNECTION_URL)


class Demo(Model):
    demo_id = CharField(primary_key=True)

    @property
    def serialize(self):
        data = {
            'demo_id': str(self.demo_id),
        }

        return data

    def __repr__(self):
        return "{}".format(
            self.demo_id
        )

    class Meta:
        database = db
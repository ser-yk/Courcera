from peewee import *

db = SqliteDatabase('locations.db')


class Person(Model):
    id = IntegerField(primary_key=True)
    state = CharField()

    class Meta:
        database = db


class Location(Model):
    title = CharField()
    longitude = FloatField()
    latitude = FloatField()
    photo = CharField()
    owner = ForeignKeyField(Person, related_name='locations')

    class Meta:
        database = db


if __name__ == '__main__':
    Person.create_table()
    Location.create_table()
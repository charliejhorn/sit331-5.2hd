from peewee import *
# from app import db

db = SqliteDatabase('database.db')


class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db # This model uses the "people.db" database.
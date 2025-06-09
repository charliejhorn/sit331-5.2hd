import peewee as pw
from peewee import Model
from gallery.db import db

class Base(Model):
    created_datetime = pw.DateTimeField()
    modified_datetime = pw.DateTimeField()

    class Meta:
        database = db  # This model uses the "database.db" database.

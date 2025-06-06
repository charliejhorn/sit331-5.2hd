from peewee import Model
from gallery.db import db

class Base(Model):
    class Meta:
        database = db  # This model uses the "database.db" database.

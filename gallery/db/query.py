from peewee import *
from datetime import date
from gallery.models.models import Person
# from app import db

db = SqliteDatabase('database.db')

db.connect()

# create record
uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15))
uncle_bob.save() # bob is now stored in the database
# Returns: 1

# query record
bob = Person.select().where(Person.name == 'Bob').get()

db.close()

print(bob.name)
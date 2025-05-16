from peewee import *
from app.models import Person
from connect import db

allModels = [Person]

db.connect()

db.create_tables(allModels)

db.close()
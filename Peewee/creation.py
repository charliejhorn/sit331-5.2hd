from peewee import *
from models import Person
# from app import db

allModels = [Person]

db = SqliteDatabase('database.db')

db.connect()

db.create_tables(allModels)

db.close()
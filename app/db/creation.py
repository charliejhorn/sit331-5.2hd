import inspect

import app.models

from app.db import db

allModels = [model for name, model in inspect.getmembers(app.models, inspect.isclass)]
print(allModels)

db.connect()
db.create_tables(allModels)
db.close()
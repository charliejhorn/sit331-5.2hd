import inspect

import gallery.models

from gallery.db import db

allModels = [model for name, model in inspect.getmembers(gallery.models, inspect.isclass)]
print(allModels)

db.connect()
db.create_tables(allModels)
db.close()
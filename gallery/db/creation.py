import inspect

import gallery.models

from gallery.db import db
from gallery.db import UserDataAccess, RoleDataAccess

allModels = [model for name, model in inspect.getmembers(gallery.models, inspect.isclass)]
print(allModels)

db.connect()

db.create_tables(allModels)

# add a default admin role
from gallery.models import Role
admin_role = {'name':'Admin', 'description':'Administrator with full access'}
RoleDataAccess().add_new_role(admin_role)

from gallery.models import User
admin_user = {'username':'admin', 'first_name':'Alfred', 'last_name':'Harry', 'passwordHash':'admin123', 'role':'Admin', 'email':'admin@admin.com'}
UserDataAccess().add_new_user((admin_user))

db.close()
from gallery.models import Role
from playhouse.shortcuts import model_to_dict, dict_to_model
from peewee import DoesNotExist, IntegrityError
from gallery.utils import NotFoundException, DuplicateException
import datetime

class RoleDataAccess:
    def get_all_roles(self) -> list:
        """Get all roles"""
        models = [model_to_dict(r) for r in Role.select()]
        return models

    def add_new_role(self, role):
        """Create a new role"""
        current_time = datetime.datetime.now()
        role['created_datetime'] = current_time
        role['modified_datetime'] = current_time
        
        try:
            role = dict_to_model(Role, role)
            role.save()
            return model_to_dict(role)
        except IntegrityError:
            raise DuplicateException('name', role.get('name'))

    def get_role_by_id(self, id):
        """Get a single role by its ID"""
        try:
            role = Role.get_by_id(id)
            return model_to_dict(role)
        except DoesNotExist:
            raise NotFoundException("role", id)

    def update_role_by_id(self, id, updated_data):
        """Update a role by its ID"""
        try:
            role = Role.get_by_id(id)
            updated_data['modified_datetime'] = datetime.datetime.now()
            
            for key, value in updated_data.items():
                if hasattr(role, key):
                    setattr(role, key, value)
            role.save()
            return model_to_dict(role)
        except DoesNotExist:
            raise NotFoundException("role", id)
        except IntegrityError:
            # check if it's a duplicate name
            if 'name' in updated_data:
                raise DuplicateException('name', updated_data['name'])
            raise

    def delete_role_by_id(self, id):
        """Delete a role by its ID"""
        try:
            role = Role.get_by_id(id)
            role.delete_instance()
        except DoesNotExist:
            raise NotFoundException("role", id)

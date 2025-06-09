from gallery.models import User, Role, UserRoleThrough
from playhouse.shortcuts import model_to_dict, dict_to_model
from peewee import DoesNotExist, IntegrityError
from gallery.utils import NotFoundException, DuplicateException
import datetime

class UserDataAccess:
    def get_all_users(self) -> list:
        """Get all users"""
        models = [model_to_dict(u) for u in User.select()]
        return models

    def add_new_user(self, user):
        """Create a new user"""
        current_time = datetime.datetime.now()
        user['created_datetime'] = current_time
        user['modified_datetime'] = current_time
        
        try:
            user = dict_to_model(User, user)
            user.save()
            return model_to_dict(user)
        except IntegrityError:
            # Check which field caused the duplicate - username or email
            if 'username' in user:
                raise DuplicateException('username', user.get('username'))
            elif 'email' in user:
                raise DuplicateException('email', user.get('email'))
            else:
                raise DuplicateException('username', user.get('username'))

    def get_user_by_id(self, id):
        """Get a single user by its ID"""
        try:
            user = User.get_by_id(id)
            return model_to_dict(user)
        except DoesNotExist:
            raise NotFoundException("user", id)

    def update_user_by_id(self, id, updated_data):
        """Update a user by its ID"""
        try:
            user = User.get_by_id(id)
            updated_data['modified_datetime'] = datetime.datetime.now()
            
            for key, value in updated_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            try:
                user.save()
                return model_to_dict(user)
            except IntegrityError:
                # Check which field caused the duplicate - username or email
                if 'username' in updated_data:
                    raise DuplicateException('username', updated_data.get('username'))
                elif 'email' in updated_data:
                    raise DuplicateException('email', updated_data.get('email'))
                else:
                    raise DuplicateException('username', updated_data.get('username'))
        except DoesNotExist:
            raise NotFoundException("user", id)

    def delete_user_by_id(self, id):
        """Delete a user by its ID"""
        try:
            user = User.get_by_id(id)
            user.delete_instance()
        except DoesNotExist:
            raise NotFoundException("user", id)

    def get_users_by_role(self, role):
        """Get all users with a specific role"""
        # Join User with UserRoleJoin and Role to filter by role name
        users = (User
                .select()
                .join(UserRoleThrough)
                .join(Role)
                .where(Role.name == role))
        return [model_to_dict(u) for u in users]

    def get_user_by_email(self, email):
        """Get a user by email address"""
        try:
            user = User.get(User.email == email)
            return model_to_dict(user)
        except DoesNotExist:
            raise NotFoundException("user", email)

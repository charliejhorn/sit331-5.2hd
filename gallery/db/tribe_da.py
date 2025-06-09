from gallery.models import Tribe, Region
from playhouse.shortcuts import model_to_dict, dict_to_model
from peewee import DoesNotExist, IntegrityError
from gallery.utils import NotFoundException, DuplicateException
import datetime

class TribeDataAccess:
    def get_all_tribes(self) -> list:
        """Get all tribes"""
        models = [model_to_dict(t) for t in Tribe.select()]
        return models

    def add_new_tribe(self, tribe):
        """Create a new tribe"""
        current_time = datetime.datetime.now()
        tribe['created_datetime'] = current_time
        tribe['modified_datetime'] = current_time
        
        try:
            tribe = dict_to_model(Tribe, tribe)
            tribe.save()
            return model_to_dict(tribe)
        except IntegrityError:
            raise DuplicateException('name', tribe.get('name'))

    def get_tribe_by_id(self, id):
        """Get a single tribe by its ID"""
        try:
            tribe = Tribe.get_by_id(id)
            return model_to_dict(tribe)
        except DoesNotExist:
            raise NotFoundException("tribe", id)

    def update_tribe_by_id(self, id, updated_data):
        """Update a tribe by its ID"""
        try:
            tribe = Tribe.get_by_id(id)
            updated_data['modified_datetime'] = datetime.datetime.now()
            
            for key, value in updated_data.items():
                if hasattr(tribe, key):
                    setattr(tribe, key, value)
            try:
                tribe.save()
                return model_to_dict(tribe)
            except IntegrityError:
                raise DuplicateException('name', updated_data.get('name'))
        except DoesNotExist:
            raise NotFoundException("tribe", id)

    def delete_tribe_by_id(self, id):
        """Delete a tribe by its ID"""
        try:
            tribe = Tribe.get_by_id(id)
            tribe.delete_instance()
        except DoesNotExist:
            raise NotFoundException("tribe", id)

    def get_tribes_by_region(self, region_id):
        """Get all tribes in a specific region"""
        tribes = Tribe.select().where(Tribe.region == region_id)
        return [model_to_dict(t) for t in tribes]

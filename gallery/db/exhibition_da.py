from gallery.models import Exhibition
from playhouse.shortcuts import model_to_dict, dict_to_model
from peewee import DoesNotExist, IntegrityError
from gallery.utils import NotFoundException, DuplicateException
import datetime

class ExhibitionDataAccess:
    def get_all_exhibitions(self) -> list:
        """Get all exhibitions"""
        models = [model_to_dict(e) for e in Exhibition.select()]
        return models

    def add_new_exhibition(self, exhibition):
        """Create a new exhibition"""
        # Note: Exhibition model doesn't explicitly have created_datetime/modified_datetime
        # but inherits from Base which should have them
        current_time = datetime.datetime.now()
        exhibition['created_datetime'] = current_time
        exhibition['modified_datetime'] = current_time
        
        try:
            exhibition = dict_to_model(Exhibition, exhibition)
            exhibition.save()
            return model_to_dict(exhibition)
        except IntegrityError:
            raise DuplicateException('name', exhibition.get('name'))

    def get_exhibition_by_id(self, id):
        """Get a single exhibition by its ID"""
        try:
            exhibition = Exhibition.get_by_id(id)
            return model_to_dict(exhibition)
        except DoesNotExist:
            raise NotFoundException("exhibition", id)

    def update_exhibition_by_id(self, id, updated_data):
        """Update an exhibition by its ID"""
        try:
            exhibition = Exhibition.get_by_id(id)
            updated_data['modified_datetime'] = datetime.datetime.now()
            
            for key, value in updated_data.items():
                if hasattr(exhibition, key):
                    setattr(exhibition, key, value)
            exhibition.save()
            return model_to_dict(exhibition)
        except DoesNotExist:
            raise NotFoundException("exhibition", id)
        except IntegrityError:
            # check if it's a duplicate name
            if 'name' in updated_data:
                raise DuplicateException('name', updated_data['name'])
            raise

    def delete_exhibition_by_id(self, id):
        """Delete an exhibition by its ID"""
        try:
            exhibition = Exhibition.get_by_id(id)
            exhibition.delete_instance()
        except DoesNotExist:
            raise NotFoundException("exhibition", id)

    def get_exhibitions_by_date(self, date):
        """Get all exhibitions running on a specific date"""
        exhibitions = Exhibition.select().where(
            (Exhibition.start_date <= date) & 
            (Exhibition.end_date >= date)
        )
        return [model_to_dict(e) for e in exhibitions]

    def get_exhibitions_by_location(self, location):
        """Get all exhibitions at a specific location"""
        exhibitions = Exhibition.select().where(Exhibition.location == location)
        return [model_to_dict(e) for e in exhibitions]

from gallery.models import Region
from playhouse.shortcuts import model_to_dict, dict_to_model
from peewee import DoesNotExist, IntegrityError
from gallery.utils import NotFoundException, DuplicateException
import datetime

class RegionDataAccess:
    def get_all_regions(self) -> list:
        """Get all regions"""
        models = [model_to_dict(r) for r in Region.select()]
        return models

    def add_new_region(self, region):
        """Create a new region"""
        current_time = datetime.datetime.now()
        region['created_datetime'] = current_time
        region['modified_datetime'] = current_time
        
        try:
            region = dict_to_model(Region, region)
            region.save()
            return model_to_dict(region)
        except IntegrityError:
            raise DuplicateException('name', region.get('name'))

    def get_region_by_id(self, id):
        """Get a single region by its ID"""
        try:
            region = Region.get_by_id(id)
            return model_to_dict(region)
        except DoesNotExist:
            raise NotFoundException("region", id)

    def update_region_by_id(self, id, updated_data):
        """Update a region by its ID"""
        try:
            region = Region.get_by_id(id)
            updated_data['modified_datetime'] = datetime.datetime.now()
            
            for key, value in updated_data.items():
                if hasattr(region, key):
                    setattr(region, key, value)
            region.save()
            return model_to_dict(region)
        except DoesNotExist:
            raise NotFoundException("region", id)
        except IntegrityError:
            # check if it's a duplicate name
            if 'name' in updated_data:
                raise DuplicateException('name', updated_data['name'])
            raise

    def delete_region_by_id(self, id):
        """Delete a region by its ID"""
        try:
            region = Region.get_by_id(id)
            region.delete_instance()
        except DoesNotExist:
            raise NotFoundException("region", id)

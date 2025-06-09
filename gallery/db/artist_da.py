from gallery.models import Artist, Region, Tribe
from playhouse.shortcuts import model_to_dict, dict_to_model
from peewee import DoesNotExist, IntegrityError
from gallery.utils import NotFoundException, DuplicateException
import datetime

class ArtistDataAccess:
    def get_all_artists(self) -> list:
        """Get all artists"""
        models = [model_to_dict(a) for a in Artist.select()]
        return models

    def add_new_artist(self, artist):
        """Create a new artist"""
        current_time = datetime.datetime.now()
        artist['created_datetime'] = current_time
        artist['modified_datetime'] = current_time
        
        try:
            artist = dict_to_model(Artist, artist)
            artist.save()
            return model_to_dict(artist)
        except IntegrityError:
            raise DuplicateException('name', artist.get('name'))

    def get_artist_by_id(self, id):
        """Get a single artist by its ID"""
        try:
            artist = Artist.get_by_id(id)
            return model_to_dict(artist)
        except DoesNotExist:
            raise NotFoundException("artist", id)

    def update_artist_by_id(self, id, updated_data):
        """Update an artist by its ID"""
        try:
            artist = Artist.get_by_id(id)
            updated_data['modified_datetime'] = datetime.datetime.now()
            
            for key, value in updated_data.items():
                if hasattr(artist, key):
                    setattr(artist, key, value)
            artist.save()
            return model_to_dict(artist)
        except DoesNotExist:
            raise NotFoundException("artist", id)
        except IntegrityError:
            # check if it's a duplicate name
            if 'name' in updated_data:
                raise DuplicateException('name', updated_data['name'])
            raise

    def delete_artist_by_id(self, id):
        """Delete an artist by its ID"""
        try:
            artist = Artist.get_by_id(id)
            artist.delete_instance()
        except DoesNotExist:
            raise NotFoundException("artist", id)

    def get_artists_by_region(self, region_id):
        """Get all artists from a specific region"""
        artists = Artist.select().where(Artist.region == region_id)
        return [model_to_dict(a) for a in artists]

    def get_artists_by_tribe(self, tribe_id):
        """Get all artists from a specific tribe"""
        artists = Artist.select().where(Artist.tribe == tribe_id)
        return [model_to_dict(a) for a in artists]

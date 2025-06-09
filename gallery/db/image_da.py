from gallery.models import Image, Artifact
from playhouse.shortcuts import model_to_dict, dict_to_model
from peewee import DoesNotExist, IntegrityError
from gallery.utils import NotFoundException, DuplicateException
import datetime

class ImageDataAccess:
    def get_all_images(self) -> list:
        """Get all images"""
        models = [model_to_dict(i) for i in Image.select()]
        return models

    def add_new_image(self, image):
        """Create a new image"""
        current_time = datetime.datetime.now()
        image['created_datetime'] = current_time
        image['modified_datetime'] = current_time
        
        try:
            image = dict_to_model(Image, image)
            image.save()
            return model_to_dict(image)
        except IntegrityError:
            raise DuplicateException('url', image.get('url'))

    def get_image_by_id(self, id):
        """Get a single image by its ID"""
        try:
            image = Image.get_by_id(id)
            return model_to_dict(image)
        except DoesNotExist:
            raise NotFoundException("image", id)

    def update_image_by_id(self, id, updated_data):
        """Update an image by its ID"""
        try:
            image = Image.get_by_id(id)
            updated_data['modified_datetime'] = datetime.datetime.now()
            
            for key, value in updated_data.items():
                if hasattr(image, key):
                    setattr(image, key, value)
            image.save()
            return model_to_dict(image)
        except DoesNotExist:
            raise NotFoundException("image", id)
        except IntegrityError:
            # check if it's a duplicate url
            if 'url' in updated_data:
                raise DuplicateException('url', updated_data['url'])
            raise

    def delete_image_by_id(self, id):
        """Delete an image by its ID"""
        try:
            image = Image.get_by_id(id)
            image.delete_instance()
        except DoesNotExist:
            raise NotFoundException("image", id)

    def get_images_by_artifact(self, artifact_id):
        """Get all images for a specific artifact"""
        images = Image.select().where(Image.artifact == artifact_id)
        return [model_to_dict(i) for i in images]

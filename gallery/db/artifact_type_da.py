from gallery.models import ArtifactType
from playhouse.shortcuts import model_to_dict, dict_to_model
from peewee import DoesNotExist, IntegrityError
from gallery.utils import NotFoundException, DuplicateException
import datetime

class ArtifactTypeDataAccess:
    def get_all_artifact_types(self) -> list:
        """Get all artifact types"""
        models = [model_to_dict(at) for at in ArtifactType.select()]
        return models

    def add_new_artifact_type(self, artifact_type):
        """Create a new artifact type"""
        current_time = datetime.datetime.now()
        artifact_type['created_datetime'] = current_time
        artifact_type['modified_datetime'] = current_time
        
        try:
            artifact_type = dict_to_model(ArtifactType, artifact_type)
            artifact_type.save()
            return model_to_dict(artifact_type)
        except IntegrityError:
            raise DuplicateException('name', artifact_type.get('name'))

    def get_artifact_type_by_id(self, id):
        """Get a single artifact type by its ID"""
        try:
            artifact_type = ArtifactType.get_by_id(id)
            return model_to_dict(artifact_type)
        except DoesNotExist:
            raise NotFoundException("artifact_type", id)

    def update_artifact_type_by_id(self, id, updated_data):
        """Update an artifact type by its ID"""
        try:
            artifact_type = ArtifactType.get_by_id(id)
            updated_data['modified_datetime'] = datetime.datetime.now()
            
            for key, value in updated_data.items():
                if hasattr(artifact_type, key):
                    setattr(artifact_type, key, value)
            artifact_type.save()
            return model_to_dict(artifact_type)
        except DoesNotExist:
            raise NotFoundException("artifact_type", id)
        except IntegrityError:
            # check if it's a duplicate name
            if 'name' in updated_data:
                raise DuplicateException('name', updated_data['name'])
            raise

    def delete_artifact_type_by_id(self, id):
        """Delete an artifact type by its ID"""
        try:
            artifact_type = ArtifactType.get_by_id(id)
            artifact_type.delete_instance()
        except DoesNotExist:
            raise NotFoundException("artifact_type", id)

from gallery.models import Artifact
from playhouse.shortcuts import model_to_dict, dict_to_model
from peewee import DoesNotExist, IntegrityError
from gallery.utils import NotFoundException, DuplicateException
from pprint import pprint
import datetime

class ArtifactDataAccess:
    def get_all_artifacts(self) -> list:
        models = [model_to_dict(a) for a in Artifact.select()]
        return models

    def add_new_artifact(self, artifact):
        # set created and modified datetime
        current_time = datetime.datetime.now()
        artifact['created_datetime'] = current_time
        artifact['modified_datetime'] = current_time
        
        try:
            artifact = dict_to_model(Artifact, artifact)
            artifact.save()
            return model_to_dict(artifact)
        except IntegrityError:
            raise DuplicateException('title', artifact.get('title'))

    def get_artifact_by_id(self, id):
        """Get a single artifact by its ID"""
        try:
            artifact = Artifact.get_by_id(id)
            return model_to_dict(artifact)
        except DoesNotExist:
            raise NotFoundException("artifact", id)

    def update_artifact_by_id(self, id, updated_data):
        """Update an artifact by its ID"""
        try:
            artifact = Artifact.get_by_id(id)
            # set modified datetime
            updated_data['modified_datetime'] = datetime.datetime.now()
            
            # update only the provided fields
            for key, value in updated_data.items():
                if hasattr(artifact, key):
                    setattr(artifact, key, value)
            artifact.save()
            return model_to_dict(artifact)
        except DoesNotExist:
            raise NotFoundException("artifact", id)
        except IntegrityError:
            # check if it's a duplicate title
            if 'title' in updated_data:
                raise DuplicateException('title', updated_data['title'])
            raise

    def delete_artifact_by_id(self, id):
        """Delete an artifact by its ID"""
        try:
            artifact = Artifact.get_by_id(id)
            artifact.delete_instance()
        except DoesNotExist:
            raise NotFoundException("artifact", id)

    def get_artifacts_by_type(self, artifact_type_id):
        """Get all artifacts of a specific type"""
        artifacts = Artifact.select().where(Artifact.artifact_type == artifact_type_id)
        return [model_to_dict(a) for a in artifacts]

    def get_artifacts_by_year(self, year):
        """Get all artifacts authored in a specific year"""
        artifacts = Artifact.select().where(Artifact.date_authored.year == year)
        return [model_to_dict(a) for a in artifacts]

    def get_artifacts_by_location(self, display_location):
        """Get all artifacts by display location"""
        artifacts = Artifact.select().where(Artifact.display_location == display_location)
        return [model_to_dict(a) for a in artifacts]

    def get_artifacts_by_date_range(self, start_date, end_date):
        """Get all artifacts authored within a date range"""
        artifacts = Artifact.select().where(
            (Artifact.date_authored >= start_date) & 
            (Artifact.date_authored <= end_date)
        )
        return [model_to_dict(a) for a in artifacts]


if __name__ == "__main__":
    da = ArtifactDataAccess()
    # a=Artifact.create(title="Cool Rock", description="Coolest of the rocks", date_authored=datetime.date.today(), display_location="Pedastool next to the cool stones exhibit", artifact_type=1)
    # a.save()
    pprint(da.get_all_artifacts())
    print(type(da.get_all_artifacts()))

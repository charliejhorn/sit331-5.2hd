from gallery.models import Artifact
import datetime
import json
from playhouse.shortcuts import model_to_dict, dict_to_model
from pprint import pprint

class ArtifactDataAccess:
    def get_all_artifacts(self) -> list:
        return [model_to_dict(a) for a in Artifact.select()]

    def add_new_artifact(self, artifact: dict):
        artifact = dict_to_model(Artifact, artifact)
        return None 


if __name__ == "__main__":
    da = ArtifactDataAccess()
    # a=Artifact.create(title="Cool Rock", description="Coolest of the rocks", date_authored=datetime.date.today(), display_location="Pedastool next to the cool stones exhibit", artifact_type=1)
    # a.save()
    pprint(da.get_all_artifacts())
    print(type(da.get_all_artifacts()))

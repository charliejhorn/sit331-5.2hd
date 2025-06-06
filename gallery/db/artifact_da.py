from gallery.models import Artifact
from playhouse.shortcuts import model_to_dict, dict_to_model
from pprint import pprint

class ArtifactDataAccess:
    def get_all_artifacts(self) -> list:
        models = [model_to_dict(a) for a in Artifact.select()]
        return models

    def add_new_artifact(self, artifact):

        # set dates here

        artifact = dict_to_model(Artifact, artifact)
        artifact.save()
        return model_to_dict(artifact)


if __name__ == "__main__":
    da = ArtifactDataAccess()
    # a=Artifact.create(title="Cool Rock", description="Coolest of the rocks", date_authored=datetime.date.today(), display_location="Pedastool next to the cool stones exhibit", artifact_type=1)
    # a.save()
    pprint(da.get_all_artifacts())
    print(type(da.get_all_artifacts()))

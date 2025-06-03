from models import Artifact
import datetime

class ArtifactDataAccess:
    def GetAllArtifacts(id):
        artifact = Artifact(1, 'river painting', 'painting of a river', datetime.date.today(), "a1", "painting")
        return artifact
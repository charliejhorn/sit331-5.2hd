import falcon

from gallery.db import ArtifactDataAccess
from gallery.utils import serialize_dicts

class ArtifactResource:
    def __init__(self) -> None:
        self.dal = ArtifactDataAccess()

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON

        artifacts = self.dal.get_all_artifacts()
        resp.media = serialize_dicts(artifacts)

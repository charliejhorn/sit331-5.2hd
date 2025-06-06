from pprint import pprint
from falcon import MEDIA_JSON, HTTP_200, HTTP_201

class RoleResource:
    def __init__(self, dal) -> None:
        self.dal = dal

    def on_get(self, req, resp):
        artifacts = self.dal.get_all_artifacts()

        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = artifacts

    def on_post(self, req, resp):
        newArtifact = req.get_media()
        pprint(newArtifact)
        
        createdArtifact = self.dal.add_new_artifact(newArtifact)
        
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_201
        resp.media = createdArtifact
        resp.location = '/api/artifacts/' + createdArtifact["id"]
        
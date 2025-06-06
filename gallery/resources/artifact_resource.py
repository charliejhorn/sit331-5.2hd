import falcon
import json
from pprint import pprint
from falcon import MEDIA_JSON, HTTP_200, HTTP_201

from gallery.db import ArtifactDataAccess
from gallery.utils import serialize_dicts

class ArtifactResource:
    def __init__(self) -> None:
        self.dal = ArtifactDataAccess()

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
        
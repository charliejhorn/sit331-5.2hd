import falcon

from gallery.db.artifact import ArtifactDataAccess

class ArtifactResource:
    def __init__(self) -> None:
        self.dal = ArtifactDataAccess() 
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.media = self.dal.get_all_artifacts() 

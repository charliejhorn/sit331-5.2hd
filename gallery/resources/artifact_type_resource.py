from pprint import pprint
from falcon import MEDIA_JSON, HTTP_200, HTTP_201

class ArtifactTypeResource:
    def __init__(self, dal) -> None:
        self.dal = dal

    def on_get(self, req, resp):
        types = self.dal.get_all_types()

        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = types 

    def on_post(self, req, resp):
        new_type = req.get_media()
        
        created_type = self.dal.add_new_artifact(new_type)
        
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_201
        resp.media = created_type
        resp.location = '/api/artifact_types/' + created_type["id"]
        
    def on_get_item(self, req, resp, id):
        image = self.dal.get_type(id)

        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = image

    def on_update_item(self, req, resp, id):
        image = self.dal.update_type(id, req.get_media)

        resp.status = HTTP_201

    def on_delete_item(self, req, resp, id):
        self.dal.delete_type(id)
        resp.status = HTTP_201

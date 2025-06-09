from pprint import pprint
from falcon import MEDIA_JSON, HTTP_200, HTTP_201

class ImageResource:
    def __init__(self, dal) -> None:
        self.dal = dal()

    def on_get(self, req, resp):
        images = self.dal.get_all_images()

        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = images

    def on_post(self, req, resp):
        newArtifact = req.get_media()
        pprint(newArtifact)
        
        createdArtifact = self.dal.add_new_artifact(newArtifact)
        
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = createdArtifact
        resp.location = '/api/artifacts/' + createdArtifact["id"]

    def on_get_item(self, req, resp, id):
        image = self.dal.get_image(id)

        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = image

    def on_update_item(self, req, resp, id):
        resp.status = HTTP_201
        self.dal.update_image(req.get_media())

    def on_delete_item(self, req, resp, id):
        resp.status = HTTP_201

        self.dal.delete_image(id)
        

from pprint import pprint
from falcon import MEDIA_JSON, HTTP_200, HTTP_201, HTTP_404, HTTP_204, HTTP_409, HTTP_500
from gallery.utils import NotFoundException, DuplicateException

class ImageResource:
    def __init__(self, dal) -> None:
        self.dal = dal()

    def on_get(self, req, resp):
        # get all images
        images = self.dal.get_all_images()

        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = images

    def on_post(self, req, resp):
        # create new image
        try:
            new_image = req.get_media()
            pprint(new_image)
            
            created_image = self.dal.add_new_image(new_image)
            
            resp.content_type = MEDIA_JSON
            resp.status = HTTP_201
            resp.media = created_image
            resp.location = '/api/images/' + str(created_image["id"])
        except DuplicateException as e:
            resp.status = HTTP_409
            resp.media = {"error": str(e)}
        except Exception as e:
            resp.status = HTTP_500
            resp.media = {"error": "Internal server error"}

    def on_get_by_id(self, req, resp, id):
        # get image by id
        try:
            image = self.dal.get_image_by_id(id)
            resp.content_type = MEDIA_JSON
            resp.status = HTTP_200
            resp.media = image
        except NotFoundException as e:
            resp.status = HTTP_404
            resp.media = {"error": str(e)}
        except Exception as e:
            resp.status = HTTP_500
            resp.media = {"error": "Internal server error"}

    def on_put_by_id(self, req, resp, id):
        # update image by id
        try:
            updated_data = req.get_media()
            updated_image = self.dal.update_image_by_id(id, updated_data)
            resp.content_type = MEDIA_JSON
            resp.status = HTTP_200
            resp.media = updated_image
        except NotFoundException as e:
            resp.status = HTTP_404
            resp.media = {"error": str(e)}
        except DuplicateException as e:
            resp.status = HTTP_409
            resp.media = {"error": str(e)}
        except Exception as e:
            resp.status = HTTP_500
            resp.media = {"error": "Internal server error"}

    def on_delete_by_id(self, req, resp, id):
        # delete image by id
        try:
            self.dal.delete_image_by_id(id)
            resp.status = HTTP_204
        except NotFoundException as e:
            resp.status = HTTP_404
            resp.media = {"error": str(e)}
        except Exception as e:
            resp.status = HTTP_500
            resp.media = {"error": "Internal server error"}

    def on_get_by_artifact(self, req, resp, artifact_id):
        # get images by artifact
        images = self.dal.get_images_by_artifact(artifact_id)
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = images
        

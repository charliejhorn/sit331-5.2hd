from pprint import pprint
from falcon import MEDIA_JSON, HTTP_200, HTTP_201, HTTP_404, HTTP_204, HTTP_409, HTTP_500
from gallery.utils import NotFoundException, DuplicateException

class ArtifactTypeResource:
    def __init__(self, dal) -> None:
        self.dal = dal()

    def on_get(self, req, resp):
        # get all artifact types
        types = self.dal.get_all_artifact_types()

        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = types 

    def on_post(self, req, resp):
        # create new artifact type
        try:
            new_type = req.get_media()
            pprint(new_type)
            
            created_type = self.dal.add_new_artifact_type(new_type)
            
            resp.content_type = MEDIA_JSON
            resp.status = HTTP_201
            resp.media = created_type
            resp.location = '/api/artifact-types/' + str(created_type["id"])
        except DuplicateException as e:
            resp.status = HTTP_409
            resp.media = {"error": str(e)}
        except Exception as e:
            resp.status = HTTP_500
            resp.media = {"error": "Internal server error"}

    def on_get_by_id(self, req, resp, id):
        # get artifact type by id
        try:
            artifact_type = self.dal.get_artifact_type_by_id(id)
            resp.content_type = MEDIA_JSON
            resp.status = HTTP_200
            resp.media = artifact_type
        except NotFoundException as e:
            resp.status = HTTP_404
            resp.media = {"error": str(e)}
        except Exception as e:
            resp.status = HTTP_500
            resp.media = {"error": "Internal server error"}

    def on_put_by_id(self, req, resp, id):
        # update artifact type by id
        try:
            updated_data = req.get_media()
            updated_type = self.dal.update_artifact_type_by_id(id, updated_data)
            resp.content_type = MEDIA_JSON
            resp.status = HTTP_200
            resp.media = updated_type
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
        # delete artifact type by id
        try:
            self.dal.delete_artifact_type_by_id(id)
            resp.status = HTTP_204
        except NotFoundException as e:
            resp.status = HTTP_404
            resp.media = {"error": str(e)}
        except Exception as e:
            resp.status = HTTP_500
            resp.media = {"error": "Internal server error"}

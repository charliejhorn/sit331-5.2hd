from pprint import pprint
from falcon import MEDIA_JSON, HTTP_200, HTTP_201, HTTP_409, HTTP_404, HTTP_500, HTTP_204
from gallery.utils import NotFoundException, DuplicateException

class ExhibitionResource:
    def __init__(self, dal) -> None:
        self.dal = dal()

    def on_get(self, req, resp):
        # get all exhibitions
        types = self.dal.get_all_exhibitions()

        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = types 

    def on_post(self, req, resp):
        # create new exhibition
        try:
            new_type = req.get_media()
            pprint(new_type)
            
            created_type = self.dal.add_new_exhibition(new_type)
            
            resp.content_type = MEDIA_JSON
            resp.status = HTTP_201
            resp.media = created_type
            resp.location = '/api/exhibitions/' + str(created_type["id"])
        except DuplicateException as e:
            resp.status = HTTP_409
            resp.media = {"error": str(e)}
        except Exception as e:
            resp.status = HTTP_500
            resp.media = {"error": "Internal server error"}

    def on_get_by_id(self, req, resp, id):
        # get exhibition by id
        try:
            exhibition = self.dal.get_exhibition_by_id(id)
            resp.content_type = MEDIA_JSON
            resp.status = HTTP_200
            resp.media = exhibition
        except NotFoundException as e:
            resp.status = HTTP_404
            resp.media = {"error": str(e)}
        except Exception as e:
            resp.status = HTTP_500
            resp.media = {"error": "Internal server error"}

    def on_put_by_id(self, req, resp, id):
        # update exhibition by id
        try:
            updated_data = req.get_media()
            updated_type = self.dal.update_exhibition_by_id(id, updated_data)
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
        # delete exhibition by id
        try:
            self.dal.delete_exhibition_by_id(id)
            resp.status = HTTP_204
        except NotFoundException as e:
            resp.status = HTTP_404
            resp.media = {"error": str(e)}
        except Exception as e:
            resp.status = HTTP_500
            resp.media = {"error": "Internal server error"}

    def on_get_by_date(self, req, resp, date):
        # get exhibitions by date
        exhibitions = self.dal.get_exhibitions_by_date(date)
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = exhibitions

    def on_get_by_location(self, req, resp, location):
        # get exhibitions by location
        exhibitions = self.dal.get_exhibitions_by_location(location)
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = exhibitions

    def on_get_by_artifact(self, req, resp, artifact_id):
        # get exhibitions by artifact
        exhibitions = self.dal.get_exhibitions_by_artifact(artifact_id)
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = exhibitions

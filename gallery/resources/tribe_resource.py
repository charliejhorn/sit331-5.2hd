from pprint import pprint
from falcon import MEDIA_JSON, HTTP_200, HTTP_201, HTTP_404, HTTP_204, HTTP_409, HTTP_500
from gallery.utils import NotFoundException, DuplicateException

class TribeResource:
    def __init__(self, dal) -> None:
        self.dal = dal()

    def on_get(self, req, resp):
        # get all tribes
        tribes = self.dal.get_all_tribes()

        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = tribes

    def on_post(self, req, resp):
        # create new tribe
        try:
            new_tribe = req.get_media()
            pprint(new_tribe)
            
            created_tribe = self.dal.add_new_tribe(new_tribe)
            
            resp.content_type = MEDIA_JSON
            resp.status = HTTP_201
            resp.media = created_tribe
            resp.location = '/api/tribes/' + str(created_tribe["id"])
        except DuplicateException as e:
            resp.status = HTTP_409
            resp.media = {"error": str(e)}
        except Exception as e:
            resp.status = HTTP_500
            resp.media = {"error": "Internal server error"}

    def on_get_by_id(self, req, resp, id):
        # get tribe by id
        try:
            tribe = self.dal.get_tribe_by_id(id)
            resp.content_type = MEDIA_JSON
            resp.status = HTTP_200
            resp.media = tribe
        except NotFoundException as e:
            resp.status = HTTP_404
            resp.media = {"error": str(e)}
        except Exception as e:
            resp.status = HTTP_500
            resp.media = {"error": "Internal server error"}

    def on_put_by_id(self, req, resp, id):
        # update tribe by id
        try:
            updated_data = req.get_media()
            updated_tribe = self.dal.update_tribe_by_id(id, updated_data)
            resp.content_type = MEDIA_JSON
            resp.status = HTTP_200
            resp.media = updated_tribe
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
        # delete tribe by id
        try:
            self.dal.delete_tribe_by_id(id)
            resp.status = HTTP_204
        except NotFoundException as e:
            resp.status = HTTP_404
            resp.media = {"error": str(e)}
        except Exception as e:
            resp.status = HTTP_500
            resp.media = {"error": "Internal server error"}

    def on_get_by_region(self, req, resp, region_id):
        # get tribes by region
        tribes = self.dal.get_tribes_by_region(region_id)
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = tribes
        
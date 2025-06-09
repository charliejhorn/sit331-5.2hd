from pprint import pprint
from falcon import MEDIA_JSON, HTTP_200, HTTP_201, HTTP_404, HTTP_204, HTTP_409, HTTP_500
from gallery.utils import NotFoundException, DuplicateException

class RegionResource:
    def __init__(self, dal) -> None:
        self.dal = dal()

    def on_get(self, req, resp):
        # get all regions
        regions = self.dal.get_all_regions()

        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = regions

    def on_post(self, req, resp):
        # create new region
        try:
            new_region = req.get_media()
            pprint(new_region)
            
            created_region = self.dal.add_new_region(new_region)
            
            resp.content_type = MEDIA_JSON
            resp.status = HTTP_201
            resp.media = created_region
            resp.location = '/api/regions/' + str(created_region["id"])
        except DuplicateException as e:
            resp.status = HTTP_409
            resp.media = {"error": str(e)}
        except Exception as e:
            resp.status = HTTP_500
            resp.media = {"error": "Internal server error"}

    def on_get_by_id(self, req, resp, id):
        # get region by id
        try:
            region = self.dal.get_region_by_id(id)
            resp.content_type = MEDIA_JSON
            resp.status = HTTP_200
            resp.media = region
        except NotFoundException as e:
            resp.status = HTTP_404
            resp.media = {"error": str(e)}
        except Exception as e:
            resp.status = HTTP_500
            resp.media = {"error": "Internal server error"}

    def on_put_by_id(self, req, resp, id):
        # update region by id
        try:
            updated_data = req.get_media()
            updated_region = self.dal.update_region_by_id(id, updated_data)
            resp.content_type = MEDIA_JSON
            resp.status = HTTP_200
            resp.media = updated_region
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
        # delete region by id
        try:
            self.dal.delete_region_by_id(id)
            resp.status = HTTP_204
        except NotFoundException as e:
            resp.status = HTTP_404
            resp.media = {"error": str(e)}
        except Exception as e:
            resp.status = HTTP_500
            resp.media = {"error": "Internal server error"}
        
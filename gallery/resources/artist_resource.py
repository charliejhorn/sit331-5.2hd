from pprint import pprint
import falcon
from falcon import MEDIA_JSON, HTTP_200, HTTP_201, HTTP_404, HTTP_204, HTTP_409, HTTP_500
from gallery.utils import NotFoundException, DuplicateException
from gallery.auth import Authorize

@falcon.before(Authorize(['Viewer', 'Editor', 'Admin']))
class ArtistResource:
    def __init__(self, dal) -> None:
        self.dal = dal

    def on_get(self, req, resp):
        # get all artists
        artists = self.dal.get_all_artists()

        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = artists 

    @falcon.before(Authorize(['Editor', 'Admin']))
    def on_post(self, req, resp):
        # create new artist
        try:
            artist = req.get_media()
            pprint(artist)
            
            new_artist = self.dal.add_new_artist(artist)
            
            resp.content_type = MEDIA_JSON
            resp.status = HTTP_201
            resp.media = new_artist
            resp.location = '/api/artists/' + str(new_artist["id"])
        except DuplicateException as e:
            resp.status = HTTP_409
            resp.media = {"error": str(e)}
        except Exception as e:
            resp.status = HTTP_500
            resp.media = {"error": "Internal server error"}

    def on_get_by_id(self, req, resp, id):
        # get artist by id
        try:
            artist = self.dal.get_artist_by_id(id)
            resp.content_type = MEDIA_JSON
            resp.status = HTTP_200
            resp.media = artist
        except NotFoundException as e:
            resp.status = HTTP_404
            resp.media = {"error": str(e)}
        except Exception as e:
            resp.status = HTTP_500
            resp.media = {"error": "Internal server error"}

    @falcon.before(Authorize(['Editor', 'Admin']))
    def on_put_by_id(self, req, resp, id):
        # update artist by id
        try:
            updated_data = req.get_media()
            updated_artist = self.dal.update_artist_by_id(id, updated_data)
            resp.content_type = MEDIA_JSON
            resp.status = HTTP_200
            resp.media = updated_artist
        except NotFoundException as e:
            resp.status = HTTP_404
            resp.media = {"error": str(e)}
        except DuplicateException as e:
            resp.status = HTTP_409
            resp.media = {"error": str(e)}
        except Exception as e:
            resp.status = HTTP_500
            resp.media = {"error": "Internal server error"}

    @falcon.before(Authorize(['Admin']))
    def on_delete_by_id(self, req, resp, id):
        # delete artist by id
        try:
            self.dal.delete_artist_by_id(id)
            resp.status = HTTP_204
        except NotFoundException as e:
            resp.status = HTTP_404
            resp.media = {"error": str(e)}
        except Exception as e:
            resp.status = HTTP_500
            resp.media = {"error": "Internal server error"}

    def on_get_by_region(self, req, resp, region_id):
        # get artists by region
        artists = self.dal.get_artists_by_region(region_id)
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = artists

    def on_get_by_tribe(self, req, resp, tribe_id):
        # get artists by tribe
        artists = self.dal.get_artists_by_tribe(tribe_id)
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = artists

    def on_get_by_artifact(self, req, resp, artifact_id):
        # get artists by artifact
        artists = self.dal.get_artists_by_artifact(artifact_id)
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = artists

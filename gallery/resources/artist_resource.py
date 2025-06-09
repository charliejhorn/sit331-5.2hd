from pprint import pprint
from falcon import MEDIA_JSON, HTTP_200, HTTP_201

class ArtistResource:
    def __init__(self, dal) -> None:
        self.dal = dal()

    def on_get(self, req, resp):
        artists = self.dal.get_all_artists()

        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = artists 

    def on_post(self, req, resp):
        artist = req.get_media()
        
        new_artist = self.dal.add_new_artifact(artist)
        
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_201
        resp.media = new_artist
        resp.location = '/api/artists/' + new_artist["id"]

    def on_get_item(self, req, resp, id):
        artist = self.dal.get_artist(id)

        resp.status = HTTP_200
        resp.content_type = MEDIA_JSON
        resp.media = artist
        
    def on_update_item(self, req, resp, id):
        self.dal.update_artist(id, req.get_media())

        resp.status = HTTP_201

    def on_delete_item(self, req, resp, id):
        self.dal.delete_artist(id)

        resp.status = HTTP_201

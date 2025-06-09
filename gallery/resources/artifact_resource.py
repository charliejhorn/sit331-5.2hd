from pprint import pprint
from falcon import MEDIA_JSON, HTTP_200, HTTP_201, HTTP_404, HTTP_204, HTTP_409, HTTP_500
from gallery.utils import NotFoundException, DuplicateException

class ArtifactResource:
    def __init__(self, dal) -> None:
        self.dal = dal()

    def on_get(self, req, resp):
        artifacts = self.dal.get_all_artifacts()

        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = artifacts

    def on_post(self, req, resp):
        newArtifact = req.get_media()
        pprint(newArtifact)
        
        try:
            createdArtifact = self.dal.add_new_artifact(newArtifact)
            resp.content_type = MEDIA_JSON
            resp.status = HTTP_201
            resp.media = createdArtifact
            resp.location = '/api/artifacts/' + str(createdArtifact["id"])
        except DuplicateException as e:
            resp.status = HTTP_409
            resp.media = {"error": str(e)}
        except Exception as e:
            resp.status = HTTP_500
            resp.media = {"error": "Internal server error"}

    def on_get_by_id(self, req, resp, id):
        # get artifact by id
        try:
            artifact = self.dal.get_artifact_by_id(id)
            resp.content_type = MEDIA_JSON
            resp.status = HTTP_200
            resp.media = artifact
        except NotFoundException as e:
            resp.status = HTTP_404
            resp.media = {"error": str(e)}
        except Exception as e:
            resp.status = HTTP_500
            resp.media = {"error": "Internal server error"}

    def on_put_by_id(self, req, resp, id):
        # update artifact by id
        try:
            updated_data = req.get_media()
            updated_artifact = self.dal.update_artifact_by_id(id, updated_data)
            resp.content_type = MEDIA_JSON
            resp.status = HTTP_200
            resp.media = updated_artifact
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
        # delete artifact by id
        try:
            self.dal.delete_artifact_by_id(id)
            resp.status = HTTP_204
        except NotFoundException as e:
            resp.status = HTTP_404
            resp.media = {"error": str(e)}
        except Exception as e:
            resp.status = HTTP_500
            resp.media = {"error": "Internal server error"}

    def on_get_by_type(self, req, resp, artifact_type_id):
        # get artifacts by artifact type
        artifacts = self.dal.get_artifacts_by_type(artifact_type_id)
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = artifacts

    def on_get_by_year(self, req, resp, year):
        # get artifacts by year authored
        artifacts = self.dal.get_artifacts_by_year(year)
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = artifacts

    def on_get_by_location(self, req, resp, display_location):
        # get artifacts by display location
        artifacts = self.dal.get_artifacts_by_location(display_location)
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = artifacts

    def on_get_by_date(self, req, resp, start_date, end_date):
        # get artifacts by date range
        artifacts = self.dal.get_artifacts_by_date_range(start_date, end_date)
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = artifacts

    def on_get_by_artist(self, req, resp, artist_id):
        # get artifacts by artist
        artifacts = self.dal.get_artifacts_by_artist(artist_id)
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = artifacts

    def on_get_by_exhibition(self, req, resp, exhibition_id):
        # get artifacts by exhibition
        artifacts = self.dal.get_artifacts_by_exhibition(exhibition_id)
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = artifacts
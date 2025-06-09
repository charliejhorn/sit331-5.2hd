from pprint import pprint
from falcon import MEDIA_JSON, HTTP_200, HTTP_201, HTTP_404, HTTP_204

class CommentResource:
    def __init__(self, dal) -> None:
        self.dal = dal()
    
    def on_get(self, req, resp):
        # get all comments
        comments = self.dal.get_all_comments()

        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = comments 
 
    def on_post(self, req, resp):
        # create new comment
        new_comment = req.get_media()
        pprint(new_comment)
        
        created_comment = self.dal.add_new_comment(new_comment)
        
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_201
        resp.media = created_comment
        resp.location = '/api/comments/' + str(created_comment["id"])

    def on_get_by_id(self, req, resp, id):
        # get comment by id
        try:
            comment = self.dal.get_comment_by_id(id)
            resp.content_type = MEDIA_JSON
            resp.status = HTTP_200
            resp.media = comment
        except Exception:
            resp.status = HTTP_404
            resp.media = {"error": "Comment not found"}

    def on_put_by_id(self, req, resp, id):
        # update comment by id
        try:
            updated_data = req.get_media()
            updated_comment = self.dal.update_comment_by_id(id, updated_data)
            resp.content_type = MEDIA_JSON
            resp.status = HTTP_200
            resp.media = updated_comment
        except Exception:
            resp.status = HTTP_404
            resp.media = {"error": "Comment not found"}

    def on_delete_by_id(self, req, resp, id):
        # delete comment by id
        try:
            self.dal.delete_comment_by_id(id)
            resp.status = HTTP_204
        except Exception:
            resp.status = HTTP_404
            resp.media = {"error": "Comment not found"}

    def on_get_by_artifact(self, req, resp, artifact_id):
        # get comments by artifact
        comments = self.dal.get_comments_by_artifact(artifact_id)
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = comments

    def on_get_by_user(self, req, resp, user_id):
        # get comments by user
        comments = self.dal.get_comments_by_user(user_id)
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = comments

    def on_get_by_artifact_and_user(self, req, resp, artifact_id, user_id):
        # get comments by artifact and user
        comments = self.dal.get_comments_by_artifact_and_user(artifact_id, user_id)
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = comments

    def on_get_by_date(self, req, resp, start_date, end_date):
        # get comments by date range
        comments = self.dal.get_comments_by_date_range(start_date, end_date)
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = comments

    def on_get_by_parent_comment(self, req, resp, parent_comment_id):
        # get comments by parent comment
        comments = self.dal.get_comments_by_parent_comment(parent_comment_id)
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = comments

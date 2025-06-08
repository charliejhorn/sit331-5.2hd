from pprint import pprint
from falcon import HTTP_NO_CONTENT, MEDIA_JSON, HTTP_200, HTTP_201

class CommentResource:
    def __init__(self, dal) -> None:
        self.dal = dal()
    
    # gets all comments
    def on_get(self, req, resp):
        comments = self.dal.get_all_comments()

        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = comments 
 
    def on_post(self, req, resp):
        new_comment = req.get_media()
        
        created_comment = self.dal.add_comment(new_comment)
        
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_201
        resp.media = created_comment
        resp.location = '/api/comments/' + created_comment["id"]
        
    def on_delete_item(self, req, resp, id):
        resp.status = HTTP_NO_CONTENT
        self.dal.delete_comment(id)

    def on_get_item(self, req, resp, id):
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = self.dal.get_comment(id)

    def on_put_item(self, req, resp, id):
        resp.status = HTTP_NO_CONTENT
        self.dal.update_comment(req.get_media())

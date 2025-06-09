from pprint import pprint
import falcon
from falcon import MEDIA_JSON, HTTP_200, HTTP_201, HTTP_404, HTTP_204, HTTP_409, HTTP_500
from gallery.utils import NotFoundException, DuplicateException
from gallery.auth import hash_password, Authorize

class UserResource:
    def __init__(self, dal) -> None:
        self.dal = dal

    @falcon.before(Authorize(['Admin']))
    def on_get(self, req, resp):
        # get all users
        users = self.dal.get_all_users()

        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = users

    @falcon.before(Authorize([]))
    def on_post(self, req, resp):
        # create new user
        try:
            new_user = req.get_media()

            new_user["password"] = hash_password(new_user["password"])
            
            created_user = self.dal.add_new_user(new_user)
            
            resp.content_type = MEDIA_JSON
            resp.status = HTTP_201
            resp.media = created_user
            resp.location = '/api/users/' + str(created_user["id"])
        except DuplicateException as e:
            resp.status = HTTP_409
            resp.media = {"error": str(e)}
        except Exception as e:
            resp.status = HTTP_500
            resp.media = {"error": "Internal server error"}
    
    @falcon.before(Authorize(['Editor', 'Admin', 'Self']))
    def on_get_by_id(self, req, resp, id):
        # get user by id
        try:
            user = self.dal.get_user_by_id(id)
            resp.content_type = MEDIA_JSON
            resp.status = HTTP_200
            resp.media = user
        except NotFoundException:  
            resp.status = HTTP_404
            resp.media = {"error": "User not found"}
        except Exception as e:  
            resp.status = HTTP_500
            resp.media = {"error": "Internal server error"}

    @falcon.before(Authorize(['Editor', 'Admin', 'Self']))
    def on_put_by_id(self, req, resp, id):
        # update user by id
        try:
            updated_data = req.get_media()
            updated_user = self.dal.update_user_by_id(id, updated_data)
            resp.content_type = MEDIA_JSON
            resp.status = HTTP_200
            resp.media = updated_user
        except NotFoundException:
            resp.status = HTTP_404
            resp.media = {"error": "User not found"}
        except DuplicateException:
            resp.status = HTTP_409
            resp.media = {"error": "Conflicts with existing user"}
        except Exception as e:
            resp.status = HTTP_500
            resp.media = {"error": "Internal server error"}

    @falcon.before(Authorize(['Admin']))
    def on_delete_by_id(self, req, resp, id):
        # delete user by id
        try:
            self.dal.delete_user_by_id(id)
            resp.status = HTTP_204
        except NotFoundException:
            resp.status = HTTP_404
            resp.media = {"error": "User not found"}
        except Exception as e:
            resp.status = HTTP_500
            resp.media = {"error": "Internal server error"}

    @falcon.before(Authorize(['Admin']))
    def on_get_by_role(self, req, resp, role):
        # get users by role
        try:
            users = self.dal.get_users_by_role(role)
            resp.content_type = MEDIA_JSON
            resp.status = HTTP_200
            resp.media = users
        except NotFoundException:   
            resp.status = HTTP_404
            resp.media = {"error": "No users found with the specified role"}
        except Exception as e:
            resp.status = HTTP_500
            resp.media = {"error": "Internal server error"}

    @falcon.before(Authorize(['Admin']))
    def on_get_by_email(self, req, resp, email):
        # get user by email
        try:
            user = self.dal.get_user_by_email(email)
            resp.content_type = MEDIA_JSON
            resp.status = HTTP_200
            resp.media = user
        except NotFoundException:   
            resp.status = HTTP_404
            resp.media = {"error": "User not found"}
        except Exception as e:
            resp.status = HTTP_500
            resp.media = {"error": "Internal server error"}
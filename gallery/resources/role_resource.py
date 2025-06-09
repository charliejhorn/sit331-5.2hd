from pprint import pprint
from falcon import MEDIA_JSON, HTTP_200, HTTP_201, HTTP_404, HTTP_204

class RoleResource:
    def __init__(self, dal) -> None:
        self.dal = dal()

    def on_get(self, req, resp):
        # get all roles
        roles = self.dal.get_all_roles()

        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = roles

    def on_post(self, req, resp):
        # create new role
        new_role = req.get_media()
        pprint(new_role)
        
        created_role = self.dal.add_new_role(new_role)
        
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_201
        resp.media = created_role
        resp.location = '/api/roles/' + str(created_role["id"])

    def on_get_by_id(self, req, resp, id):
        # get role by id
        try:
            role = self.dal.get_role_by_id(id)
            resp.content_type = MEDIA_JSON
            resp.status = HTTP_200
            resp.media = role
        except Exception:
            resp.status = HTTP_404
            resp.media = {"error": "Role not found"}

    def on_put_by_id(self, req, resp, id):
        # update role by id
        try:
            updated_data = req.get_media()
            updated_role = self.dal.update_role_by_id(id, updated_data)
            resp.content_type = MEDIA_JSON
            resp.status = HTTP_200
            resp.media = updated_role
        except Exception:
            resp.status = HTTP_404
            resp.media = {"error": "Role not found"}

    def on_delete_by_id(self, req, resp, id):
        # delete role by id
        try:
            self.dal.delete_role_by_id(id)
            resp.status = HTTP_204
        except Exception:
            resp.status = HTTP_404
            resp.media = {"error": "Role not found"}

    def on_get_by_user(self, req, resp, user_id):
        # get roles by user
        artists = self.dal.get_roles_by_user(user_id)
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200
        resp.media = artists
        
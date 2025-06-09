import falcon

# Authorization Hook
class Authorize:
    def __init__(self, roles):
        self._roles = roles

    def __call__(self, req, resp, resource, params):
        user = req.context.get('user')
        
        # allow self access for user resources when user is authenticated
        if resource.__class__.__name__ == 'UserResource' and user and "id" in params:
            if str(user.id) == str(params["id"]):
                return
        
        # allow access if user has required role
        if user and user.role in self._roles:
            return
            
        # allow unauthenticated access if no roles required (empty list)
        if not self._roles:
            return
            
        # fail authorization
        roles_str = "', '".join(self._roles)
        raise falcon.HTTPForbidden(
            title="Authorization Required",
            description=f"You must have one of the following roles to access this resource: '{roles_str}'"
        )
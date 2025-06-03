import falcon
from gallery.api.routes import register_routes

app = falcon.App()
register_routes(app)
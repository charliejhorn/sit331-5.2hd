import falcon
from wsgiref.simple_server import make_server
from gallery.db.artifact import ArtifactDataAccess
from gallery.resources.artifact import ArtifactResource

app = application = falcon.App()
app.add_route('/api/artifact', ArtifactResource)

if __name__ == "__main__":
    with make_server('', 8000, app) as httpd:
        httpd.serve_forever()
    pass

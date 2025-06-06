import falcon
from wsgiref.simple_server import make_server
from gallery.db import ArtifactDataAccess
from gallery.resources import ArtifactResource

app = application = falcon.App()
app.add_route('/api/artifact', ArtifactResource())

if __name__ == "__main__":
    with make_server('', 8000, app) as httpd:
        print("Open wide, come inside, the server's ready!")
        httpd.serve_forever()
    pass

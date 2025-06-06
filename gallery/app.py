import falcon
import datetime
import json
from functools import partial
from falcon import media

from wsgiref.simple_server import make_server
from gallery.db import ArtifactDataAccess, ArtifactTypeDataAccess, ArtistDataAccess, CommentDataAccess, ExhibitionDataAccess, \
    ImageDataAccess, RegionDataAccess, RoleDataAccess, TribeDataAccess, UserDataAccess
from gallery.resources import ArtifactResource, ArtifactTypeResource, ArtistResource, CommentResource, ExhibitionResource, \
    ImageResource, RegionResource, RoleResource, TribeResource, UserResource
from gallery.utils import datetime_serializer, datetime_deserializer

class HelloWorldResource:
    def on_get(self, req, resp):
        resp.media = {"message": "Open wide, come inside, Hello World!"}

# add serialization and deserialization for datetime objects
json_handler = media.JSONHandler(
    dumps=partial(
        json.dumps,
        default=datetime_serializer,
        sort_keys=True,
        ensure_ascii=False
    ),
    loads=partial(
        json.loads,
        object_hook=datetime_deserializer,
    )
)
extra_handlers = {
    'application/json': json_handler,
}

app = application = falcon.App()

# register datetime serialization handlers
app.resp_options.media_handlers.update(extra_handlers)
app.req_options.media_handlers.update(extra_handlers)

# add routes
app.add_route('/', HelloWorldResource())

app.add_route('/api/artifacts', ArtifactResource(ArtifactDataAccess))
app.add_route('/api/artifact-types', ArtifactTypeResource(ArtifactTypeDataAccess))
app.add_route('/api/artists', ArtistResource(ArtistDataAccess))
app.add_route('/api/comments', CommentResource(CommentDataAccess))
app.add_route('/api/exhibitions', ExhibitionResource(ExhibitionDataAccess))
app.add_route('/api/images', ImageResource(ImageDataAccess))
app.add_route('/api/regions', RegionResource(RegionDataAccess))
app.add_route('/api/roles', RoleResource(RoleDataAccess))
app.add_route('/api/tribes', TribeResource(TribeDataAccess))
app.add_route('/api/users', UserResource(UserDataAccess))

if __name__ == "__main__":
    with make_server('', 8000, app) as httpd:
        print("Open wide, come inside, the server's ready!")
        httpd.serve_forever()
    pass

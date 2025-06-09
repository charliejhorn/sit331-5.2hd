import falcon
import datetime
import json
from functools import partial
from falcon import media

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

# sample URLs
# filtering:     https://gw.api.gov.au/e09284/v1/employees?year=2011&sort=desc
# single entity: https://gw.api.gov.au/e09284/v1/employees/0d047d80-eb69-4665-9395-6df5a5e569a4

# add routes
app.add_route('/', HelloWorldResource())

# artifacts
app.add_route('/api/artifacts', ArtifactResource(ArtifactDataAccess())) 
app.add_route('/api/artifacts/{id:int}', ArtifactResource(ArtifactDataAccess()), suffix='by_id') 
app.add_route('/api/artifacts?type={artifact_type_id:int}', ArtifactResource(ArtifactDataAccess()), suffix='by_type')
app.add_route('/api/artifacts?year={year:int}', ArtifactResource(ArtifactDataAccess()), suffix='by_year') 
app.add_route('/api/artifacts?display_location={display_location}', ArtifactResource(ArtifactDataAccess()), suffix='by_location') 
app.add_route('/api/artifacts?start_date={start_date}&end_date={end_date}', ArtifactResource(ArtifactDataAccess()), suffix='by_date') 

# artifact types
app.add_route('/api/artifact-types', ArtifactTypeResource(ArtifactTypeDataAccess()))
app.add_route('/api/artifact-types/{id:int}', ArtifactTypeResource(ArtifactTypeDataAccess()), suffix='by_id') 

# artists
app.add_route('/api/artists', ArtistResource(ArtistDataAccess()))
app.add_route('/api/artists/{id:int}', ArtistResource(ArtistDataAccess()), suffix='by_id') 
app.add_route('/api/artists?region={region_id:int}', ArtistResource(ArtistDataAccess()), suffix='by_region')
app.add_route('/api/artists?tribe={tribe_id:int}', ArtistResource(ArtistDataAccess()), suffix='by_tribe')

# comments
app.add_route('/api/comments', CommentResource(CommentDataAccess())) 
app.add_route('/api/comments/{id:int}', CommentResource(CommentDataAccess()), suffix='by_id') 
app.add_route('/api/comments?artifact={artifact_id:int}', CommentResource(CommentDataAccess()), suffix='by_artifact') 
app.add_route('/api/comments?author={user_id:int}', CommentResource(CommentDataAccess()), suffix='by_user') 
app.add_route('/api/comments?artifact={artifact_id:int}&author={user_id:int}', CommentResource(CommentDataAccess()), suffix='by_artifact_and_user') 
app.add_route('/api/comments?start_date={start_date}&end_date={end_date}', CommentResource(CommentDataAccess()), suffix='by_date') 
app.add_route('/api/comments?parent_comment={parent_comment_id:int}', CommentResource(CommentDataAccess()), suffix='by_parent_comment') 

# exhibitions
app.add_route('/api/exhibitions', ExhibitionResource(ExhibitionDataAccess()))
app.add_route('/api/exhibitions/{id:int}', ExhibitionResource(ExhibitionDataAccess()), suffix='by_id') 
app.add_route('/api/exhibitions?date={date}', ExhibitionResource(ExhibitionDataAccess()), suffix='by_date') 
app.add_route('/api/exhibitions?location={location}', ExhibitionResource(ExhibitionDataAccess()), suffix='by_location') 

# images
app.add_route('/api/images', ImageResource(ImageDataAccess()))
app.add_route('/api/images/{id:int}', ImageResource(ImageDataAccess()), suffix='by_id')
app.add_route('/api/images?artifact={artifact_id:int}', ImageResource(ImageDataAccess()), suffix='by_artifact') 

#regions 
app.add_route('/api/regions', RegionResource(RegionDataAccess()))
app.add_route('/api/regions/{id:int}', RegionResource(RegionDataAccess()), suffix='by_id')

# roles
app.add_route('/api/roles', RoleResource(RoleDataAccess()))
app.add_route('/api/roles/{id:int}', RoleResource(RoleDataAccess()), suffix='by_id')

# tribes
app.add_route('/api/tribes', TribeResource(TribeDataAccess()))
app.add_route('/api/tribes/{id:int}', TribeResource(TribeDataAccess()), suffix='by_id')
app.add_route('/api/tribes?region={region_id:int}', TribeResource(TribeDataAccess()), suffix='by_region')

# users
app.add_route('/api/users', UserResource(UserDataAccess()))
app.add_route('/api/users/{id:int}', UserResource(UserDataAccess()), suffix='by_id')
app.add_route('/api/users?role={role}', UserResource(UserDataAccess()), suffix='by_role')
app.add_route('/api/users?email={email}', UserResource(UserDataAccess()), suffix='by_email')

# start server (not used by gunicorn)
if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    with make_server('', 8000, app) as httpd:
        print("Open wide, come inside, the server's ready!")
        httpd.serve_forever()
    pass

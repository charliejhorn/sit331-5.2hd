import falcon
import datetime
import json
from functools import partial
from falcon import media

from wsgiref.simple_server import make_server
from gallery.db import ArtifactDataAccess
from gallery.resources import ArtifactResource
from gallery.utils import datetime_serializer, datetime_deserializer

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

app.resp_options.media_handlers.update(extra_handlers)
app.req_options.media_handlers.update(extra_handlers)

app.add_route('/api/artifacts', ArtifactResource())


if __name__ == "__main__":
    with make_server('', 8000, app) as httpd:
        print("Open wide, come inside, the server's ready!")
        httpd.serve_forever()
    pass

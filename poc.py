from wsgiref.simple_server import make_server

import falcon

class HelloWorld:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_TEXT
        resp.text = "Hello World!"
        pass

def main(): 
    app = falcon.App()

    controller = HelloWorld()

    app.add_route("/api/hello-world", controller)

    with make_server('', 8000, app) as httpd:
        httpd.serve_forever()
        pass

    pass


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nFuck you goodbye")
        pass # good spot for any closing logic that might be needed, or a fuck you goodbye message
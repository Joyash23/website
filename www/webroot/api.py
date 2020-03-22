from quickweb import controller
from os import environ
from cherrypy import HTTPError
import requests

API_URL = environ["API_URL"]


class Controller(object):
    @controller.publish
    def default(self, *args, **kwargs):
        path = '/'.join(args)
        if controller.method == "POST":
            email = controller.get_session_value("email")
            if not email:
                raise HTTPError(400, "Session is invalid")
            url = f"{API_URL}/"+path
            return requests.post(url, kwargs)
        if controller.method == "GET":
            if path != "provider/login":
                raise HTTPError(400, "Invalid method")
            return requests.get(url, kwargs)
        raise HTTPError(400, "Invalid method")


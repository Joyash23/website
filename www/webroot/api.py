from quickweb import controller
from os import environ
from cherrypy import HTTPError
import requests
import json

API_URL = environ["API_URL"]

ANONYMOUS_PATHS = ["api/help/request", "provider/login"]


class Controller(object):
    @controller.publish
    def default(self, *args, **kwargs):
        path = "/".join(args)
        if kwargs:
            kwargs["lang"] = controller.get_lang()
        if path not in ANONYMOUS_PATHS:
            email = controller.get_session_value("email")
            if not email:
                raise HTTPError(400, "Session is invalid")
        url = f"{API_URL}/" + path
        if controller.method() == "POST":
            result = requests.post(url, kwargs)
        elif controller.method() == "GET":
            result = requests.get(url, kwargs)
        else:
            raise HTTPError(400, "Invalid method")
        result.raise_for_status()
        return result.json()

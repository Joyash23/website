from quickweb import controller
from os import environ
from cherrypy import HTTPError
import requests

API_URL = environ["API_URL"]


class Controller(object):
    @controller.publish
    def default(self, *args, **kwargs):
        path = "/".join(args)
        if kwargs:
            kwargs["lang"] = controller.get_lang()
        if controller.method() == "POST":
            if path != "provider/login":
                email = controller.get_session_value("email")
                if not email:
                    raise HTTPError(400, "Session is invalid")
            url = f"{API_URL}/" + path
            result = requests.post(url, kwargs)
            result.raise_for_status()
            return result.json()
        raise HTTPError(400, "Invalid method")

from quickweb import controller
from os import environ
import urllib
import json
import cherrypy
from cherrypy import HTTPError
from urllib.error import URLError
import jwt

JWT_SECRET = environ["JWT_SECRET"]


class Controller(object):
    @controller.publish
    def index(self, email, token):
        API_URL = environ["API_URL"]
        url = f"{API_URL}/provider/check?email={email}&token={token}"
        try:
            request = urllib.request.urlopen(url)
        except URLError:
            raise HTTPError(500, "Error calling the API server")
        data = request.read().decode("utf-8")
        json_data = json.loads(data)
        cherrypy.session["email"] = json_data["email"]
        jwt_token = jwt.encode(json_data, JWT_SECRET, algorithm="HS256")
        jwt_token = jwt_token.decode("utf-8")
        cookie = cherrypy.response.cookie
        cookie["PROVIDER_DATA"] = jwt_token
        cookie["PROVIDER_DATA"]["max-age"] = 43200  # 30 days
        return controller.redirect("/provider/profile")

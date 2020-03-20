from quickweb import controller
from os import environ
import urllib
import jwt
import json
import cherrypy


JWT_SECRET = environ["JWT_SECRET"]


class Controller(object):
    @controller.publish
    def index(self, email, token):
        API_URL = environ["API_URL"]
        url = f"{API_URL}/provider/check?email={email}&token={token}"
        request = urllib.request.urlopen(url)
        data = request.read().decode("utf-8")
        json_data = json.loads(data)
        cookie = cherrypy.response.cookie
        encoded_data = jwt.encode(
            json_data, JWT_SECRET, algorithm="HS256"
        )
        cookie["PROVIDER_DATA"] = encoded_data
        print("JOIN", encoded_data.decode('utf-8'))
        cookie["PROVIDER_DATA"]["max-age"] = 43200  # 30 days
        return controller.redirect("/provider/profile")


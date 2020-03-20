from quickweb import controller
from os import environ
import urllib
import jwt
import json
import cherrypy


JWT_SECRET = environ["JWT_SECRET"]


class Controller(object):
    @controller.publish
    def index(self, ):
        #API_URL = environ["API_URL"]
        cookie = cherrypy.request.cookie
        cookie_data = cookie["PROVIDER_DATA"].value
        print("CWD", str(cookie_data))
        print(jwt.decode(cookie_data, JWT_SECRET,  algorithms=['HS256']))
        return (cookie["PROVIDER_DATA"])

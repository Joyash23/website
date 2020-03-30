import cherrypy
import requests
from cherrypy import HTTPError
from quickweb import controller
from os import environ

API_URL = environ["API_URL"]
GITHOOK_SECRET = environ['GITHOOK_SECRET']

class Controller(object):

    @controller.publish
    @cherrypy.tools.json_in()
    def index(self):
        # try:
        #     secret = cherrypy.request.json['hook']['config']['secret']
        # except KeyError:
        #     raise HTTPError(400)
        # if secret != GITHOOK_SECRET:
        #     raise HTTPError(400)
        url = f"{API_URL}/shutdown"
        result = requests.get(url)
        cherrypy.engine.exit()
import cherrypy
import requests
import hmac
import hashlib
from cherrypy import HTTPError
from quickweb import controller
from os import environ

API_URL = environ["API_URL"]
GITHOOK_SECRET = environ['GITHOOK_SECRET']

class Controller(object):

    @controller.publish
    def index(self):
        try:
            signature = cherrypy.request.headers['X-Hub-Signature']
        except KeyError:
            raise HTTPError(400)
        payload =  cherrypy.request.body.read()
        hmac_gen = hmac.new(GITHOOK_SECRET.encode(), payload, hashlib.sha1)
        digest = "sha1=" + hmac_gen.hexdigest()
        if not hmac.compare_digest(digest, signature):
            raise HTTPError(400)
        url = f"{API_URL}/shutdown"
        try:
            result = requests.get(url)
        except requests.ConnectionError:
            pass
        cherrypy.engine.exit()

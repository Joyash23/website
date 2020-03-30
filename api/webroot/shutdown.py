import cherrypy
from quickweb import controller

class Controller(object):

    @controller.publish
    def index(self):
        cherrypy.engine.exit()
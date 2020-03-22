from quickweb import controller
import json
import cherrypy


class Controller(object):
    @controller.publish
    @cherrypy.tools.json_out()
    def index(self, email, lang):
        help_requests = controller.lib.db.get_help_requests(email)
        return json.dumps(help_requests)

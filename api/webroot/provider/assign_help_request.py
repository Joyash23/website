from quickweb import controller
import json
import cherrypy


class Controller(object):
    @controller.publish
    @cherrypy.tools.json_out()
    def index(self, **kwargs):
        email = kwargs.get("email")
        help_request_id = int(kwargs.get("help_request_id"))

        help_request = controller.lib.db.assign_help_request(email, help_request_id)
        return json.dumps(help_request)

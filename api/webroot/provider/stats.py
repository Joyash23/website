import cherrypy
from quickweb import controller
import json


class Controller(object):
    @controller.publish()
    @cherrypy.tools.json_out()
    def default(self, *args, **kwargs):
        providers_count = controller.lib.db.get_providers_count()[0]
        help_requests_count = controller.lib.db.get_help_requests_count()[0]
        data = {
            "providers_count": providers_count,
            "help_requests_count": help_requests_count,
        }
        print(data)
        return json.dumps(data)

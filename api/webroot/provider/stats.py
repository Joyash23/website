import cherrypy
from quickweb import controller
import json


class Controller(object):
    @controller.publish()
    @cherrypy.tools.json_out()
    def default(self, *args, **kwargs):
        providers_count = controller.lib.db.get_providers_count()[0]
        requests_count = controller.lib.db.get_help_requests_count()[0]
        return json.dumps(
            {"providers_count": providers_count, "requests_count": requests_count}
        )

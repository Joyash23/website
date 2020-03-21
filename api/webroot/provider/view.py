from quickweb import controller
import json


class Controller(object):
    @controller.publish
    def index(self, email):
        help_requests = controller.lib.db.get_help_requests()
        return json.dumps(help_requests)

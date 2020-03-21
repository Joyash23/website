from quickweb import controller
from cherrypy import HTTPError
import json


class Controller(object):
    @controller.publish
    def index(self, email, token):
        check_result = controller.lib.db.get_provider(email, token)
        if check_result is None:
            raise HTTPError(403, "Invalid email/token")
        return json.dumps({"email": email, "token": token})

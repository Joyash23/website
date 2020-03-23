from quickweb import controller
from cherrypy import HTTPError
from os import environ
import re
import secrets
import json
import cherrypy


class Controller(object):
    def __init__(self):
        self.email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")

    @controller.publish
    @cherrypy.tools.json_out()
    def index(self, email, lang):

        if not self.email_regex.match(email):
            raise HTTPError(400, "Email adress is not valid")
        controller.lib.db.get_provider(email)
        token = secrets.token_hex(16)
        action_name = "provider/join"
        controller.lib.db.insert_or_replace_provider(email, lang, token)
        action_link = self.gen_action_link(action_name, email, lang, token)
        controller.lib.mail.send(email, action_name, lang, action_link=action_link)
        return json.dumps({"status": "OK"})

    def gen_action_link(self, action, email, lang, token):
        c = controller.helpers()
        domain = environ["WEB_DOMAIN"]

        return (
            f"{c['scheme']()}://{lang}.{domain}/"
            + f"{action}?email={email}&token={token}"
        )

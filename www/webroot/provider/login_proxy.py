import urllib
from quickweb import controller
from os import environ


class Controller(object):

    @controller.publish
    def index(self, email):
        API_URL = environ["API_URL"]
        lang = controller.get_lang()
        url = f"{API_URL}/provider/login?email={email}&lang={lang}"
        return urllib.request.urlopen(url)
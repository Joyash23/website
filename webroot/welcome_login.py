from quickweb import controller
import urllib
from os import environ


class Controller(object):

    @controller.publish
    def index(self, email, token):
        API_URL = environ['API_URL']
        url = f'{API_URL}/provider_check/email={email}&token={token}'
        request = urllib.request.urlopen(url)
        response = request.read().decode('utf-8')
        print(response)

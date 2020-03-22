import re
from quickweb import controller
from cherrypy import HTTPError


class Controller(object):
    def __init__(self):
        self.email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")

    @controller.publish
    def index(self, fname, zipcode, phone, **kwargs):
        email = kwargs.get("email", None)
        category = kwargs.get("category", [])
        language = kwargs.get("language", [])
        additional_info = kwargs.get("additional_info", None)

        if controller.lib.db.check_zip_code(zipcode) is None:
            raise HTTPError(400, "Uknown zip code")

        if type(language) in (tuple, list):
            language = "|".join(language)

        if type(category) in (tuple, list):
            category = "|".join(category)

        controller.lib.db.insert_seeker_request(
            fname,
            email,
            phone,
            language,
            zipcode,
            category,
            additional_info,
        )
        return "OK"

from quickweb import controller
import re


class Controller(object):
    def __init__(self):
        self.email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")

    @controller.publish
    def request(self, fname, zipcode, phone, **kwargs):
        email = kwargs.get("email", None)
        category = kwargs.get("category", [])
        language = kwargs.get("language", [])
        additional_info = kwargs.get("additional_info", None)
        controller.lib.db.insert_seeker_request(
            fname,
            email,
            phone,
            "|".join(language),
            zipcode,
            "|".join(category),
            additional_info,
        )
        return "OK"

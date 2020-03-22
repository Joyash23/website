import re
import json
from quickweb import controller
from cherrypy import HTTPError
from os import environ
import cherrypy


class Controller(object):
    def __init__(self):
        self.email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")

    @cherrypy.tools.json_out()
    @controller.publish
    def default(self, *args, **kwargs):
        fname = kwargs.get("fname", None)
        zipcode = kwargs.get("zipcode", None)
        phone = kwargs.get("phone", None)
        email = kwargs.get("email", None)
        category = kwargs.get("category", [])
        language = kwargs.get("language", [])
        additional_info = kwargs.get("additional_info", None)

        if controller.lib.db.check_zip_code(zipcode) is None:
            raise HTTPError(400, "Uknown zip code")

        if type(language) in (tuple, list):
            if language.__len__() == 0:
                language = controller.get_lang()
            else:
                language = "|".join(language)

        if type(category) in (tuple, list):
            category = "|".join(category)

        self.add_seeker_request(
            additional_info, category, email, fname, language, phone, zipcode
        )
        self.notify_providers(email, language, zipcode)

        return json.dumps({"status": "OK"})

    def notify_providers(self, email, language, zipcode):
        action_name = "provider/new_help_request"
        providers = self.find_providers_by_zipcode_and_language_to_notify(
            zipcode, language
        )
        for provider in providers:
            view_help_requests_link = self.generate_view_help_requests_link(
                provider.lang
            )
            controller.lib.mail.send(
                provider.email,
                action_name,
                provider.lang,
                view_help_requests_link=view_help_requests_link,
            )

    def generate_view_help_requests_link(self, lang):
        c = controller.helpers()
        domain = environ["WEB_DOMAIN"]

        return f"{c['scheme']()}://{lang}.{domain}/provider/view"

    def find_providers_by_zipcode_and_language_to_notify(self, zipcode, language):
        providers = controller.lib.db.get_providers(zipcode, 1)
        providers = list(
            filter(self.speaks_one_of_requested_languages(language), providers)
        )
        return providers

    def speaks_one_of_requested_languages(self, language):
        return (
            lambda provider: list(
                set(language.split("|")) & set(provider.language.split("|"))
            ).__len__()
            > 0
        )

    def add_seeker_request(
        self, additional_info, category, email, fname, language, phone, zipcode
    ):
        controller.lib.db.insert_seeker_request(
            fname, email, phone, language, zipcode, category, additional_info,
        )

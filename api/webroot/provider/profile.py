from quickweb import controller
import json


class Controller(object):
    @controller.publish
    def index(self, *args, **kwargs):
        zipcode = int(kwargs.get("zipcode"))
        email = kwargs.get("email")
        language = kwargs.get("language", [])
        category = kwargs.get("category", [])
        notify = kwargs.get("notify")

        if type(language) in (tuple, list):
            language = "|".join(language)

        if type(category) in (tuple, list):
            category = "|".join(category)

        # Read email from user session
        controller.lib.db.update_provider(email, zipcode, language, category, notify)
        return json.dumps({"status": "OK "})

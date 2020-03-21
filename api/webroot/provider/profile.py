from quickweb import controller


class Controller(object):
    @controller.publish
    def index(self, zipcode, **kwargs):
        email = kwargs.get("email")
        languages = "|".join(kwargs.get("language", []))
        category = "|".join(kwargs.get("category", []))
        notify = kwargs.get("notify")

        # Read email from user session
        controller.lib.db.update_provider(email, zipcode, languages, category, notify)
        return "OK"

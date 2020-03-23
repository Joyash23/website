import cherrypy


def start():
    app_config = {
        "tools.response_headers.on": True,
        "tools.response_headers.headers": [("Access-Control-Allow-Origin", "*")],
    }

    cherrypy.config.update(app_config)

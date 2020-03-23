import cherrypy


def start():
    cherrypy.config.update({"tools.sessions.on": True})

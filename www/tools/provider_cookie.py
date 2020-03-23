import cherrypy
import jwt
from os import environ

JWT_SECRET = environ["JWT_SECRET"]


@cherrypy.tools.register("before_handler", priority=60)
def provider_cookie():

    # Was authenticated in the current session ?
    if "email" in cherrypy.session:
        return

    # An authentication cookie is set ?
    try:
        jwt_token = cherrypy.request.cookie["PROVIDER_DATA"].value
    except KeyError:  # Cookie is not set
        return
    try:
        encrypted_data = jwt.decode(jwt_token, JWT_SECRET, algorithm="HS256")
    except jwt.exceptions.InvalidSignatureError:  # Invalid token
        return
    # Set the session as authenticated
    cherrypy.session["email"] = encrypted_data["email"]

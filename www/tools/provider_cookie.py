import cherrypy
import jwt
from os import environ

JWT_SECRET = environ["JWT_SECRET"]


@cherrypy.tools.register("before_handler", priority=60)
def provider_cookie():
    cookie = cherrypy.request.cookie
    try:
        jwt_token = cookie["PROVIDER_DATA"].value
    except KeyError:    # Cookie is not set
        return
    try:
        payload = jwt.decode(jwt_token, JWT_SECRET, algorithm="HS256")
    except jwt.exceptions.InvalidSignatureError:  # Ignore invalid stokens
        return
    cherrypy.session["email"] = payload['email']

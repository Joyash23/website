import smtplib
import yaml
from email.message import EmailMessage
from os.path import join, exists, basename
from cherrypy import HTTPError
from os import environ
from quickweb.features.web.templates import TemplateEngine
from jinja2.exceptions import TemplateNotFound


MAILS_DIR = "mails"
template_engine = TemplateEngine(MAILS_DIR)

SMTP_SERVER = environ.get("SMTP_SERVER")


def send(email, filename, lang, **kwargs):
    # must check for available lang templates before calling send_raw
    for look_for in [filename, filename + "_" + lang]:
        try:
            send_raw(email, f"{look_for}.yaml", lang, **kwargs)
        except TemplateNotFound:
            pass
        else:
            return

    raise HTTPError(500, f"Mail template {filename} not found")


def send_raw(email, filename, lang, **kwargs):
    mail_txt_data = template_engine.render(filename, lang, **kwargs)
    mail_data = yaml.safe_load(mail_txt_data)

    msg = EmailMessage()
    msg["Subject"] = mail_data["subject"]
    msg["From"] = mail_data["sender"]
    msg["To"] = email
    msg.set_content(mail_data["message"])

    # Send the message via  SMTP server.
    if SMTP_SERVER:
        s = smtplib.SMTP(SMTP_SERVER)
        s.send_message(msg)
        s.quit()
    else:
        print(msg)

import flask_mail
from flask_login import current_user
from . import mail_mgr


def send_email(body):
    msg = flask_mail.Message(
        sender='apptrak20@gmail.com',
        recipients=current_user.email,
        body=body
    )
    mail_mgr.send(msg)


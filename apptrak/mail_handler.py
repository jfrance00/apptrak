import flask
import flask_mail
from flask_login import current_user
from . import mail_mgr
from ..wsgi import app


def send_email(body):
    msg = flask_mail.Message(
        sender='apptrak20@gmail.com',
        recipients=current_user.email,
        body=body
    )
    mail_mgr.send(msg)


def send_password_link(email):
    url = flask.url_for('blueprints.auth.views.reset_password')
    msg = flask_mail.Message(
        subject="Password Reset",
        sender=app.config['MAIL_USERNAME'],
        recipients=current_user.email,
        body=f'Hello, To reset your password please click on the link: {url}'
    )
    mail_mgr.send(msg)

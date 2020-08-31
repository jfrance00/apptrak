import flask
import flask_mail
from flask_login import current_user
from . import mail_mgr
import os

path = 'C:\\Users\\Julie\\Desktop\\apptrak'
os.chdir(path)

from wsgi import app

os.chdir("C:\\Users\\Julie\\Desktop\\apptrak\\apptrak")


def send_email(body):
    msg = flask_mail.Message(
        sender='apptrak20@gmail.com',
        recipients=current_user.email,
        body=body
    )
    mail_mgr.send(msg)


def send_password_link(email, token):
    url = flask.url_for('blueprints.auth.views.reset_password')
    payload = {token, app.config['SECRET_KEY']}
    msg = flask_mail.Message(
        subject="Password Reset",
        sender=app.config['MAIL_USERNAME'],
        recipients=[email],
        body=f'Hello, To reset your password please click on the link: {url}'
    )
    mail_mgr.send(msg)

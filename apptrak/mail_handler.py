import flask
import flask_mail
from flask_login import current_user
from . import mail_mgr
import jwt
import os
import datetime
from flask import current_app


# path = 'C:\\Users\\Julie\\Desktop\\apptrak'
# os.chdir(path)
#
# from wsgi import app
#
# os.chdir("C:\\Users\\Julie\\Desktop\\apptrak\\apptrak")


def send_email(body):
    msg = flask_mail.Message(
        sender='apptrak20@gmail.com',
        recipients=current_user.email,
        body=body
    )
    mail_mgr.send(msg)


def send_password_link(email, user):
    payload = {
        'user_id': user.id,
        'expires': (datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp()
               }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'])
    print(token)
    url = flask.url_for('auth.reset_password', jwt_token=token, _external=True)
    msg = flask_mail.Message(
        subject="Password Reset",
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[email],
        body=f'Hello, To reset your password please click on the link: {url}'
    )
    mail_mgr.send(msg)
    print("message sent")

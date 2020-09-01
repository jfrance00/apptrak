import flask
from flask_login import logout_user, current_user, login_required
from . import forms, auth
from .models import User
from ... import db
from ...mail_handler import send_password_link
import jwt
import os


path = 'C:\\Users\\Julie\\Desktop\\apptrak'
os.chdir(path)

from wsgi import app





@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.Register()
    if flask.request.method == "POST":
    # if form.validate_on_submit():
        user = User(
            name=form.name.data,
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)            #TODO write saving to db as User method
        db.session.commit()
        flask.flash('User registered')
        return "user registered"
    return flask.render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.Login()
    if flask.request.method == 'POST':
        email = form.email.data
        password = form.password.data
        if User.authenticate(email, password):
            print(current_user)
            return flask.redirect('index')  # TODO change redirect to user page
        else:
            flask.flash("Username or password invalid")
            return flask.redirect('login')
    return flask.render_template('login.html', form=form)


@auth.route('/user-info', methods=['GET', 'POST'])
@login_required
def user_info():
    user = current_user
    return flask.render_template('user-info.html', user=user)


@auth.route('/logout')
def logout():
    logout_user()
    return flask.redirect('index')


@auth.route('/request-password', methods=['GET', 'POST'])
def request_password():
    form = forms.PasswordResetEmail()
    if flask.request.method == 'POST':
        email = form.email.data                          # TODO use email to id user and send email
        user = User.query.filter_by(email=email).first()
        if user:
            payload = {'user_id': user.id}
            token = jwt.encode(payload, app.config['SECRET_KEY'])
            url = flask.url_for('auth.reset_password', jwt_token=token)
            print(url)
            flask.flash("Password reset email sent")
            return flask.render_template('index.html')
        else:
            flask.flash("No account with that email address")
            return flask.redirect('login')
    return flask.render_template('password_request.html', form=form)


@auth.route('/reset-password/<jwt_token>', methods=['GET', 'POST'])
def reset_password(token):
    form = forms.PasswordReset()
    return 'password reset'





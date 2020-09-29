import flask
from flask_login import login_user, logout_user, current_user, login_required
from . import forms, auth
from .models import User
from ... import db, sort_data
from ...mail_handler import send_password_link
import jwt
import datetime
import os
from flask import current_app

# path = 'C:\\Users\\Julie\\Desktop\\apptrak'
# os.chdir(path)
#
# from wsgi import app
#
# os.chdir('C:\\Users\\Julie\\Desktop\\apptrak\\apptrak\\blueprints\\auth')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.Register()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)            #TODO write saving to db as User method
        db.session.commit()
        flask.flash('User registered', category="success")
        return flask.redirect('login')
    else:
        for error in form.errors.items():
            flask.flash(error[1][0], category='warning')
    return flask.render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.Login()
    if flask.request.method == 'POST':
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if User.authenticate(email, password):
            login_user(user, remember=True)       #TODO add option to be remembered in login form (default to True)
            return flask.redirect('/user-info')
        else:
            return flask.redirect('login')
    return flask.render_template('login.html', form=form)


@auth.route('/user-info', methods=['GET', 'POST'])
@login_required
def user_info():
    user = current_user
    num_apps = len(sort_data.remove_archived())
    return flask.render_template('user-info.html', user=user, num_apps=num_apps)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return flask.redirect('index')


@auth.route('/request-password', methods=['GET', 'POST'])
def request_password():
    form = forms.PasswordResetEmail()
    if flask.request.method == 'POST':
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            send_password_link(email, user)
            flask.flash("Password reset email sent", category="success")
            return flask.render_template('index.html')
        else:
            flask.flash("No account with that email address", category="danger")
            return flask.redirect('login')
    return flask.render_template('password_request.html', form=form)


@auth.route('/reset-password/<jwt_token>', methods=['GET', 'POST'])
def reset_password(jwt_token):
    payload = jwt.decode(jwt_token, current_app.config['SECRET_KEY'])
    user = User.query.filter_by(id=payload['user_id']).first()

    if datetime.datetime.now().timestamp() < payload['expires']:      # loop checks if token valid
        form = forms.PasswordReset()
    else:
        flask.flash("token expired. Try again", category="error")

    if flask.request.method == 'POST':
        password = form.password.data
        user.update_password(password)
        flask.flash("password successfully reset", category="success")
        return flask.redirect('/login')
    return flask.render_template('password_reset.html', form=form, user=user)





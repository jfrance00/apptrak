import flask
from flask_login import logout_user, current_user
from . import forms, auth
from .models import User
from ... import db


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
            return flask.redirect('index') #TODO change redirect to user page
        else:
            flask.flash("Username or password invalid")
            return flask.redirect('login')
    return flask.render_template('login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    print(current_user)
    return flask.redirect('index')

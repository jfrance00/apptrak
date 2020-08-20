import wtforms as wtf
import flask_wtf
from wtforms import validators as valid

class Register(flask_wtf.FlaskForm):
    name = wtf.StringField('Name', [valid.InputRequired()])
    username = wtf.StringField("Username", [valid.InputRequired()])
    email = wtf.StringField('Email', [valid.Email()])
    password = wtf.PasswordField('Password', [valid.InputRequired()])
    confirm_pass = wtf.PasswordField('Confirm Password', [valid.EqualTo(password)])
    submit = wtf.SubmitField("Register")


class Login(flask_wtf.FlaskForm):
    email = wtf.StringField('Email', [valid.Email()])
    password = wtf.PasswordField('Password', [valid.InputRequired()])
    submit = wtf.SubmitField('Login')


from ... import db, login_mgr
from flask_login import UserMixin
import flask_login
from ..jobapps.models import JobApplication


@login_mgr.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(40))
    job_applications = db.relationship('JobApplication', backref='user')

    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter_by(email=email).first()
        if user.password == password:
            flask_login.login_user(user)
            return True
        else:
            return False

    def update_password(self):
        pass

    def change_email(self):
        pass








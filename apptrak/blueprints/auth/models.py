from ... import db, login_mgr, create_app
from flask_login import UserMixin
import flask_login
import time
import jwt
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
            flask_login.login_user(user, remember=True)
            return True
        else:
            return False

    def get_reset_password_token(self, expires_in=600):
        timeout = time.time() + expires_in
        payload = {
            'reset_password': self.id,
            'exp': timeout
        }

        # Get the secret key from config
        app = create_app()
        secret_key = app.config['SECRET_KEY']

        # Create the token
        token = jwt.encode(payload, secret_key, algorithm="HS256")

        # Turn it to string
        s_token = token.decode('utf-8')

        return s_token

    def update_password(self):
        pass

    def change_email(self):
        pass








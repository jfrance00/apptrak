import flask
import flask_sqlalchemy
import flask_migrate
import flask_login
import flask_mail
import psycopg2
import os


basedir = os.path.abspath(
    os.path.dirname(__file__)
)

db = flask_sqlalchemy.SQLAlchemy()
migrate = flask_migrate.Migrate()
login_mgr = flask_login.LoginManager()
mail_mgr = flask_mail.Mail()


def create_app(default_env='development'):
    from config import config
    from . import views
    from .blueprints.auth.views import auth
    from .blueprints.auth.models import User
    from .blueprints.landing import landing
    from .blueprints.jobapps.views import jobapps

    app = flask.Flask(__name__)
    env = os.environ.get("FLASK_ENV", default_env)
    app.config.from_object(config[env])
    db.init_app(app)
    migrate.init_app(app, db)
    login_mgr.init_app(app)
    mail_mgr.init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(landing)
    app.register_blueprint(jobapps)

    return app








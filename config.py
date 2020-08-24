import os


basedir = os.path.abspath(
    os.path.dirname(__file__)
)

class Config:
    pass


class DevConfig(Config):
    SECRET_KEY = os.urandom(24)

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587                   # if use SSL instead change to 465
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'apptrak20@gmail.com'  # TODO don't hard code name and passwords
    MAIL_PASSWORD = 'th!si$apassw0rd'


class ProdConfig(Config):
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")


config = {
    "development": DevConfig,
    "production": ProdConfig
}

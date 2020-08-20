import os


basedir = os.path.abspath(
    os.path.dirname(__file__)
)

class Config:
    pass


class DevConfig(Config):
    SECRET_KEY = "arandomsecretkey"

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'julie@mail.com'
    MAIL_PASSWORD = 'Chocolate111'


class ProdConfig(Config):
    SECRET_KEY = "1265ewqtfsdaxvgz9287ynx918u2nx8172m301u9"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")


config = {
    "development": DevConfig,
    "production": ProdConfig
}

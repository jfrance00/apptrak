import flask

# from .blueprints import auth
from .blueprints.landing import landing


@landing.route('/')
@landing.route('/index')
def index():
    return flask.render_template('index.html')

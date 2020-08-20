import flask

landing = flask.Blueprint('landing', __name__,
                          template_folder='templates')

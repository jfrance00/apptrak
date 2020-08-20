import flask


jobapps = flask.Blueprint('jobapps', __name__,
                          template_folder='templates')

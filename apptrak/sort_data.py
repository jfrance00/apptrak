import flask
from flask_login import current_user


def sorting_feature(field):
    user_apps = current_user.job_applications
    sorted_applications = [app.__json__() for app in filter(lambda app: getattr(app, field), user_apps)]
    return sorted_applications

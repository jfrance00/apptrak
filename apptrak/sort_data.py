import flask
from flask_login import current_user


def single_sorting_feature(field):
    user_apps = current_user.job_applications
    print(user_apps)
    sorted_applications = [app.__json__() for app in filter(lambda app: getattr(app, field), user_apps)]
    print(sorted_applications)
    return sorted_applications


def double_sorting_feature(sort_list):
    user_apps = current_user.job_applications
    sorted_applications = [app.__json__() for app in filter(lambda app: getattr(app, sort_list[0]) and getattr(app, sort_list[1]), user_apps)]
    return sorted_applications


def triple_sorting_feature(sort_list):
    user_apps = current_user.job_applications
    sorted_applications = [app.__json__() for app in filter(lambda app: getattr(app, sort_list[0])
                                          and getattr(app, sort_list[1]) and getattr(app, sort_list[2]), user_apps)]
    return sorted_applications


def quad_sorting_feature(sort_list):
    user_apps = current_user.job_applications
    sorted_applications = [app.__json__() for app in filter(lambda app: getattr(app, sort_list[0])
                                          and getattr(app, sort_list[1]) and getattr(app, sort_list[2])
                                          and getattr(app, sort_list[3]), user_apps)]
    return sorted_applications

from flask_login import current_user


def sort_applications(sort_by_attributes, app_list):
    remove_apps = []
    for i, attribute in enumerate(sort_by_attributes):
        for app in app_list:
            if not getattr(app, attribute):
                remove_apps.append(app)
        for bad_app in remove_apps:
            if bad_app in app_list:
                app_list.remove(bad_app)
    return app_list


def remove_archived():
    total_apps = current_user.job_applications
    active_apps = []
    for item in total_apps:
        if not item.archived:
            active_apps.append(item)
    return active_apps


def remove_active():
    total_apps = current_user.job_applications
    archived_applications = []
    for item in total_apps:
        if item.archived:
            archived_applications.append(item)
    return archived_applications





# Old code for reference

# def single_sorting_feature(field):                               lambda help from Eyal
#     user_apps = current_user.job_applications
#     sorted_applications = [app.__json__() for app in filter(lambda app: getattr(app, field), user_apps)]
#     return sorted_applications
#
#
# def double_sorting_feature(sort_list):
#     user_apps = current_user.job_applications
#     sorted_applications = [app.__json__() for app in filter(lambda app: getattr(app, sort_list[0]) and getattr(app, sort_list[1]), user_apps)]
#     return sorted_applications
#
#
# def triple_sorting_feature(sort_list):
#     user_apps = current_user.job_applications
#     sorted_applications = [app.__json__() for app in filter(lambda app: getattr(app, sort_list[0])
#                                           and getattr(app, sort_list[1]) and getattr(app, sort_list[2]), user_apps)]
#     return sorted_applications
#
#
# def quad_sorting_feature(sort_list):
#     user_apps = current_user.job_applications
#     sorted_applications = [app.__json__() for app in filter(lambda app: getattr(app, sort_list[0])
#                                           and getattr(app, sort_list[1]) and getattr(app, sort_list[2])
#                                           and getattr(app, sort_list[3]), user_apps)]
#     return sorted_applications







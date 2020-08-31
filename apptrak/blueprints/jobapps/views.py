import flask
from . import jobapps, forms
from .models import JobApplication
from ..auth.models import User
from ... import db
from ...sort_data import sorting_feature
from flask_login import current_user, login_required
import datetime
import json


@jobapps.route('/add-app', methods=['GET', 'POST'])
@login_required
def add_app():
    form = forms.UploadApp()
    if flask.request.method == 'POST':
        jobapp = JobApplication(
            date_added=datetime.datetime.now(),
            url=form.url.data,
            company=form.company.data,
            position=form.position.data,
            location=form.location.data,
            contact=form.contact.data,
            called_back=form.called_back.data,
            interview=form.interview.data,
            interview_date=form.interview_date.data,
            assignment=form.assignment.data,
            assignment_date=form.assignment_date.data,
            top_job=form.top_job.data,
            user_id=current_user.id
            )
        JobApplication.save(jobapp)
        return flask.redirect('index')
    return flask.render_template('uploadapp.html', form=form)


@jobapps.route('/current-apps', methods=['GET', 'POST'])
@login_required
def display_apps():
    applications = current_user.job_applications
    applications_as_json = []
    if flask.request.method == 'POST':
        field = flask.request.json
        filtered_apps = sorting_feature(field)
        print(f'data passed as applications: {filtered_apps}')
        return flask.render_template('displayapps.html', applications=filtered_apps)

    # def openfile(f):                 # TODO if done in backend delete
    #     return open(f, 'r').read()
    for item in applications:
        single_app = item.__json__()
        applications_as_json.append(single_app)
    return flask.render_template('displayapps.html', applications=applications_as_json)


@jobapps.route('/edit-app', methods=['GET', 'POST'])
@login_required
def edit_app():
    job_id = flask.request.json[0]               # gets id from Ajax call
    field = flask.request.json[1]                # gets data field to be updated (interview, assignment, call)
    date = flask.request.json[2]                 # gets user input date
    job_object = JobApplication.get_job(job_id)
    job_object.edit(field)                       # class method to update db
    job_object.add_date(field, date)             # class method to add date to db
    return 'okay'


@jobapps.route('/sort_apps', methods=['GET', 'POST'])
def sort_by():
    field = flask.request.json
    user_apps = current_user.job_applications
    sorted_applications = [app.__json__() for app in filter(lambda app: getattr(app, field), user_apps)]
    for app in sorted_applications:
        print(app['id'])
    return flask.jsonify({'applications': sorted_applications})


@jobapps.route('/archive')
def archive():
    job_id = flask.request.json(0)
    job_object = JobApplication.get_job(job_id)
    job_object.archived = True


# @jobapps.route('/jobapp/<job_id>', methods=["POST", "GET"]) Page not in use - delete when positive won't be relevant
# def app_details(job_id):
#     job = JobApplication.get_job(job_id)
#     return flask.render_template('jobdetails.html', job=job)

import flask
from . import jobapps, forms
from .models import JobApplication
from ..auth.models import User
from ... import db
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
    form = forms.UploadApp()
    applications = current_user.job_applications
    applications_as_json = []
    for item in applications:
        single_app = item.__json__()
        applications_as_json.append(single_app)
    print(applications_as_json)
    return flask.render_template('displayapps.html', applications=applications_as_json, form=form)


@jobapps.route('/edit-app', methods=['GET', 'POST'])
@login_required
def edit_app():
    job_id = flask.request.json[0]               # gets id from Ajax call
    field = flask.request.json[1]                # gets data field to be updated (interview, assignment, call)
    date = flask.request.json[2]                 # gets user input date
    job_object = JobApplication.get_job(job_id)
    job_object.edit(field)                       # class method to update db
    job_object.add_date(field, date)             # class method to add date to db


@jobapps.route('/sort_apps', methods=['GET', 'POST'])
def sort_by():
    field = flask.request.json
    user_apps = current_user.job_applications
    sorted_applications = []
    for item in user_apps:
        attribute = item.get_att_to_sort(field)
        print(attribute)
        if attribute:
            app_as_json = item.__json__()
            sorted_applications.append(app_as_json)
    print(sorted_applications)
    return flask.jsonify({'applications': sorted_applications})


@jobapps.route('/archive')
def archive():
    job_id = flask.request.json(0)
    job_object = JobApplication.get_job(job_id)
    job_object.archived = True


@jobapps.route('/filter/<field>')
def filter(field):
    pass


# @jobapps.route('/jobapp/<job_id>', methods=["POST", "GET"]) Page not in use - delete when positive won't be relevant
# def app_details(job_id):
#     job = JobApplication.get_job(job_id)
#     return flask.render_template('jobdetails.html', job=job)

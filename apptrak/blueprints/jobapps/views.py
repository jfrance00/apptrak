import flask
from sqlalchemy import select, and_
from . import jobapps, forms
from .models import JobApplication
from ..auth.models import User
from ... import db
from ...sort_data import single_sorting_feature, double_sorting_feature, triple_sorting_feature, quad_sorting_feature
from flask_login import current_user, login_required
import datetime


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
    if flask.request.method == 'POST':                                # TODO move this code to sort file
        sort_field_list = flask.request.form.getlist('filter_field')
        num_fields_to_check = len(sort_field_list)
        if num_fields_to_check == 1:                                   # loop checks for all possible combinations of
            applications = single_sorting_feature(sort_field_list[0])  # filter choices
        elif num_fields_to_check == 2:
            applications = double_sorting_feature(sort_field_list)
        elif num_fields_to_check == 3:
            applications = triple_sorting_feature(sort_field_list)
        elif num_fields_to_check == 4:
            applications = quad_sorting_feature(sort_field_list)
        return flask.render_template('displayapps.html', applications=applications)
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


@jobapps.route('/archive', methods=['GET', 'POST'])
@login_required
def archive():
    job_id = flask.request.json[0]
    print(job_id)
    job_object = JobApplication.get_job(job_id)
    print(job_object)
    job_object.edit('archived')
    return 'archived'


# @jobapps.route('/jobapp/<job_id>', methods=["POST", "GET"]) Page not in use - delete when positive won't be relevant
# def app_details(job_id):
#     job = JobApplication.get_job(job_id)
#     return flask.render_template('jobdetails.html', job=job)

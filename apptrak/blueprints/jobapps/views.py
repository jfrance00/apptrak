import flask
from flask import current_app
from sqlalchemy import select, and_
from . import jobapps, forms
from .models import JobApplication
from ..auth.models import User
from ... import db
from ...sort_data import single_sorting_feature, double_sorting_feature, triple_sorting_feature, quad_sorting_feature, remove_archived
from flask_login import current_user, login_required
import datetime


@jobapps.route('/add-app', methods=['GET', 'POST'])
def add_app():
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
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
        return flask.redirect('/current-apps')
    return flask.render_template('uploadapp.html', form=form)


@jobapps.route('/current-apps', methods=['GET', 'POST'])
@login_required
def display_apps():
    applications = current_user.job_applications
    active_applications = remove_archived(applications)
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
    return flask.render_template('displayapps.html', applications=active_applications)


@jobapps.route('/edit-app', methods=['GET', 'POST'])
def edit_app():
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
    job_id = flask.request.json[0]
    field = flask.request.json[1]
    date = flask.request.json[2]
    job_object = JobApplication.get_job(job_id)
    job_object.mark_true(field)                        # class method to update db
    job_object.add_date(field, date)              # class method to add date to db
    return 'data edited'


@jobapps.route('/archive', methods=['GET', 'POST'])
@login_required
def archive():
    job_id = flask.request.json[0]
    job_object = JobApplication.get_job(job_id)
    job_object.mark_true('archived')
    return 'archived'


@jobapps.route('/total-app-edit/<app_id>', methods=['GET', 'POST'])
@login_required
def total_app_edit(app_id):
    job_object = JobApplication.get_job(app_id)
    if flask.request.method == 'POST':
        job_object.url = flask.request.form.get('url')
        job_object.company = flask.request.form['company']
        job_object.position = flask.request.form['position']
        job_object.location = flask.request.form['location']
        job_object.contact = flask.request.form['contact']
        # job_object.interview = job_object.check_to_true(flask.request.form['interview'])
        job_object.interview_date = flask.request.form.get('interview_date')
        # job_object.assignment = job_object.check_to_true_false('assignment', flask.request.form.get('assignment'))
        job_object.assignment_date = flask.request.form.get('assignment_date')
        job_object.archived = job_object.check_to_true_false('archived', flask.request.form.get('archived'))
        job_object.save()
        return flask.redirect('/current-apps')
    return flask.render_template('edit-app-info.html', app=job_object)

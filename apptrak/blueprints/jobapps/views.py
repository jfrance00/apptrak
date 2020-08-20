import flask
from . import jobapps, forms
from .models import JobApplication
from ..auth.models import User
from ... import db
from flask_login import current_user
import datetime


@jobapps.route('/add-app', methods=['GET', 'POST'])
def add_app():
    form = forms.UploadApp()
    if flask.request.method == 'POST':
        jobapp = JobApplication(
            company=form.company.data,
            position=form.position.data,
            location=form.location.data,
            contact=form.contact.data,
            called_back=form.called_back.data,
            interview=form.interview.data,
            interview_date=form.interview_date.data,
            assignment=form.assignment.data,
            assignment_due=form.assignment_due.data,
            top_job=form.top_job.data,
            user_id=current_user.id
            )
        JobApplication.save(jobapp)
        return flask.redirect('index')
    return flask.render_template('uploadapp.html', form=form)


@jobapps.route('/current-apps')
def display_apps():
    applications = current_user.job_applications
    # apps_filterby_callback = db.session.filter_by()
    return flask.render_template('displayapps.html', applications=applications)


@jobapps.route('/jobapp/<job_id>', methods=["POST", "GET"])
def app_details(job_id):
    job = JobApplication.get_job(job_id)
    return flask.render_template('jobdetails.html', job=job)

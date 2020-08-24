import flask_wtf
import wtforms as wtf


class UploadApp(flask_wtf.FlaskForm):
    company = wtf.StringField('Company')
    position = wtf.StringField('Position')
    location = wtf.StringField('Location')
    url = wtf.StringField('Job Post URL')
    contact = wtf.StringField('Contact Email')
    called_back = wtf.BooleanField('Received a callback?')
    interview = wtf.BooleanField('Interview Scheduled?')
    interview_date = wtf.DateTimeField('Interview Data/Time')
    assignment = wtf.BooleanField('Assignment Received')
    assignment_date = wtf.DateTimeField('Assignment due date')
    top_job = wtf.BooleanField('Do you really really want this job?')
    submit = wtf.SubmitField('Submit')

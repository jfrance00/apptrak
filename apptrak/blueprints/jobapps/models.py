from ... import db
# from ...blueprints.auth.models import User


class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # date_added = db.Column(db.Date)  TODO add later
    company = db.Column(db.String(30))
    position = db.Column(db.String(50))
    location = db.Column(db.String(50))
    url = db.Column(db.String, unique=True)
    contact = db.Column(db.String)
    interview = db.Column(db.Boolean)
    called_back = db.Column(db.Boolean)
    interview_date = db.Column(db.DateTime)
    assignment = db.Column(db.Boolean)
    assignment_due = db.Column(db.DateTime)
    archived = db.Column(db.Boolean)
    top_job = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def edit(self, call_back, interview, interview_date, assignment, assignment_date):
        self.called_back = call_back
        self.interview = interview
        self.interview_date = interview_date
        self.assignment = assignment
        self.assignment_due = assignment_date

    @classmethod
    def get_job(cls, job_id):
        job = cls.query.filter_by(id=job_id).first()
        return job

    # JSON stringify function - turn to dict




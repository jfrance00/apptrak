from ... import db
# from ...blueprints.auth.models import User


class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.Date)
    company = db.Column(db.String(30))
    position = db.Column(db.String(50))
    location = db.Column(db.String(50))
    url = db.Column(db.String, unique=True)
    contact = db.Column(db.String)
    interview = db.Column(db.Boolean)
    called_back = db.Column(db.Boolean)
    interview_date = db.Column(db.String)
    assignment = db.Column(db.Boolean)
    assignment_date = db.Column(db.String)
    archived = db.Column(db.Boolean)
    top_job = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def edit(self, field):
        setattr(self, field, True)
        db.session.commit()

    def add_date(self, field, date):
        full_field = field + '_date'        # updates field to be the field to be 'interview_date' or 'assignment_date'
        print(f'full field: {full_field}')
        setattr(self, full_field, date)
        db.session.commit()
        print("date added")

    @classmethod
    def get_job(cls, job_id):
        job = cls.query.filter_by(id=job_id).first()
        return job

    # JSON stringify function - turn to dict




from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'student', 'hod', 'tpo'
    created_at = db.Column(db.DateTime, default=lambda: datetime.utcnow())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    name = db.Column(db.String(100), nullable=False)
    enrollment_no = db.Column(db.String(50), unique=True, nullable=False)
    department = db.Column(db.String(50), nullable=False)
    cgpa = db.Column(db.Float)
    phone = db.Column(db.String(15))
    resume_path = db.Column(db.String(255))
    skills = db.Column(db.JSON)  # Store as JSON array
    is_approved = db.Column(db.Boolean, default=False)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=lambda: datetime.utcnow())

    user = db.relationship('User', foreign_keys=[user_id], backref='student_profile')
    approver = db.relationship('User', foreign_keys=[approved_by])

class HOD(db.Model):
    __tablename__ = 'hods'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15))

    user = db.relationship('User', backref='hod_profile')

class TPO(db.Model):
    __tablename__ = 'tpos'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15))

    user = db.relationship('User', backref='tpo_profile')

class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    website = db.Column(db.String(255))
    industry = db.Column(db.String(100))
    description = db.Column(db.Text)
    research_data = db.Column(db.JSON)  # Cached AI research
    last_researched = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=lambda: datetime.utcnow())

class PlacementDrive(db.Model):
    __tablename__ = 'placement_drives'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    job_title = db.Column(db.String(200), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    job_requirements = db.Column(db.JSON)  # Skills, experience, etc.
    eligibility_criteria = db.Column(db.JSON)  # CGPA, departments, etc.
    ctc = db.Column(db.String(50))
    location = db.Column(db.String(100))
    drive_date = db.Column(db.DateTime)
    registration_deadline = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active')  # active, completed, cancelled
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=lambda: datetime.utcnow())

    company = db.relationship('Company', backref='drives')

class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drives.id'))
    resume_version = db.Column(db.String(255))  # Path to personalized resume
    cover_letter = db.Column(db.Text)
    match_score = db.Column(db.Float)  # AI-calculated fit score
    ats_score = db.Column(db.Float)  # ATS compatibility score
    skills_gap = db.Column(db.JSON)  # Missing skills
    status = db.Column(db.String(20), default='applied')  # applied, shortlisted, rejected, selected
    applied_at = db.Column(db.DateTime, default=lambda: datetime.utcnow())

    student = db.relationship('Student', backref='applications')
    drive = db.relationship('PlacementDrive', backref='applications')

class SelectionRound(db.Model):
    __tablename__ = 'selection_rounds'

    id = db.Column(db.Integer, primary_key=True)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drives.id'))
    round_name = db.Column(db.String(100))  # Online Test, Technical, HR, etc.
    round_number = db.Column(db.Integer)
    round_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=lambda: datetime.utcnow())

    drive = db.relationship('PlacementDrive', backref='rounds')

class RoundResult(db.Model):
    __tablename__ = 'round_results'

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'))
    round_id = db.Column(db.Integer, db.ForeignKey('selection_rounds.id'))
    status = db.Column(db.String(20))  # selected, rejected, pending
    feedback = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.utcnow())

    application = db.relationship('Application', backref='round_results')
    round = db.relationship('SelectionRound', backref='results')

class OfferLetter(db.Model):
    __tablename__ = 'offer_letters'

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'))
    file_path = db.Column(db.String(255))
    issued_date = db.Column(db.DateTime, default=lambda: datetime.utcnow())

    application = db.relationship('Application', backref='offer_letter')

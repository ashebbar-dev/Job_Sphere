from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Student, User, PlacementDrive, Application, OfferLetter
from utils.decorators import role_required
from werkzeug.utils import secure_filename
import os

student_bp = Blueprint('student', __name__)

@student_bp.route('/profile', methods=['GET'])
@jwt_required()
@role_required(['student'])
def get_profile():
    user_id = get_jwt_identity()
    student = Student.query.filter_by(user_id=user_id).first_or_404()

    return jsonify({
        'id': student.id,
        'name': student.name,
        'enrollment_no': student.enrollment_no,
        'department': student.department,
        'email': student.user.email,
        'cgpa': student.cgpa,
        'phone': student.phone,
        'resume_path': student.resume_path,
        'skills': student.skills,
        'is_approved': student.is_approved
    }), 200

@student_bp.route('/profile', methods=['PUT'])
@jwt_required()
@role_required(['student'])
def update_profile():
    user_id = get_jwt_identity()
    student = Student.query.filter_by(user_id=user_id).first_or_404()
    data = request.get_json()

    if 'name' in data:
        student.name = data['name']
    if 'cgpa' in data:
        student.cgpa = data['cgpa']
    if 'phone' in data:
        student.phone = data['phone']
    if 'skills' in data:
        student.skills = data['skills']

    db.session.commit()

    return jsonify({'message': 'Profile updated'}), 200

@student_bp.route('/resume', methods=['POST'])
@jwt_required()
@role_required(['student'])
def upload_resume():
    user_id = get_jwt_identity()
    student = Student.query.filter_by(user_id=user_id).first_or_404()

    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Save file
    filename = secure_filename(f"{student.enrollment_no}_{file.filename}")
    filepath = os.path.join('uploads/resumes', filename)
    os.makedirs('uploads/resumes', exist_ok=True)
    file.save(filepath)

    student.resume_path = filepath
    db.session.commit()

    return jsonify({
        'message': 'Resume uploaded',
        'resume_path': filepath
    }), 200

@student_bp.route('/drives/available', methods=['GET'])
@jwt_required()
@role_required(['student'])
def get_available_drives():
    user_id = get_jwt_identity()
    student = Student.query.filter_by(user_id=user_id).first_or_404()

    # Get drives student is eligible for and hasn't applied to
    drives = PlacementDrive.query.filter_by(status='active').all()

    available_drives = []
    for drive in drives:
        # Check if already applied
        existing_app = Application.query.filter_by(
            student_id=student.id,
            drive_id=drive.id
        ).first()

        if not existing_app:
            # Check eligibility
            criteria = drive.eligibility_criteria or {}
            eligible = True

            if 'min_cgpa' in criteria and student.cgpa < criteria['min_cgpa']:
                eligible = False

            if 'departments' in criteria and student.department not in criteria['departments']:
                eligible = False

            if eligible:
                available_drives.append({
                    'id': drive.id,
                    'company_name': drive.company.name,
                    'job_title': drive.job_title,
                    'ctc': drive.ctc,
                    'location': drive.location,
                    'drive_date': drive.drive_date.isoformat() if drive.drive_date else None,
                    'registration_deadline': drive.registration_deadline.isoformat() if drive.registration_deadline else None
                })

    return jsonify(available_drives), 200

@student_bp.route('/applications', methods=['GET'])
@jwt_required()
@role_required(['student'])
def get_my_applications():
    user_id = get_jwt_identity()
    student = Student.query.filter_by(user_id=user_id).first_or_404()

    applications = Application.query.filter_by(student_id=student.id).all()

    return jsonify([{
        'id': app.id,
        'company_name': app.drive.company.name,
        'job_title': app.drive.job_title,
        'status': app.status,
        'match_score': app.match_score,
        'ats_score': app.ats_score,
        'applied_at': app.applied_at.isoformat()
    } for app in applications]), 200

@student_bp.route('/applications/<int:app_id>/offer-letter', methods=['GET'])
@jwt_required()
@role_required(['student'])
def download_offer_letter(app_id):
    user_id = get_jwt_identity()
    student = Student.query.filter_by(user_id=user_id).first_or_404()

    application = Application.query.filter_by(id=app_id, student_id=student.id).first_or_404()
    offer = OfferLetter.query.filter_by(application_id=app_id).first_or_404()

    return send_file(offer.file_path, as_attachment=True)

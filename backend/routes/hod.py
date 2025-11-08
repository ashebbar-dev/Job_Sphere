from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Student, HOD, Application
from utils.decorators import role_required
from services.email_service import send_email_notification

hod_bp = Blueprint('hod', __name__)

@hod_bp.route('/students/pending', methods=['GET'])
@jwt_required()
@role_required(['hod'])
def get_pending_students():
    user_id = int(get_jwt_identity())
    hod = HOD.query.filter_by(user_id=user_id).first()

    students = Student.query.filter_by(
        department=hod.department,
        is_approved=False
    ).all()

    return jsonify([{
        'id': s.id,
        'name': s.name,
        'enrollment_no': s.enrollment_no,
        'email': s.user.email,
        'cgpa': s.cgpa,
        'phone': s.phone,
        'resume_path': s.resume_path,
        'skills': s.skills
    } for s in students]), 200

@hod_bp.route('/students/<int:student_id>/approve', methods=['POST'])
@jwt_required()
@role_required(['hod'])
def approve_student(student_id):
    user_id = int(get_jwt_identity())
    student = Student.query.get_or_404(student_id)

    student.is_approved = True
    student.approved_by = user_id

    db.session.commit()

    # Send approval email
    send_email_notification(
        to=student.user.email,
        subject="Profile Approved",
        body=f"Your profile has been approved by the HOD. You can now apply for placements."
    )

    return jsonify({'message': 'Student approved'}), 200

@hod_bp.route('/students/<int:student_id>', methods=['PUT'])
@jwt_required()
@role_required(['hod'])
def update_student(student_id):
    data = request.get_json()
    student = Student.query.get_or_404(student_id)

    # Update fields
    if 'name' in data:
        student.name = data['name']
    if 'cgpa' in data:
        student.cgpa = data['cgpa']
    if 'phone' in data:
        student.phone = data['phone']
    if 'skills' in data:
        student.skills = data['skills']

    db.session.commit()

    return jsonify({'message': 'Student updated'}), 200

@hod_bp.route('/stats', methods=['GET'])
@jwt_required()
@role_required(['hod'])
def get_department_stats():
    user_id = int(get_jwt_identity())
    hod = HOD.query.filter_by(user_id=user_id).first()

    total_students = Student.query.filter_by(department=hod.department).count()
    approved_students = Student.query.filter_by(department=hod.department, is_approved=True).count()

    # Get placement stats
    placed_students = db.session.query(Student).join(Application).filter(
        Student.department == hod.department,
        Application.status == 'selected'
    ).distinct().count()

    return jsonify({
        'department': hod.department,
        'total_students': total_students,
        'approved_students': approved_students,
        'placed_students': placed_students,
        'placement_percentage': round((placed_students / total_students * 100) if total_students > 0 else 0, 2)
    }), 200

@hod_bp.route('/reports/placements', methods=['GET'])
@jwt_required()
@role_required(['hod'])
def get_placement_report():
    user_id = int(get_jwt_identity())
    hod = HOD.query.filter_by(user_id=user_id).first()

    # Get all placed students in department
    placed_apps = db.session.query(Application).join(Student).filter(
        Student.department == hod.department,
        Application.status == 'selected'
    ).all()

    report = []
    for app in placed_apps:
        report.append({
            'student_name': app.student.name,
            'enrollment_no': app.student.enrollment_no,
            'company': app.drive.company.name,
            'job_title': app.drive.job_title,
            'ctc': app.drive.ctc,
            'selected_date': app.applied_at.isoformat()
        })

    return jsonify(report), 200

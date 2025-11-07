from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, PlacementDrive, Company, Application, SelectionRound, RoundResult, OfferLetter
from utils.decorators import role_required
from services.email_service import send_email_notification
from datetime import datetime
import os

tpo_bp = Blueprint('tpo', __name__)

@tpo_bp.route('/companies', methods=['POST'])
@jwt_required()
@role_required(['tpo'])
def create_company():
    data = request.get_json()

    company = Company(
        name=data['name'],
        website=data.get('website'),
        industry=data.get('industry'),
        description=data.get('description')
    )

    db.session.add(company)
    db.session.commit()

    return jsonify({
        'message': 'Company created',
        'company_id': company.id
    }), 201

@tpo_bp.route('/companies', methods=['GET'])
@jwt_required()
def get_companies():
    companies = Company.query.all()

    return jsonify([{
        'id': c.id,
        'name': c.name,
        'website': c.website,
        'industry': c.industry
    } for c in companies]), 200

@tpo_bp.route('/drives', methods=['POST'])
@jwt_required()
@role_required(['tpo'])
def create_drive():
    data = request.get_json()

    drive = PlacementDrive(
        company_id=data['company_id'],
        job_title=data['job_title'],
        job_description=data['job_description'],
        job_requirements=data.get('job_requirements', {}),
        eligibility_criteria=data.get('eligibility_criteria', {}),
        ctc=data.get('ctc'),
        location=data.get('location'),
        drive_date=datetime.fromisoformat(data['drive_date']) if data.get('drive_date') else None,
        registration_deadline=datetime.fromisoformat(data['registration_deadline']) if data.get('registration_deadline') else None,
        created_by=get_jwt_identity()
    )

    db.session.add(drive)
    db.session.commit()

    return jsonify({
        'message': 'Drive created',
        'drive_id': drive.id
    }), 201

@tpo_bp.route('/drives', methods=['GET'])
@jwt_required()
def get_drives():
    drives = PlacementDrive.query.all()

    return jsonify([{
        'id': d.id,
        'company_name': d.company.name,
        'job_title': d.job_title,
        'ctc': d.ctc,
        'location': d.location,
        'drive_date': d.drive_date.isoformat() if d.drive_date else None,
        'status': d.status,
        'applications_count': len(d.applications)
    } for d in drives]), 200

@tpo_bp.route('/drives/<int:drive_id>', methods=['GET'])
@jwt_required()
def get_drive_details(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)

    return jsonify({
        'id': drive.id,
        'company': {
            'id': drive.company.id,
            'name': drive.company.name,
            'website': drive.company.website
        },
        'job_title': drive.job_title,
        'job_description': drive.job_description,
        'job_requirements': drive.job_requirements,
        'eligibility_criteria': drive.eligibility_criteria,
        'ctc': drive.ctc,
        'location': drive.location,
        'drive_date': drive.drive_date.isoformat() if drive.drive_date else None,
        'registration_deadline': drive.registration_deadline.isoformat() if drive.registration_deadline else None,
        'status': drive.status
    }), 200

@tpo_bp.route('/drives/<int:drive_id>/applications', methods=['GET'])
@jwt_required()
@role_required(['tpo'])
def get_drive_applications(drive_id):
    applications = Application.query.filter_by(drive_id=drive_id).all()

    return jsonify([{
        'id': app.id,
        'student_name': app.student.name,
        'enrollment_no': app.student.enrollment_no,
        'department': app.student.department,
        'cgpa': app.student.cgpa,
        'match_score': app.match_score,
        'ats_score': app.ats_score,
        'status': app.status,
        'applied_at': app.applied_at.isoformat()
    } for app in applications]), 200

@tpo_bp.route('/rounds', methods=['POST'])
@jwt_required()
@role_required(['tpo'])
def create_round():
    data = request.get_json()

    round = SelectionRound(
        drive_id=data['drive_id'],
        round_name=data['round_name'],
        round_number=data['round_number'],
        round_date=datetime.fromisoformat(data['round_date']) if data.get('round_date') else None
    )

    db.session.add(round)
    db.session.commit()

    return jsonify({
        'message': 'Round created',
        'round_id': round.id
    }), 201

@tpo_bp.route('/rounds/<int:round_id>/results', methods=['POST'])
@jwt_required()
@role_required(['tpo'])
def update_round_results(round_id):
    data = request.get_json()
    results = data['results']  # [{application_id, status, feedback}, ...]

    for result_data in results:
        result = RoundResult.query.filter_by(
            application_id=result_data['application_id'],
            round_id=round_id
        ).first()

        if result:
            result.status = result_data['status']
            result.feedback = result_data.get('feedback')
        else:
            result = RoundResult(
                application_id=result_data['application_id'],
                round_id=round_id,
                status=result_data['status'],
                feedback=result_data.get('feedback')
            )
            db.session.add(result)

        # Update application status if rejected
        if result_data['status'] == 'rejected':
            application = Application.query.get(result_data['application_id'])
            application.status = 'rejected'

        # Send email notification
        application = Application.query.get(result_data['application_id'])
        send_email_notification(
            to=application.student.user.email,
            subject=f"Round Update - {result_data['status'].title()}",
            body=f"Your status for round {round_id}: {result_data['status']}"
        )

    db.session.commit()

    return jsonify({'message': 'Results updated'}), 200

@tpo_bp.route('/applications/<int:app_id>/select', methods=['POST'])
@jwt_required()
@role_required(['tpo'])
def select_candidate(app_id):
    application = Application.query.get_or_404(app_id)
    application.status = 'selected'

    db.session.commit()

    # Send selection email
    send_email_notification(
        to=application.student.user.email,
        subject="Congratulations! You've been selected",
        body=f"You have been selected for {application.drive.job_title} at {application.drive.company.name}"
    )

    return jsonify({'message': 'Candidate selected'}), 200

@tpo_bp.route('/applications/<int:app_id>/offer-letter', methods=['POST'])
@jwt_required()
@role_required(['tpo'])
def upload_offer_letter(app_id):
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Save file
    filename = f"offer_{app_id}_{file.filename}"
    filepath = os.path.join('uploads/offers', filename)
    os.makedirs('uploads/offers', exist_ok=True)
    file.save(filepath)

    # Create offer letter record
    offer = OfferLetter(
        application_id=app_id,
        file_path=filepath
    )
    db.session.add(offer)
    db.session.commit()

    # Send email
    application = Application.query.get(app_id)
    send_email_notification(
        to=application.student.user.email,
        subject="Your Offer Letter is Ready",
        body="Your offer letter has been uploaded. Please login to download."
    )

    return jsonify({'message': 'Offer letter uploaded'}), 201

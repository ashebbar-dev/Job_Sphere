import json
import os

import openai
from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Application, Company, PlacementDrive, Student, db
from utils.decorators import role_required
from services.company_research import analyze_job_requirements, research_company
from services.resume_service import (
    extract_resume_text,
    parse_resume_with_ai,
    calculate_match_score,
    calculate_ats_score,
    identify_skills_gap,
    prepare_personalized_resume,
    get_personalized_resume_path,
)

ai_bp = Blueprint('ai', __name__)


def _safe_download_token(value):
    token = (value or "").strip()
    if not token:
        return "resume"
    cleaned = "".join(ch if ch.isalnum() else "-" for ch in token)
    cleaned = "-".join(filter(None, cleaned.split("-"))).lower()
    return cleaned or "resume"

@ai_bp.route('/analyze-job/<int:drive_id>', methods=['GET'])
@jwt_required()
@role_required(['student'])
def analyze_job_fit(drive_id):
    """Comprehensive AI analysis of job fit"""
    user_id = int(get_jwt_identity())
    student = Student.query.filter_by(user_id=user_id).first_or_404()
    drive = PlacementDrive.query.get_or_404(drive_id)

    # Check if student has resume
    if not student.resume_path:
        return jsonify({'error': 'Please upload resume first'}), 400

    # Extract resume text
    resume_text = extract_resume_text(student.resume_path)
    if not resume_text:
        return jsonify({'error': 'Could not read resume'}), 500

    # Parse resume with AI
    parsed_resume = parse_resume_with_ai(resume_text)
    if not parsed_resume:
        return jsonify({'error': 'Could not parse resume'}), 500

    # Research company & role using deep research
    company_data = research_company(
        drive.company.name,
        drive.company.website,
        job_title=drive.job_title,
        job_description=drive.job_description,
        student_profile={
            "summary": parsed_resume.get("summary"),
            "skills": parsed_resume.get("skills"),
            "experience": parsed_resume.get("experience"),
            "projects": parsed_resume.get("projects"),
        },
    )

    # Analyze job requirements
    job_analysis = analyze_job_requirements(
        drive.job_description,
        drive.job_requirements or {}
    )

    # Calculate match score
    match_analysis = calculate_match_score(parsed_resume, job_analysis, company_data)

    # Calculate ATS score
    all_keywords = (job_analysis.get('required_skills', []) +
                   job_analysis.get('preferred_skills', []) +
                   job_analysis.get('must_have_keywords', []))
    ats_analysis = calculate_ats_score(resume_text, all_keywords)

    # Skills gap analysis
    skills_gap = identify_skills_gap(
        parsed_resume.get('skills', []),
        job_analysis.get('required_skills', []),
        job_analysis.get('preferred_skills', [])
    )

    # Generate personalized resume package (content + PDF)
    personalized_content, personalized_pdf_path = prepare_personalized_resume(
        student,
        drive,
        parsed_resume,
        job_analysis,
        company_data,
        match_analysis,
        skills_gap,
    )

    return jsonify({
        'company_research': company_data,
        'job_analysis': job_analysis,
        'match_analysis': match_analysis,
        'ats_analysis': ats_analysis,
        'skills_gap': skills_gap,
        'personalized_content': personalized_content,
        'personalized_resume_pdf': personalized_pdf_path.replace('\\', '/') if personalized_pdf_path else None,
        'parsed_resume': parsed_resume
    }), 200

@ai_bp.route('/apply/<int:drive_id>', methods=['POST'])
@jwt_required()
@role_required(['student'])
def apply_to_drive(drive_id):
    """Apply to drive with AI-enhanced application"""
    user_id = int(get_jwt_identity())
    student = Student.query.filter_by(user_id=user_id).first_or_404()
    drive = PlacementDrive.query.get_or_404(drive_id)

    # Check if already applied
    existing = Application.query.filter_by(
        student_id=student.id,
        drive_id=drive_id
    ).first()

    if existing:
        return jsonify({'error': 'Already applied to this drive'}), 400

    # Check if approved
    if not student.is_approved:
        return jsonify({'error': 'Profile not approved by HOD'}), 403

    data = request.get_json()
    personalized_resume_path = get_personalized_resume_path(student, drive)
    resume_version_path = (
        personalized_resume_path if os.path.exists(personalized_resume_path) else student.resume_path
    )

    # Create application
    application = Application(
        student_id=student.id,
        drive_id=drive_id,
        resume_version=resume_version_path if resume_version_path else None,
        match_score=data.get('match_score'),
        ats_score=data.get('ats_score'),
        skills_gap=data.get('skills_gap'),
        status='applied'
    )

    db.session.add(application)
    db.session.commit()

    # Send confirmation email (AI-generated)
    from services.email_service import generate_ai_email, send_email_notification

    email_body = generate_ai_email(
        context=f"Student {student.name} applied to {drive.job_title} at {drive.company.name}",
        purpose="Application confirmation email"
    )

    if email_body:
        send_email_notification(
            to=student.user.email,
            subject=f"Application Submitted - {drive.job_title}",
            body=email_body
        )

    return jsonify({
        'message': 'Application submitted successfully',
        'application_id': application.id,
        'used_personalized_resume': resume_version_path == personalized_resume_path and resume_version_path is not None
    }), 201

@ai_bp.route('/research-company/<int:company_id>', methods=['GET'])
@jwt_required()
def get_company_research(company_id):
    """Get cached or fresh company research"""
    company = Company.query.get_or_404(company_id)

    research_data = research_company(company.name, company.website)

    return jsonify(research_data), 200

@ai_bp.route('/generate-cover-letter/<int:drive_id>', methods=['GET'])
@jwt_required()
@role_required(['student'])
def generate_cover_letter(drive_id):
    """Generate personalized cover letter"""
    user_id = int(get_jwt_identity())
    student = Student.query.filter_by(user_id=user_id).first_or_404()
    drive = PlacementDrive.query.get_or_404(drive_id)

    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    # Get student resume
    resume_text = extract_resume_text(student.resume_path)
    parsed_resume = parse_resume_with_ai(resume_text)

    # Get company research
    company_data = research_company(drive.company.name, drive.company.website)

    prompt = f"""Write a personalized cover letter for this job application:

Student Profile:
Name: {student.name}
Department: {student.department}
Skills: {json.dumps(parsed_resume.get('skills', []))}
Experience: {json.dumps(parsed_resume.get('experience', []))}

Job Details:
Company: {drive.company.name}
Role: {drive.job_title}
Description: {drive.job_description}

Company Research:
{json.dumps(company_data, indent=2)}

Write a compelling, personalized cover letter that:
1. Shows genuine interest in the company
2. Highlights relevant skills and experience
3. Demonstrates cultural fit
4. Is concise (250-300 words)
5. Has a professional tone"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional cover letter writer helping college students apply for jobs."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )

        cover_letter = response.choices[0].message.content

        return jsonify({
            'cover_letter': cover_letter
        }), 200

    except Exception as e:
        return jsonify({'error': 'Could not generate cover letter'}), 500

@ai_bp.route('/personalized-resume/<int:drive_id>', methods=['GET'])
@jwt_required()
@role_required(['student'])
def download_personalized_resume(drive_id):
    """Allow student to download the AI-personalized resume PDF."""
    user_id = int(get_jwt_identity())
    student = Student.query.filter_by(user_id=user_id).first_or_404()
    drive = PlacementDrive.query.get_or_404(drive_id)

    file_path = get_personalized_resume_path(student, drive)

    if not os.path.exists(file_path):
        return jsonify({'error': 'Personalized resume not generated yet'}), 404

    download_name = f"{_safe_download_token(student.name)}-{_safe_download_token(drive.job_title)}.pdf"
    return send_file(file_path, as_attachment=True, download_name=download_name)

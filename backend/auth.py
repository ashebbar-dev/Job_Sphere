from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, Student, HOD, TPO

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Check if user exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400

    # Create user
    user = User(
        email=data['email'],
        role=data['role']
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.flush()  # Get user.id

    # Create role-specific profile
    if data['role'] == 'student':
        student = Student(
            user_id=user.id,
            name=data['name'],
            enrollment_no=data['enrollment_no'],
            department=data['department'],
            phone=data.get('phone'),
            cgpa=data.get('cgpa')
        )
        db.session.add(student)

    elif data['role'] == 'hod':
        hod = HOD(
            user_id=user.id,
            name=data['name'],
            department=data['department'],
            phone=data.get('phone')
        )
        db.session.add(hod)

    elif data['role'] == 'tpo':
        tpo = TPO(
            user_id=user.id,
            name=data['name'],
            phone=data.get('phone')
        )
        db.session.add(tpo)

    db.session.commit()

    return jsonify({'message': 'Registration successful'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=str(user.id))

    # Get profile data
    profile = None
    if user.role == 'student':
        profile = Student.query.filter_by(user_id=user.id).first()
    elif user.role == 'hod':
        profile = HOD.query.filter_by(user_id=user.id).first()
    elif user.role == 'tpo':
        profile = TPO.query.filter_by(user_id=user.id).first()

    return jsonify({
        'access_token': access_token,
        'role': user.role,
        'profile': {
            'id': profile.id if profile else None,
            'name': profile.name if profile else None,
            'department': getattr(profile, 'department', None)
        }
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    return jsonify({
        'id': user.id,
        'email': user.email,
        'role': user.role
    }), 200

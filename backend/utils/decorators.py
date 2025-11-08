from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from models import User

def role_required(allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                user_id = int(get_jwt_identity())
                user = User.query.get(user_id)

                if not user or user.role not in allowed_roles:
                    return jsonify({'error': 'Access denied'}), 403

                return fn(*args, **kwargs)
            except Exception as e:
                print(f"Error in role_required decorator: {str(e)}")
                print(f"User ID from JWT: {get_jwt_identity() if get_jwt_identity() else 'None'}")
                return jsonify({'error': f'Authorization error: {str(e)}'}), 500
        return wrapper
    return decorator

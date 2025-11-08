from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from config import Config
from models import db
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    CORS(app)
    JWTManager(app)
    Mail(app)

    # Create upload folders
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('uploads/resumes', exist_ok=True)
    os.makedirs('uploads/offers', exist_ok=True)
    os.makedirs('data', exist_ok=True)

    # Register blueprints
    from auth import auth_bp
    from routes.tpo import tpo_bp
    from routes.hod import hod_bp
    from routes.student import student_bp
    from routes.ai_services import ai_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(tpo_bp, url_prefix='/api/tpo')
    app.register_blueprint(hod_bp, url_prefix='/api/hod')
    app.register_blueprint(student_bp, url_prefix='/api/student')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')

    # Health check
    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200

    # Request lifecycle hooks
    @app.before_request
    def log_request_info():
        print(f"\n=== INCOMING REQUEST ===")
        print(f"Method: {request.method}")
        print(f"Path: {request.path}")
        print(f"Headers: {dict(request.headers)}")

    @app.after_request
    def log_response_info(response):
        print(f"\n=== OUTGOING RESPONSE ===")
        print(f"Status: {response.status}")
        print(f"Path: {request.path}")
        if response.status_code == 422:
            print(f"422 RESPONSE DATA: {response.get_data(as_text=True)}")
        return response

    # Global error handlers
    @app.errorhandler(422)
    def handle_unprocessable_entity(e):
        print(f"422 ERROR CAUGHT: {str(e)}")
        print(f"Error description: {e.description if hasattr(e, 'description') else 'No description'}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': 'Unprocessable Entity', 'details': str(e)}), 422

    @app.errorhandler(Exception)
    def handle_exception(e):
        print(f"GENERAL EXCEPTION CAUGHT: {type(e).__name__}: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    # Create database tables
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)

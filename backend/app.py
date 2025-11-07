from flask import Flask
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
    os.makedirs('data', exist_ok=True)

    # Register blueprints
    from auth import auth_bp
    from routes.tpo import tpo_bp
    from routes.hod import hod_bp
    from routes.student import student_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(tpo_bp, url_prefix='/api/tpo')
    app.register_blueprint(hod_bp, url_prefix='/api/hod')
    app.register_blueprint(student_bp, url_prefix='/api/student')

    # Create database tables
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)

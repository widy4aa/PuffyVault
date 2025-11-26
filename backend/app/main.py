"""
Main application entry point for Secure Notes API
"""
from flask import Flask, jsonify
from flask_cors import CORS
from app.config import Config
from app.database import db
from app.middleware.error_handler import register_error_handlers

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
CORS(app, 
     origins=['http://localhost:8000', 'http://localhost:3000'],
     supports_credentials=True,
     allow_headers=['Content-Type', 'Authorization'])

# Register error handlers
register_error_handlers(app)

# Import and register blueprints
from app.routes import auth, users, notes

app.register_blueprint(auth.bp, url_prefix='/api/auth')
app.register_blueprint(users.bp, url_prefix='/api/user')
app.register_blueprint(notes.bp, url_prefix='/api/notes')

@app.route('/')
def index():
    """API root endpoint"""
    return jsonify({
        'success': True,
        'message': 'Secure Notes API',
        'version': '1.0.0'
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy'
    })

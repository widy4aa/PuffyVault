"""
Routes untuk autentikasi (register & login)
"""
from flask import Blueprint, request, jsonify
import jwt
import base64
from datetime import datetime, timedelta
from app.models.user import User
from app.database import db
from app.utils.security import hash_password, verify_password, generate_salt
from app.config import Config

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    """Daftar user baru"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        name = data.get('name', '').strip()
        
        # Validasi input
        if not email or not password:
            return jsonify({'error': 'Email dan password harus diisi'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Password minimal 6 karakter'}), 400
        
        # Cek apakah email sudah terdaftar
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email sudah terdaftar'}), 400
        
        # Buat user baru
        salt = generate_salt()
        password_hash = hash_password(password)
        
        user = User(
            email=email,
            password_hash=password_hash,
            name=name or email.split('@')[0],
            salt=salt
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'Registrasi berhasil',
            'user_id': user.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        # Validasi input
        if not email or not password:
            return jsonify({'error': 'Email dan password harus diisi'}), 400
        
        # Cari user
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error': 'Email atau password salah'}), 401
        
        # Verifikasi password
        if not verify_password(password, user.password_hash):
            return jsonify({'error': 'Email atau password salah'}), 401
        
        # Buat JWT token
        token = jwt.encode({
            'user_id': user.id,
            'email': user.email,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, Config.JWT_SECRET_KEY, algorithm='HS256')
        
        # Convert bytes to string jika perlu
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        
        # Convert salt dari bytes ke base64 string
        salt_b64 = base64.b64encode(user.salt).decode('utf-8') if user.salt else ''
        
        return jsonify({
            'token': token,
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'salt': salt_b64
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

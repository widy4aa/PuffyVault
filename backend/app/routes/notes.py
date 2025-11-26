"""
Routes untuk catatan (CRUD notes)
"""
from flask import Blueprint, request, jsonify
import jwt
import base64
from functools import wraps
from app.models.user import User
from app.models.note import Note
from app.database import db
from app.config import Config

bp = Blueprint('notes', __name__)

# Helper function untuk autentikasi
def login_required(f):
    """Decorator untuk route yang butuh login"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not token:
            return jsonify({'error': 'Token tidak ditemukan'}), 401
        
        try:
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
            user = User.query.get(payload['user_id'])
            if not user:
                return jsonify({'error': 'User tidak valid'}), 401
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token sudah expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token tidak valid'}), 401
    
    return decorated

@bp.route('', methods=['POST'])
@login_required
def create_note(user):
    """Buat catatan baru"""
    try:
        data = request.get_json()
        
        # Validasi input
        if not data.get('encrypted_content'):
            return jsonify({'error': 'Konten tidak boleh kosong'}), 400
        
        # Decode base64 ke bytes untuk disimpan
        encrypted_content = base64.b64decode(data['encrypted_content']) if isinstance(data['encrypted_content'], str) else data['encrypted_content']
        iv = base64.b64decode(data.get('iv', '')) if data.get('iv') and isinstance(data.get('iv'), str) else data.get('iv', b'')
        auth_tag = base64.b64decode(data.get('auth_tag', '')) if data.get('auth_tag') and isinstance(data.get('auth_tag'), str) else data.get('auth_tag', b'')
        
        # Simpan catatan
        note = Note(
            user_id=user.id,
            encrypted_content=encrypted_content,
            iv=iv,
            auth_tag=auth_tag
        )
        
        db.session.add(note)
        db.session.commit()
        
        return jsonify({
            'message': 'Catatan berhasil dibuat',
            'note_id': note.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('', methods=['GET'])
@login_required
def get_notes(user):
    """Ambil semua catatan user"""
    try:
        notes = Note.query.filter_by(user_id=user.id).order_by(Note.created_at.desc()).all()
        
        return jsonify({
            'notes': [{
                'id': note.id,
                'encrypted_content': base64.b64encode(note.encrypted_content).decode('utf-8') if note.encrypted_content else '',
                'iv': base64.b64encode(note.iv).decode('utf-8') if note.iv else '',
                'auth_tag': base64.b64encode(note.auth_tag).decode('utf-8') if note.auth_tag else '',
                'created_at': note.created_at.isoformat(),
                'updated_at': note.updated_at.isoformat()
            } for note in notes]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:note_id>', methods=['GET'])
@login_required
def get_note(user, note_id):
    """Ambil satu catatan"""
    try:
        note = Note.query.filter_by(id=note_id, user_id=user.id).first()
        
        if not note:
            return jsonify({'error': 'Catatan tidak ditemukan'}), 404
        
        return jsonify({
            'id': note.id,
            'encrypted_content': base64.b64encode(note.encrypted_content).decode('utf-8') if note.encrypted_content else '',
            'iv': base64.b64encode(note.iv).decode('utf-8') if note.iv else '',
            'auth_tag': base64.b64encode(note.auth_tag).decode('utf-8') if note.auth_tag else '',
            'created_at': note.created_at.isoformat(),
            'updated_at': note.updated_at.isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:note_id>', methods=['PUT'])
@login_required
def update_note(user, note_id):
    """Update catatan"""
    try:
        data = request.get_json()
        
        # Cari catatan
        note = Note.query.filter_by(id=note_id, user_id=user.id).first()
        if not note:
            return jsonify({'error': 'Catatan tidak ditemukan'}), 404
        
        # Update data - decode base64 ke bytes
        if 'encrypted_content' in data:
            note.encrypted_content = base64.b64decode(data['encrypted_content']) if isinstance(data['encrypted_content'], str) else data['encrypted_content']
        if 'iv' in data:
            note.iv = base64.b64decode(data['iv']) if isinstance(data['iv'], str) else data['iv']
        if 'auth_tag' in data:
            note.auth_tag = base64.b64decode(data['auth_tag']) if isinstance(data['auth_tag'], str) else data['auth_tag']
        
        db.session.commit()
        
        return jsonify({'message': 'Catatan berhasil diupdate'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:note_id>', methods=['DELETE'])
@login_required
def delete_note(user, note_id):
    """Hapus catatan"""
    try:
        note = Note.query.filter_by(id=note_id, user_id=user.id).first()
        
        if not note:
            return jsonify({'error': 'Catatan tidak ditemukan'}), 404
        
        db.session.delete(note)
        db.session.commit()
        
        return jsonify({'message': 'Catatan berhasil dihapus'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

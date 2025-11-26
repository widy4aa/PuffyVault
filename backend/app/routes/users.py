"""
User routes
"""
from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.schemas.user import ChangePassword
from app.services.user_service import UserService
from app.middleware.auth_middleware import require_auth
from app.utils.validators import validate_request

bp = Blueprint('users', __name__)
user_service = UserService()

@bp.route('/profile', methods=['GET'])
@require_auth
def get_profile(current_user):
    """
    GET /api/user/profile
    Get current user profile (including salt for key derivation)
    """
    try:
        profile = user_service.get_user_profile(current_user.id)
        
        return jsonify({
            'success': True,
            'user': profile
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal Server Error',
            'message': str(e),
            'status_code': 500
        }), 500

@bp.route('/profile', methods=['PUT'])
@require_auth
def update_profile(current_user):
    """
    PUT /api/user/profile
    Update user profile (name)
    """
    try:
        data = request.get_json()
        name = data.get('name')
        
        if not name:
            raise ValueError('Name is required')
        
        user_service.update_user_profile(current_user.id, name=name)
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully'
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'Validation Error',
            'message': str(e),
            'status_code': 400
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal Server Error',
            'message': str(e),
            'status_code': 500
        }), 500

@bp.route('/change-password', methods=['POST'])
@require_auth
def change_password(current_user):
    """
    POST /api/user/change-password
    Change user password
    """
    try:
        # Validate request data
        data = validate_request(ChangePassword, request.get_json())
        
        # Change password
        user_service.change_password(
            user_id=current_user.id,
            old_password=data.old_password,
            new_password=data.new_password
        )
        
        return jsonify({
            'success': True,
            'message': 'Password changed successfully'
        }), 200
        
    except ValidationError as e:
        return jsonify({
            'success': False,
            'error': 'Validation Error',
            'message': str(e),
            'status_code': 422
        }), 422
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'Password Change Error',
            'message': str(e),
            'status_code': 400
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal Server Error',
            'message': str(e),
            'status_code': 500
        }), 500

"""
Authentication middleware
"""
from functools import wraps
from flask import request, jsonify
from app.services.auth_service import AuthService
from app.models.user import User

def require_auth(f):
    """
    Decorator to require JWT authentication
    Extracts user from token and passes to route handler
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({
                'success': False,
                'error': 'Unauthorized',
                'message': 'No authorization header provided',
                'status_code': 401
            }), 401
        
        if not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'error': 'Unauthorized',
                'message': 'Invalid authorization header format',
                'status_code': 401
            }), 401
        
        token = auth_header.split(' ')[1]
        
        try:
            # Verify token
            auth_service = AuthService()
            payload = auth_service.verify_token(token)
            
            # Get user from database
            user = User.query.get(payload['user_id'])
            if not user:
                return jsonify({
                    'success': False,
                    'error': 'Unauthorized',
                    'message': 'User not found',
                    'status_code': 401
                }), 401
            
            # Pass user to route handler
            return f(current_user=user, *args, **kwargs)
            
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': 'Unauthorized',
                'message': str(e),
                'status_code': 401
            }), 401
        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Internal Server Error',
                'message': str(e),
                'status_code': 500
            }), 500
    
    return decorated_function

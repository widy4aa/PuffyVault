"""
Global error handler
"""
from flask import jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    """Register global error handlers"""
    
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({
            'success': False,
            'error': 'Bad Request',
            'message': str(e),
            'status_code': 400
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({
            'success': False,
            'error': 'Unauthorized',
            'message': str(e),
            'status_code': 401
        }), 401
    
    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({
            'success': False,
            'error': 'Forbidden',
            'message': str(e),
            'status_code': 403
        }), 403
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            'success': False,
            'error': 'Not Found',
            'message': str(e),
            'status_code': 404
        }), 404
    
    @app.errorhandler(422)
    def unprocessable_entity(e):
        return jsonify({
            'success': False,
            'error': 'Unprocessable Entity',
            'message': str(e),
            'status_code': 422
        }), 422
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({
            'success': False,
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred',
            'status_code': 500
        }), 500
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify({
            'success': False,
            'error': e.name,
            'message': e.description,
            'status_code': e.code
        }), e.code
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        # Log the error here
        app.logger.error(f'Unhandled exception: {str(e)}')
        
        return jsonify({
            'success': False,
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred',
            'status_code': 500
        }), 500

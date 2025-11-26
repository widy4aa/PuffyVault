"""
Test configuration
"""
import pytest
from app.main import app, db
from app.config import TestingConfig

@pytest.fixture
def client():
    """Create test client"""
    app.config.from_object(TestingConfig)
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture
def auth_headers(client):
    """Create authenticated user and return auth headers"""
    # Register user
    client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'TestPassword123!',
        'confirm_password': 'TestPassword123!',
        'name': 'Test User'
    })
    
    # Login
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'TestPassword123!'
    })
    
    token = response.json['token']
    
    return {
        'Authorization': f'Bearer {token}'
    }

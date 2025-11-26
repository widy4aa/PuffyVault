"""
Authentication tests
"""
import pytest

class TestRegistration:
    """Test user registration"""
    
    def test_register_success(self, client):
        """Test successful registration"""
        response = client.post('/api/auth/register', json={
            'email': 'newuser@example.com',
            'password': 'SecurePass123!',
            'confirm_password': 'SecurePass123!',
            'name': 'New User'
        })
        
        assert response.status_code == 201
        assert response.json['success'] is True
        assert 'user_id' in response.json
    
    def test_register_duplicate_email(self, client):
        """Test registration with duplicate email"""
        # First registration
        client.post('/api/auth/register', json={
            'email': 'duplicate@example.com',
            'password': 'SecurePass123!',
            'confirm_password': 'SecurePass123!',
            'name': 'User One'
        })
        
        # Duplicate registration
        response = client.post('/api/auth/register', json={
            'email': 'duplicate@example.com',
            'password': 'SecurePass123!',
            'confirm_password': 'SecurePass123!',
            'name': 'User Two'
        })
        
        assert response.status_code == 400
        assert response.json['success'] is False
    
    def test_register_weak_password(self, client):
        """Test registration with weak password"""
        response = client.post('/api/auth/register', json={
            'email': 'weak@example.com',
            'password': 'weak',
            'confirm_password': 'weak',
            'name': 'Weak User'
        })
        
        assert response.status_code == 422
        assert response.json['success'] is False
    
    def test_register_password_mismatch(self, client):
        """Test registration with mismatched passwords"""
        response = client.post('/api/auth/register', json={
            'email': 'mismatch@example.com',
            'password': 'SecurePass123!',
            'confirm_password': 'DifferentPass123!',
            'name': 'Mismatch User'
        })
        
        assert response.status_code == 422
        assert response.json['success'] is False

class TestLogin:
    """Test user login"""
    
    def test_login_success(self, client):
        """Test successful login"""
        # Register user
        client.post('/api/auth/register', json={
            'email': 'login@example.com',
            'password': 'LoginPass123!',
            'confirm_password': 'LoginPass123!',
            'name': 'Login User'
        })
        
        # Login
        response = client.post('/api/auth/login', json={
            'email': 'login@example.com',
            'password': 'LoginPass123!'
        })
        
        assert response.status_code == 200
        assert response.json['success'] is True
        assert 'token' in response.json
        assert 'expires_in' in response.json
    
    def test_login_wrong_password(self, client):
        """Test login with wrong password"""
        # Register user
        client.post('/api/auth/register', json={
            'email': 'wrong@example.com',
            'password': 'CorrectPass123!',
            'confirm_password': 'CorrectPass123!',
            'name': 'Wrong User'
        })
        
        # Login with wrong password
        response = client.post('/api/auth/login', json={
            'email': 'wrong@example.com',
            'password': 'WrongPass123!'
        })
        
        assert response.status_code == 401
        assert response.json['success'] is False
    
    def test_login_nonexistent_user(self, client):
        """Test login with nonexistent user"""
        response = client.post('/api/auth/login', json={
            'email': 'nonexistent@example.com',
            'password': 'SomePass123!'
        })
        
        assert response.status_code == 401
        assert response.json['success'] is False

class TestLogout:
    """Test user logout"""
    
    def test_logout_success(self, client, auth_headers):
        """Test successful logout"""
        response = client.post('/api/auth/logout', headers=auth_headers)
        
        assert response.status_code == 200
        assert response.json['success'] is True
    
    def test_logout_without_token(self, client):
        """Test logout without token"""
        response = client.post('/api/auth/logout')
        
        assert response.status_code == 400
        assert response.json['success'] is False

class TestTokenVerification:
    """Test token verification"""
    
    def test_verify_valid_token(self, client, auth_headers):
        """Test verification of valid token"""
        response = client.post('/api/auth/verify-token', headers=auth_headers)
        
        assert response.status_code == 200
        assert response.json['valid'] is True
    
    def test_verify_invalid_token(self, client):
        """Test verification of invalid token"""
        response = client.post('/api/auth/verify-token', headers={
            'Authorization': 'Bearer invalid_token'
        })
        
        assert response.status_code == 401
        assert response.json['valid'] is False

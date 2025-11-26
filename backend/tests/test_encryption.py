"""
Encryption tests
"""
import pytest
from app.utils.security import hash_password, verify_password, generate_salt, derive_key_pbkdf2

class TestPasswordHashing:
    """Test password hashing functions"""
    
    def test_hash_password(self):
        """Test password hashing"""
        password = "TestPassword123!"
        hashed = hash_password(password)
        
        assert hashed is not None
        assert isinstance(hashed, str)
        assert hashed != password
    
    def test_verify_password_correct(self):
        """Test password verification with correct password"""
        password = "TestPassword123!"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password"""
        password = "TestPassword123!"
        hashed = hash_password(password)
        
        assert verify_password("WrongPassword123!", hashed) is False

class TestSaltGeneration:
    """Test salt generation"""
    
    def test_generate_salt_default_size(self):
        """Test salt generation with default size"""
        salt = generate_salt()
        
        assert salt is not None
        assert isinstance(salt, bytes)
        assert len(salt) == 16  # Default SALT_SIZE from config
    
    def test_generate_salt_custom_size(self):
        """Test salt generation with custom size"""
        salt = generate_salt(size=32)
        
        assert salt is not None
        assert isinstance(salt, bytes)
        assert len(salt) == 32
    
    def test_generate_salt_uniqueness(self):
        """Test that generated salts are unique"""
        salt1 = generate_salt()
        salt2 = generate_salt()
        
        assert salt1 != salt2

class TestPBKDF2:
    """Test PBKDF2 key derivation"""
    
    def test_derive_key_pbkdf2(self):
        """Test PBKDF2 key derivation"""
        password = "TestPassword123!"
        salt = generate_salt()
        
        key = derive_key_pbkdf2(password, salt)
        
        assert key is not None
        assert isinstance(key, bytes)
        assert len(key) == 32  # AES_KEY_SIZE from config
    
    def test_derive_key_pbkdf2_consistency(self):
        """Test that same password and salt produce same key"""
        password = "TestPassword123!"
        salt = generate_salt()
        
        key1 = derive_key_pbkdf2(password, salt)
        key2 = derive_key_pbkdf2(password, salt)
        
        assert key1 == key2
    
    def test_derive_key_pbkdf2_different_passwords(self):
        """Test that different passwords produce different keys"""
        salt = generate_salt()
        
        key1 = derive_key_pbkdf2("Password1", salt)
        key2 = derive_key_pbkdf2("Password2", salt)
        
        assert key1 != key2
    
    def test_derive_key_pbkdf2_different_salts(self):
        """Test that different salts produce different keys"""
        password = "TestPassword123!"
        
        key1 = derive_key_pbkdf2(password, generate_salt())
        key2 = derive_key_pbkdf2(password, generate_salt())
        
        assert key1 != key2

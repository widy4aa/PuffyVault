"""
Security utilities for password hashing and encryption
"""
import os
import bcrypt
from app.config import Config

def generate_salt(size: int = None) -> bytes:
    """
    Generate a random salt for PBKDF2 key derivation
    
    Args:
        size: Salt size in bytes (default from config)
        
    Returns:
        bytes: Random salt
    """
    if size is None:
        size = Config.SALT_SIZE
    
    return os.urandom(size)

def hash_password(password: str) -> str:
    """
    Hash password using bcrypt
    
    Args:
        password: Plain text password
        
    Returns:
        str: Hashed password
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=Config.BCRYPT_LOG_ROUNDS)
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    return hashed.decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    """
    Verify password against hash
    
    Args:
        password: Plain text password
        password_hash: Hashed password
        
    Returns:
        bool: True if password matches hash
    """
    password_bytes = password.encode('utf-8')
    hash_bytes = password_hash.encode('utf-8')
    
    return bcrypt.checkpw(password_bytes, hash_bytes)

def derive_key_pbkdf2(password: str, salt: bytes, iterations: int = None) -> bytes:
    """
    Derive encryption key from password using PBKDF2-HMAC-SHA256
    This is used on client-side for note encryption
    Server doesn't use this function (client-side encryption only)
    
    Args:
        password: User password
        salt: Random salt
        iterations: Number of iterations (default from config)
        
    Returns:
        bytes: Derived key
    """
    import hashlib
    
    if iterations is None:
        iterations = Config.PBKDF2_ITERATIONS
    
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        iterations,
        dklen=Config.AES_KEY_SIZE
    )
    
    return key

"""
Authentication service
"""
import os
import jwt
from datetime import datetime, timedelta
from app.models.user import User, JWTBlacklist
from app.database import db
from app.utils.security import hash_password, verify_password, generate_salt
from app.config import Config

class AuthService:
    """Handle user authentication operations"""
    
    def register_user(self, email: str, password: str, name: str = None) -> dict:
        """
        Register a new user
        
        Args:
            email: User email
            password: User password (plain text)
            name: User name (optional)
            
        Returns:
            dict: User registration result
            
        Raises:
            ValueError: If user already exists or validation fails
        """
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            raise ValueError('User with this email already exists')
        
        # Generate salt and hash password
        salt = generate_salt()
        password_hash = hash_password(password)
        
        # Create new user
        user = User(
            email=email,
            password_hash=password_hash,
            name=name,
            salt=salt
        )
        
        db.session.add(user)
        db.session.commit()
        
        return {
            'user_id': user.id,
            'email': user.email,
            'name': user.name
        }
    
    def login_user(self, email: str, password: str) -> dict:
        """
        Authenticate user and generate JWT token
        
        Args:
            email: User email
            password: User password (plain text)
            
        Returns:
            dict: Login result with JWT token
            
        Raises:
            ValueError: If authentication fails
        """
        # Find user by email
        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValueError('Invalid email or password')
        
        # Verify password
        if not verify_password(password, user.password_hash):
            raise ValueError('Invalid email or password')
        
        # Generate JWT token
        token = self._generate_token(user.id)
        
        return {
            'token': token,
            'expires_in': int(Config.JWT_ACCESS_TOKEN_EXPIRES.total_seconds()),
            'user': user.to_dict()
        }
    
    def logout_user(self, token: str) -> bool:
        """
        Logout user by blacklisting JWT token
        
        Args:
            token: JWT token to blacklist
            
        Returns:
            bool: Success status
        """
        try:
            # Decode token to get expiry
            payload = jwt.decode(
                token,
                Config.JWT_SECRET_KEY,
                algorithms=[Config.JWT_ALGORITHM]
            )
            
            expires_at = datetime.fromtimestamp(payload['exp'])
            
            # Add token to blacklist
            blacklist_entry = JWTBlacklist(
                token=token,
                expires_at=expires_at
            )
            
            db.session.add(blacklist_entry)
            db.session.commit()
            
            return True
            
        except jwt.InvalidTokenError:
            raise ValueError('Invalid token')
    
    def verify_token(self, token: str) -> dict:
        """
        Verify JWT token validity
        
        Args:
            token: JWT token to verify
            
        Returns:
            dict: Token payload
            
        Raises:
            ValueError: If token is invalid or blacklisted
        """
        try:
            # Check if token is blacklisted
            blacklisted = JWTBlacklist.query.filter_by(token=token).first()
            if blacklisted:
                raise ValueError('Token has been revoked')
            
            # Decode and verify token
            payload = jwt.decode(
                token,
                Config.JWT_SECRET_KEY,
                algorithms=[Config.JWT_ALGORITHM]
            )
            
            return payload
            
        except jwt.ExpiredSignatureError:
            raise ValueError('Token has expired')
        except jwt.InvalidTokenError:
            raise ValueError('Invalid token')
    
    def _generate_token(self, user_id: int) -> str:
        """
        Generate JWT token for user
        
        Args:
            user_id: User ID
            
        Returns:
            str: JWT token
        """
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + Config.JWT_ACCESS_TOKEN_EXPIRES,
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(
            payload,
            Config.JWT_SECRET_KEY,
            algorithm=Config.JWT_ALGORITHM
        )
        
        return token

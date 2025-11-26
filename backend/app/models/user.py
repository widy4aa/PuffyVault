"""
User model
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, LargeBinary
from app.database import db

class User(db.Model):
    """User model for authentication and profile"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=True)
    salt = Column(LargeBinary, nullable=False)  # For PBKDF2 key derivation
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    notes = db.relationship('Note', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def to_dict(self, include_salt=False):
        """Convert user to dictionary"""
        user_dict = {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_salt:
            import base64
            user_dict['salt'] = base64.b64encode(self.salt).decode('utf-8')
        
        return user_dict

class JWTBlacklist(db.Model):
    """JWT token blacklist for logout"""
    __tablename__ = 'jwt_blacklist'
    
    id = Column(Integer, primary_key=True)
    token = Column(String(500), nullable=False, index=True)
    blacklisted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    
    def __repr__(self):
        return f'<JWTBlacklist {self.id}>'

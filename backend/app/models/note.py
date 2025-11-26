"""
Note model
"""
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, LargeBinary, DateTime, Boolean
from app.database import db

class Note(db.Model):
    """Note model for encrypted notes storage"""
    __tablename__ = 'notes'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    encrypted_content = Column(LargeBinary, nullable=False)  # Encrypted title + content
    iv = Column(LargeBinary, nullable=False)  # Initialization Vector
    auth_tag = Column(LargeBinary, nullable=False)  # Authentication tag for GCM
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f'<Note {self.id} - User {self.user_id}>'
    
    def to_dict(self):
        """Convert note to dictionary"""
        import base64
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'encrypted_content': base64.b64encode(self.encrypted_content).decode('utf-8'),
            'iv': base64.b64encode(self.iv).decode('utf-8'),
            'auth_tag': base64.b64encode(self.auth_tag).decode('utf-8'),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_deleted': self.is_deleted,
            'deleted_at': self.deleted_at.isoformat() if self.deleted_at else None
        }

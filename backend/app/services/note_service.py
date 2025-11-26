"""
Note service
"""
import base64
from datetime import datetime
from app.models.note import Note
from app.database import db

class NoteService:
    """Handle note CRUD operations"""
    
    def create_note(self, user_id: int, encrypted_content: str, iv: str, auth_tag: str) -> dict:
        """
        Create a new encrypted note
        
        Args:
            user_id: User ID
            encrypted_content: Base64 encoded encrypted content
            iv: Base64 encoded initialization vector
            auth_tag: Base64 encoded authentication tag
            
        Returns:
            dict: Created note data
        """
        # Decode base64 strings to bytes
        encrypted_content_bytes = base64.b64decode(encrypted_content)
        iv_bytes = base64.b64decode(iv)
        auth_tag_bytes = base64.b64decode(auth_tag)
        
        # Create new note
        note = Note(
            user_id=user_id,
            encrypted_content=encrypted_content_bytes,
            iv=iv_bytes,
            auth_tag=auth_tag_bytes
        )
        
        db.session.add(note)
        db.session.commit()
        
        return note.to_dict()
    
    def get_user_notes(self, user_id: int) -> list:
        """
        Get all notes for a user (excluding deleted)
        
        Args:
            user_id: User ID
            
        Returns:
            list: List of notes
        """
        notes = Note.query.filter_by(
            user_id=user_id,
            is_deleted=False
        ).order_by(Note.created_at.desc()).all()
        
        return [note.to_dict() for note in notes]
    
    def get_note(self, note_id: int, user_id: int) -> dict:
        """
        Get a single note by ID
        
        Args:
            note_id: Note ID
            user_id: User ID (for authorization)
            
        Returns:
            dict: Note data or None if not found
        """
        note = Note.query.filter_by(
            id=note_id,
            user_id=user_id,
            is_deleted=False
        ).first()
        
        return note.to_dict() if note else None
    
    def update_note(self, note_id: int, user_id: int, encrypted_content: str, iv: str, auth_tag: str) -> dict:
        """
        Update an existing note
        
        Args:
            note_id: Note ID
            user_id: User ID (for authorization)
            encrypted_content: Base64 encoded encrypted content
            iv: Base64 encoded initialization vector
            auth_tag: Base64 encoded authentication tag
            
        Returns:
            dict: Updated note data or None if not found
        """
        note = Note.query.filter_by(
            id=note_id,
            user_id=user_id,
            is_deleted=False
        ).first()
        
        if not note:
            return None
        
        # Decode base64 strings to bytes
        encrypted_content_bytes = base64.b64decode(encrypted_content)
        iv_bytes = base64.b64decode(iv)
        auth_tag_bytes = base64.b64decode(auth_tag)
        
        # Update note
        note.encrypted_content = encrypted_content_bytes
        note.iv = iv_bytes
        note.auth_tag = auth_tag_bytes
        note.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return note.to_dict()
    
    def delete_note(self, note_id: int, user_id: int) -> bool:
        """
        Delete a note (soft delete)
        
        Args:
            note_id: Note ID
            user_id: User ID (for authorization)
            
        Returns:
            bool: Success status
        """
        note = Note.query.filter_by(
            id=note_id,
            user_id=user_id,
            is_deleted=False
        ).first()
        
        if not note:
            return False
        
        # Soft delete
        note.is_deleted = True
        note.deleted_at = datetime.utcnow()
        
        db.session.commit()
        
        return True

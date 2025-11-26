"""
Pydantic schemas for request/response validation
"""
from app.schemas.user import UserRegister, UserLogin, UserProfile, ChangePassword
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse

__all__ = [
    'UserRegister', 'UserLogin', 'UserProfile', 'ChangePassword',
    'NoteCreate', 'NoteUpdate', 'NoteResponse'
]

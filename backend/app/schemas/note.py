"""
Note schemas for validation
"""
from pydantic import BaseModel, Field

class NoteCreate(BaseModel):
    """Schema for creating a new note"""
    encrypted_content: str = Field(..., description="Base64 encoded encrypted content")
    iv: str = Field(..., description="Base64 encoded initialization vector")
    auth_tag: str = Field(..., description="Base64 encoded authentication tag")

class NoteUpdate(BaseModel):
    """Schema for updating a note"""
    encrypted_content: str = Field(..., description="Base64 encoded encrypted content")
    iv: str = Field(..., description="Base64 encoded initialization vector")
    auth_tag: str = Field(..., description="Base64 encoded authentication tag")

class NoteResponse(BaseModel):
    """Schema for note response"""
    id: int
    user_id: int
    encrypted_content: str
    iv: str
    auth_tag: str
    created_at: str
    updated_at: str
    is_deleted: bool
    deleted_at: str | None

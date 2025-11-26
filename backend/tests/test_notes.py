"""
Note tests
"""
import pytest
import base64

class TestCreateNote:
    """Test note creation"""
    
    def test_create_note_success(self, client, auth_headers):
        """Test successful note creation"""
        response = client.post('/api/notes', 
            headers=auth_headers,
            json={
                'encrypted_content': base64.b64encode(b'encrypted data').decode(),
                'iv': base64.b64encode(b'initialization vector').decode(),
                'auth_tag': base64.b64encode(b'authentication tag').decode()
            }
        )
        
        assert response.status_code == 201
        assert response.json['success'] is True
        assert 'note_id' in response.json
    
    def test_create_note_unauthorized(self, client):
        """Test note creation without auth"""
        response = client.post('/api/notes', json={
            'encrypted_content': base64.b64encode(b'encrypted data').decode(),
            'iv': base64.b64encode(b'initialization vector').decode(),
            'auth_tag': base64.b64encode(b'authentication tag').decode()
        })
        
        assert response.status_code == 401
        assert response.json['success'] is False
    
    def test_create_note_missing_fields(self, client, auth_headers):
        """Test note creation with missing fields"""
        response = client.post('/api/notes',
            headers=auth_headers,
            json={
                'encrypted_content': base64.b64encode(b'encrypted data').decode()
                # Missing iv and auth_tag
            }
        )
        
        assert response.status_code == 422

class TestGetNotes:
    """Test getting notes"""
    
    def test_get_all_notes(self, client, auth_headers):
        """Test getting all user notes"""
        # Create a note first
        client.post('/api/notes',
            headers=auth_headers,
            json={
                'encrypted_content': base64.b64encode(b'encrypted data').decode(),
                'iv': base64.b64encode(b'initialization vector').decode(),
                'auth_tag': base64.b64encode(b'authentication tag').decode()
            }
        )
        
        # Get all notes
        response = client.get('/api/notes', headers=auth_headers)
        
        assert response.status_code == 200
        assert response.json['success'] is True
        assert isinstance(response.json['notes'], list)
        assert len(response.json['notes']) > 0
    
    def test_get_single_note(self, client, auth_headers):
        """Test getting single note"""
        # Create a note
        create_response = client.post('/api/notes',
            headers=auth_headers,
            json={
                'encrypted_content': base64.b64encode(b'encrypted data').decode(),
                'iv': base64.b64encode(b'initialization vector').decode(),
                'auth_tag': base64.b64encode(b'authentication tag').decode()
            }
        )
        
        note_id = create_response.json['note_id']
        
        # Get the note
        response = client.get(f'/api/notes/{note_id}', headers=auth_headers)
        
        assert response.status_code == 200
        assert response.json['success'] is True
        assert response.json['note']['id'] == note_id
    
    def test_get_nonexistent_note(self, client, auth_headers):
        """Test getting nonexistent note"""
        response = client.get('/api/notes/99999', headers=auth_headers)
        
        assert response.status_code == 404
        assert response.json['success'] is False

class TestUpdateNote:
    """Test note updates"""
    
    def test_update_note_success(self, client, auth_headers):
        """Test successful note update"""
        # Create a note
        create_response = client.post('/api/notes',
            headers=auth_headers,
            json={
                'encrypted_content': base64.b64encode(b'original data').decode(),
                'iv': base64.b64encode(b'original iv').decode(),
                'auth_tag': base64.b64encode(b'original tag').decode()
            }
        )
        
        note_id = create_response.json['note_id']
        
        # Update the note
        response = client.put(f'/api/notes/{note_id}',
            headers=auth_headers,
            json={
                'encrypted_content': base64.b64encode(b'updated data').decode(),
                'iv': base64.b64encode(b'updated iv').decode(),
                'auth_tag': base64.b64encode(b'updated tag').decode()
            }
        )
        
        assert response.status_code == 200
        assert response.json['success'] is True
    
    def test_update_nonexistent_note(self, client, auth_headers):
        """Test updating nonexistent note"""
        response = client.put('/api/notes/99999',
            headers=auth_headers,
            json={
                'encrypted_content': base64.b64encode(b'updated data').decode(),
                'iv': base64.b64encode(b'updated iv').decode(),
                'auth_tag': base64.b64encode(b'updated tag').decode()
            }
        )
        
        assert response.status_code == 404
        assert response.json['success'] is False

class TestDeleteNote:
    """Test note deletion"""
    
    def test_delete_note_success(self, client, auth_headers):
        """Test successful note deletion"""
        # Create a note
        create_response = client.post('/api/notes',
            headers=auth_headers,
            json={
                'encrypted_content': base64.b64encode(b'to be deleted').decode(),
                'iv': base64.b64encode(b'initialization vector').decode(),
                'auth_tag': base64.b64encode(b'authentication tag').decode()
            }
        )
        
        note_id = create_response.json['note_id']
        
        # Delete the note
        response = client.delete(f'/api/notes/{note_id}', headers=auth_headers)
        
        assert response.status_code == 200
        assert response.json['success'] is True
        
        # Verify note is deleted
        get_response = client.get(f'/api/notes/{note_id}', headers=auth_headers)
        assert get_response.status_code == 404
    
    def test_delete_nonexistent_note(self, client, auth_headers):
        """Test deleting nonexistent note"""
        response = client.delete('/api/notes/99999', headers=auth_headers)
        
        assert response.status_code == 404
        assert response.json['success'] is False

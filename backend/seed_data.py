"""
Seed dummy data for testing
Creates sample users and encrypted notes
"""
import os
import sys
import base64

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.database import db
from app.models.user import User
from app.models.note import Note
from app.utils.security import hash_password, generate_salt

def create_dummy_data():
    """Create dummy users and notes for testing"""
    with app.app_context():
        print("Creating dummy data...")
        
        # Clear existing data (optional)
        Note.query.delete()
        User.query.delete()
        db.session.commit()
        print("✓ Cleared existing data")
        
        # Create dummy users
        users_data = [
            {
                'email': 'alice@example.com',
                'password': 'AlicePass123!',
                'name': 'Alice Johnson'
            },
            {
                'email': 'bob@example.com',
                'password': 'BobSecure456!',
                'name': 'Bob Smith'
            },
            {
                'email': 'charlie@example.com',
                'password': 'Charlie789!@#',
                'name': 'Charlie Brown'
            }
        ]
        
        created_users = []
        for user_data in users_data:
            salt = generate_salt()
            user = User(
                email=user_data['email'],
                password_hash=hash_password(user_data['password']),
                name=user_data['name'],
                salt=salt
            )
            db.session.add(user)
            created_users.append(user)
            print(f"✓ Created user: {user_data['email']} (password: {user_data['password']})")
        
        db.session.commit()
        
        # Create dummy encrypted notes for each user
        # Note: In real app, these would be encrypted on client-side
        # For testing, we're simulating encrypted content
        
        notes_data = [
            # Alice's notes
            {
                'user_email': 'alice@example.com',
                'encrypted_content': base64.b64encode(b'Encrypted: My first secure note about project ideas').decode(),
                'iv': base64.b64encode(os.urandom(16)).decode(),
                'auth_tag': base64.b64encode(os.urandom(16)).decode()
            },
            {
                'user_email': 'alice@example.com',
                'encrypted_content': base64.b64encode(b'Encrypted: Shopping list - milk, eggs, bread').decode(),
                'iv': base64.b64encode(os.urandom(16)).decode(),
                'auth_tag': base64.b64encode(os.urandom(16)).decode()
            },
            {
                'user_email': 'alice@example.com',
                'encrypted_content': base64.b64encode(b'Encrypted: Meeting notes from quarterly review').decode(),
                'iv': base64.b64encode(os.urandom(16)).decode(),
                'auth_tag': base64.b64encode(os.urandom(16)).decode()
            },
            # Bob's notes
            {
                'user_email': 'bob@example.com',
                'encrypted_content': base64.b64encode(b'Encrypted: Password manager backup codes').decode(),
                'iv': base64.b64encode(os.urandom(16)).decode(),
                'auth_tag': base64.b64encode(os.urandom(16)).decode()
            },
            {
                'user_email': 'bob@example.com',
                'encrypted_content': base64.b64encode(b'Encrypted: Travel itinerary for summer vacation').decode(),
                'iv': base64.b64encode(os.urandom(16)).decode(),
                'auth_tag': base64.b64encode(os.urandom(16)).decode()
            },
            # Charlie's notes
            {
                'user_email': 'charlie@example.com',
                'encrypted_content': base64.b64encode(b'Encrypted: Book recommendations from friends').decode(),
                'iv': base64.b64encode(os.urandom(16)).decode(),
                'auth_tag': base64.b64encode(os.urandom(16)).decode()
            }
        ]
        
        for note_data in notes_data:
            user = User.query.filter_by(email=note_data['user_email']).first()
            if user:
                note = Note(
                    user_id=user.id,
                    encrypted_content=base64.b64decode(note_data['encrypted_content']),
                    iv=base64.b64decode(note_data['iv']),
                    auth_tag=base64.b64decode(note_data['auth_tag'])
                )
                db.session.add(note)
        
        db.session.commit()
        print(f"✓ Created {len(notes_data)} dummy notes")
        
        print("\n" + "="*60)
        print("DUMMY DATA CREATED SUCCESSFULLY!")
        print("="*60)
        print("\nTest Users (for Postman):")
        print("-" * 60)
        for user_data in users_data:
            user = User.query.filter_by(email=user_data['email']).first()
            note_count = Note.query.filter_by(user_id=user.id).count()
            print(f"\nEmail: {user_data['email']}")
            print(f"Password: {user_data['password']}")
            print(f"Name: {user_data['name']}")
            print(f"Notes: {note_count}")
        print("\n" + "="*60)

if __name__ == '__main__':
    create_dummy_data()

"""
Database initialization script
Run this to create all tables
"""
import os
import sys

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

from app.main import app
from app.database import db

def init_db():
    """Initialize database tables"""
    with app.app_context():
        # Import models to register them
        from app.models import User, Note
        from app.models.user import JWTBlacklist
        
        # Create all tables
        db.create_all()
        
        print("Database tables created successfully!")

if __name__ == '__main__':
    init_db()

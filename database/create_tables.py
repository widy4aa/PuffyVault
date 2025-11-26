"""
Create database tables
Run this script to initialize the database
"""
import os
import sys

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

from app.main import app
from app.database import db
from app.models.user import User, JWTBlacklist
from app.models.note import Note

def create_tables():
    """Create all database tables"""
    with app.app_context():
        print("Creating database tables...")
        
        # Drop all tables (optional - comment out in production)
        # db.drop_all()
        # print("Dropped existing tables")
        
        # Create all tables
        db.create_all()
        print("✓ All tables created successfully!")
        
        # Show created tables
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"\nCreated tables: {', '.join(tables)}")

if __name__ == '__main__':
    create_tables()

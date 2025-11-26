"""
Flask Application Entry Point
Run this file to start the server: python run.py
"""

import sys
import os

# Add backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app
from app.config import Config

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Starting Secure Notes API Server")
    print("=" * 60)
    print(f"📍 Debug Mode: {Config.DEBUG}")
    print(f"🔗 API URL: http://{Config.HOST}:{Config.PORT}/api")
    db_uri = Config.SQLALCHEMY_DATABASE_URI
    print(f"🗄️  Database: {db_uri.split('@')[1] if '@' in db_uri else 'PostgreSQL'}")
    print("=" * 60)
    print("\n⚡ Server running... Press CTRL+C to stop\n")
    
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )

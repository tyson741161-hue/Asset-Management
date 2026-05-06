"""
Database initialization script for IT Asset Management System
Creates all necessary tables in PostgreSQL database
"""
import os
from models import db, Asset, Ticket, TicketReply, TicketNote, Request
from flask import Flask

def init_database():
    """Initialize the database with all tables"""
    
    # Create Flask app
    app = Flask(__name__)
    
    # Get database URL from environment or use default
    database_url = os.environ.get('DATABASE_URL', 'postgresql://asset_admin:asset_secure_pass_2026@localhost:5432/asset_management')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    with app.app_context():
        print("Creating database tables...")
        
        # Drop all tables (use with caution!)
        # db.drop_all()
        
        # Create all tables
        db.create_all()
        
        print("Database tables created successfully!")
        print("\nTables created:")
        print("- assets")
        print("- tickets")
        print("- ticket_replies")
        print("- ticket_notes")
        print("- requests")
        
        return True

if __name__ == '__main__':
    try:
        init_database()
        print("\n✓ Database initialization completed successfully!")
    except Exception as e:
        print(f"\n✗ Error initializing database: {str(e)}")
        import traceback
        traceback.print_exc()

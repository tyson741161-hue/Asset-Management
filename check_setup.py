"""
Setup verification script for IT Asset Management System
Checks if all components are properly configured
"""
import os
import sys

def check_python_version():
    """Check Python version"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 11:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (Need 3.11+)")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print("\nChecking Python dependencies...")
    required = [
        'flask',
        'flask_mail',
        'flask_sqlalchemy',
        'sqlalchemy',
        'psycopg2',
        'imap_tools'
    ]
    
    all_installed = True
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} (Not installed)")
            all_installed = False
    
    return all_installed

def check_database_connection():
    """Check database connection"""
    print("\nChecking database connection...")
    try:
        from models import db
        from flask import Flask
        
        app = Flask(__name__)
        database_url = os.environ.get('DATABASE_URL', 'postgresql://asset_admin:asset_secure_pass_2026@localhost:5432/asset_management')
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db.init_app(app)
        
        with app.app_context():
            # Try to connect
            db.engine.connect()
            print(f"✓ Database connection successful")
            print(f"  URL: {database_url.split('@')[1] if '@' in database_url else 'localhost'}")
            return True
            
    except Exception as e:
        print(f"✗ Database connection failed: {str(e)}")
        return False

def check_database_tables():
    """Check if database tables exist"""
    print("\nChecking database tables...")
    try:
        from models import db, Asset, Ticket, TicketReply, TicketNote, Request
        from flask import Flask
        
        app = Flask(__name__)
        database_url = os.environ.get('DATABASE_URL', 'postgresql://asset_admin:asset_secure_pass_2026@localhost:5432/asset_management')
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db.init_app(app)
        
        with app.app_context():
            tables = {
                'assets': Asset,
                'tickets': Ticket,
                'ticket_replies': TicketReply,
                'ticket_notes': TicketNote,
                'requests': Request
            }
            
            all_exist = True
            for table_name, model in tables.items():
                try:
                    count = model.query.count()
                    print(f"✓ {table_name} ({count} records)")
                except Exception as e:
                    print(f"✗ {table_name} (Table doesn't exist)")
                    all_exist = False
            
            return all_exist
            
    except Exception as e:
        print(f"✗ Error checking tables: {str(e)}")
        return False

def check_files():
    """Check if required files exist"""
    print("\nChecking required files...")
    required_files = [
        'server.py',
        'models.py',
        'init_db.py',
        'migrate_json_to_postgres.py',
        'requirements.txt',
        'docker-compose.yml',
        'Dockerfile',
        'templates/index.html',
        'static/app.js',
        'static/tickets.js',
        'static/request.js',
        'static/style.css'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} (Missing)")
            all_exist = False
    
    return all_exist

def check_docker():
    """Check if Docker is available"""
    print("\nChecking Docker...")
    try:
        import subprocess
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Docker installed: {result.stdout.strip()}")
            
            # Check if Docker is running
            result = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✓ Docker is running")
                return True
            else:
                print(f"✗ Docker is not running")
                return False
        else:
            print(f"✗ Docker not found")
            return False
    except FileNotFoundError:
        print(f"✗ Docker not installed")
        return False

def check_docker_compose():
    """Check if Docker Compose is available"""
    print("\nChecking Docker Compose...")
    try:
        import subprocess
        result = subprocess.run(['docker-compose', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Docker Compose installed: {result.stdout.strip()}")
            return True
        else:
            print(f"✗ Docker Compose not found")
            return False
    except FileNotFoundError:
        print(f"✗ Docker Compose not installed")
        return False

def main():
    """Run all checks"""
    print("=" * 60)
    print("IT Asset Management System - Setup Verification")
    print("=" * 60)
    
    results = {
        'Python Version': check_python_version(),
        'Dependencies': check_dependencies(),
        'Required Files': check_files(),
        'Docker': check_docker(),
        'Docker Compose': check_docker_compose(),
        'Database Connection': check_database_connection(),
        'Database Tables': check_database_tables()
    }
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    for check, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{check:.<40} {status}")
    
    print("=" * 60)
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n✓ All checks passed! System is ready to use.")
        print("\nTo start the application:")
        print("  Docker:  docker-compose up -d")
        print("  Manual:  python server.py")
    else:
        print("\n✗ Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  - Install dependencies: pip install -r requirements.txt")
        print("  - Initialize database: python init_db.py")
        print("  - Install Docker: https://www.docker.com/products/docker-desktop")
        print("  - Start PostgreSQL: docker-compose up -d postgres")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())

"""
Test script to verify PostgreSQL migration
"""
import os
import sys
from datetime import datetime

def test_database_connection():
    """Test database connection"""
    print("Testing database connection...")
    try:
        from models import db
        from flask import Flask
        
        app = Flask(__name__)
        database_url = os.environ.get('DATABASE_URL', 'postgresql://asset_admin:asset_secure_pass_2026@localhost:5432/asset_management')
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db.init_app(app)
        
        with app.app_context():
            db.engine.connect()
            print("✓ Database connection successful")
            return True
    except Exception as e:
        print(f"✗ Database connection failed: {str(e)}")
        return False

def test_models():
    """Test all models"""
    print("\nTesting database models...")
    try:
        from models import db, Asset, Ticket, TicketReply, TicketNote, Request
        from flask import Flask
        
        app = Flask(__name__)
        database_url = os.environ.get('DATABASE_URL', 'postgresql://asset_admin:asset_secure_pass_2026@localhost:5432/asset_management')
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db.init_app(app)
        
        with app.app_context():
            # Test Asset model
            asset_count = Asset.query.count()
            print(f"✓ Asset model working ({asset_count} records)")
            
            # Test Ticket model
            ticket_count = Ticket.query.count()
            print(f"✓ Ticket model working ({ticket_count} records)")
            
            # Test TicketReply model
            reply_count = TicketReply.query.count()
            print(f"✓ TicketReply model working ({reply_count} records)")
            
            # Test TicketNote model
            note_count = TicketNote.query.count()
            print(f"✓ TicketNote model working ({note_count} records)")
            
            # Test Request model
            request_count = Request.query.count()
            print(f"✓ Request model working ({request_count} records)")
            
            return True
    except Exception as e:
        print(f"✗ Model test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_crud_operations():
    """Test CRUD operations"""
    print("\nTesting CRUD operations...")
    try:
        from models import db, Asset
        from flask import Flask
        
        app = Flask(__name__)
        database_url = os.environ.get('DATABASE_URL', 'postgresql://asset_admin:asset_secure_pass_2026@localhost:5432/asset_management')
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db.init_app(app)
        
        with app.app_context():
            # Create
            test_asset = Asset(
                id=999999999,
                type='laptop',
                asset_id='TEST-001',
                model='Test Model',
                status='available',
                serial_number='TEST123'
            )
            db.session.add(test_asset)
            db.session.commit()
            print("✓ Create operation successful")
            
            # Read
            asset = Asset.query.filter_by(id=999999999).first()
            if asset and asset.asset_id == 'TEST-001':
                print("✓ Read operation successful")
            else:
                print("✗ Read operation failed")
                return False
            
            # Update
            asset.model = 'Updated Model'
            db.session.commit()
            
            updated_asset = Asset.query.filter_by(id=999999999).first()
            if updated_asset.model == 'Updated Model':
                print("✓ Update operation successful")
            else:
                print("✗ Update operation failed")
                return False
            
            # Delete
            db.session.delete(updated_asset)
            db.session.commit()
            
            deleted_asset = Asset.query.filter_by(id=999999999).first()
            if deleted_asset is None:
                print("✓ Delete operation successful")
            else:
                print("✗ Delete operation failed")
                return False
            
            return True
    except Exception as e:
        print(f"✗ CRUD test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_relationships():
    """Test model relationships"""
    print("\nTesting model relationships...")
    try:
        from models import db, Ticket, TicketReply, TicketNote
        from flask import Flask
        
        app = Flask(__name__)
        database_url = os.environ.get('DATABASE_URL', 'postgresql://asset_admin:asset_secure_pass_2026@localhost:5432/asset_management')
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db.init_app(app)
        
        with app.app_context():
            # Create test ticket
            test_ticket = Ticket(
                id=999999999,
                ticket_number=9999,
                subject='Test Ticket',
                from_email='test@example.com',
                body='Test body',
                status='open',
                date=datetime.now()
            )
            db.session.add(test_ticket)
            db.session.commit()
            print("✓ Test ticket created")
            
            # Add reply
            test_reply = TicketReply(
                ticket_id=test_ticket.id,
                message='Test reply',
                to_email='test@example.com',
                type='manual',
                date=datetime.now()
            )
            db.session.add(test_reply)
            db.session.commit()
            print("✓ Test reply added")
            
            # Add note
            test_note = TicketNote(
                ticket_id=test_ticket.id,
                text='Test note',
                date=datetime.now()
            )
            db.session.add(test_note)
            db.session.commit()
            print("✓ Test note added")
            
            # Test relationships
            ticket = Ticket.query.filter_by(id=999999999).first()
            if ticket:
                if len(ticket.replies) > 0:
                    print("✓ Ticket-Reply relationship working")
                else:
                    print("✗ Ticket-Reply relationship failed")
                    return False
                
                if len(ticket.notes) > 0:
                    print("✓ Ticket-Note relationship working")
                else:
                    print("✗ Ticket-Note relationship failed")
                    return False
            
            # Cleanup
            db.session.delete(test_reply)
            db.session.delete(test_note)
            db.session.delete(test_ticket)
            db.session.commit()
            print("✓ Test data cleaned up")
            
            return True
    except Exception as e:
        print(f"✗ Relationship test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_to_dict_methods():
    """Test to_dict() methods"""
    print("\nTesting to_dict() methods...")
    try:
        from models import db, Asset, Ticket, Request
        from flask import Flask
        
        app = Flask(__name__)
        database_url = os.environ.get('DATABASE_URL', 'postgresql://asset_admin:asset_secure_pass_2026@localhost:5432/asset_management')
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db.init_app(app)
        
        with app.app_context():
            # Test Asset.to_dict()
            asset = Asset.query.first()
            if asset:
                asset_dict = asset.to_dict()
                if isinstance(asset_dict, dict) and 'id' in asset_dict:
                    print("✓ Asset.to_dict() working")
                else:
                    print("✗ Asset.to_dict() failed")
                    return False
            else:
                print("⚠ No assets to test (skipping)")
            
            # Test Ticket.to_dict()
            ticket = Ticket.query.first()
            if ticket:
                ticket_dict = ticket.to_dict()
                if isinstance(ticket_dict, dict) and 'id' in ticket_dict:
                    print("✓ Ticket.to_dict() working")
                else:
                    print("✗ Ticket.to_dict() failed")
                    return False
            else:
                print("⚠ No tickets to test (skipping)")
            
            # Test Request.to_dict()
            req = Request.query.first()
            if req:
                req_dict = req.to_dict()
                if isinstance(req_dict, dict) and 'id' in req_dict:
                    print("✓ Request.to_dict() working")
                else:
                    print("✗ Request.to_dict() failed")
                    return False
            else:
                print("⚠ No requests to test (skipping)")
            
            return True
    except Exception as e:
        print(f"✗ to_dict() test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("PostgreSQL Migration Test Suite")
    print("=" * 60)
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Database Models", test_models),
        ("CRUD Operations", test_crud_operations),
        ("Model Relationships", test_relationships),
        ("to_dict() Methods", test_to_dict_methods)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n✗ {test_name} crashed: {str(e)}")
            results[test_name] = False
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:.<40} {status}")
    
    print("=" * 60)
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n✓ All tests passed! Migration is working correctly.")
    else:
        print("\n✗ Some tests failed. Please review the errors above.")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())

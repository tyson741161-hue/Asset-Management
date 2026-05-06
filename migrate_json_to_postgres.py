"""
Migration script to transfer data from JSON files to PostgreSQL database
"""
import os
import json
from datetime import datetime
from models import db, Asset, Ticket, TicketReply, TicketNote, Request
from flask import Flask

def parse_date(date_str):
    """Parse date string to datetime object"""
    if not date_str:
        return datetime.utcnow()
    
    try:
        # Try ISO format first
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except:
        try:
            # Try other common formats
            return datetime.strptime(date_str, '%Y-%m-%d')
        except:
            return datetime.utcnow()

def migrate_assets(assets_data):
    """Migrate assets from JSON to database"""
    print("\nMigrating assets...")
    count = 0
    
    for asset_json in assets_data:
        try:
            asset = Asset(
                id=asset_json.get('id'),
                asset_id=asset_json.get('assetId'),
                type=asset_json.get('type'),
                model=asset_json.get('model'),
                status=asset_json.get('status', 'available'),
                serial_number=asset_json.get('serialNumber'),
                configuration=asset_json.get('configuration'),
                office_location=asset_json.get('officeLocation'),
                location=asset_json.get('location'),
                year=int(asset_json['year']) if asset_json.get('year') and str(asset_json['year']).isdigit() else None,
                current_condition=asset_json.get('currentCondition'),
                current_user=asset_json.get('currentUser'),
                last_user=asset_json.get('lastUser'),
                quantity=asset_json.get('quantity'),
                mouse_type=asset_json.get('mouseType'),
                firewall_name=asset_json.get('firewallName'),
                purchase_year=int(asset_json['purchaseYear']) if asset_json.get('purchaseYear') else None,
                last_firmware_update=parse_date(asset_json.get('lastFirmwareUpdate')).date() if asset_json.get('lastFirmwareUpdate') else None,
                ram_name=asset_json.get('ramName'),
                ram_size=asset_json.get('ramSize'),
                ram_ddr=asset_json.get('ramDDR'),
                ram_frequency=asset_json.get('ramFrequency')
            )
            
            # Handle laptop accessories
            if asset_json.get('accessories'):
                accessories = asset_json['accessories']
                asset.mouse_name = accessories.get('mouse')
                asset.headphone_name = accessories.get('headphone')
                asset.charger_name = accessories.get('charger')
                asset.monitor_name = accessories.get('monitor')
            else:
                asset.mouse_name = asset_json.get('mouseName')
                asset.headphone_name = asset_json.get('headphoneName')
                asset.charger_name = asset_json.get('chargerName')
                asset.monitor_name = asset_json.get('monitorName')
            
            db.session.add(asset)
            count += 1
            
        except Exception as e:
            print(f"Error migrating asset {asset_json.get('id')}: {str(e)}")
    
    db.session.commit()
    print(f"✓ Migrated {count} assets")
    return count

def migrate_tickets(tickets_data):
    """Migrate tickets from JSON to database"""
    print("\nMigrating tickets...")
    count = 0
    
    for ticket_json in tickets_data:
        try:
            ticket = Ticket(
                id=ticket_json.get('id'),
                ticket_number=ticket_json.get('ticket_number', 1001),
                subject=ticket_json.get('subject', ''),
                from_email=ticket_json.get('from_email'),
                body=ticket_json.get('body'),
                status=ticket_json.get('status', 'open'),
                date=parse_date(ticket_json.get('date'))
            )
            
            db.session.add(ticket)
            db.session.flush()  # Get the ticket ID
            
            # Migrate replies
            if ticket_json.get('replies'):
                for reply_json in ticket_json['replies']:
                    reply = TicketReply(
                        ticket_id=ticket.id,
                        message=reply_json.get('message'),
                        to_email=reply_json.get('to'),
                        type=reply_json.get('type', 'manual'),
                        date=parse_date(reply_json.get('date'))
                    )
                    db.session.add(reply)
            
            # Migrate notes
            if ticket_json.get('notes'):
                for note_json in ticket_json['notes']:
                    note = TicketNote(
                        ticket_id=ticket.id,
                        text=note_json.get('text'),
                        date=parse_date(note_json.get('date'))
                    )
                    db.session.add(note)
            
            count += 1
            
        except Exception as e:
            print(f"Error migrating ticket {ticket_json.get('id')}: {str(e)}")
            import traceback
            traceback.print_exc()
    
    db.session.commit()
    print(f"✓ Migrated {count} tickets")
    return count

def migrate_requests(requests_data):
    """Migrate requests from JSON to database"""
    print("\nMigrating requests...")
    count = 0
    
    for request_json in requests_data:
        try:
            request = Request(
                id=request_json.get('id'),
                email=request_json.get('email'),
                subject=request_json.get('subject'),
                description=request_json.get('description'),
                date=parse_date(request_json.get('date'))
            )
            
            db.session.add(request)
            count += 1
            
        except Exception as e:
            print(f"Error migrating request {request_json.get('id')}: {str(e)}")
    
    db.session.commit()
    print(f"✓ Migrated {count} requests")
    return count

def run_migration():
    """Run the complete migration"""
    
    # Create Flask app
    app = Flask(__name__)
    
    # Get database URL from environment or use default
    database_url = os.environ.get('DATABASE_URL', 'postgresql://asset_admin:asset_secure_pass_2026@localhost:5432/asset_management')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    with app.app_context():
        print("=" * 60)
        print("Starting JSON to PostgreSQL Migration")
        print("=" * 60)
        
        # Load JSON data
        print("\nLoading JSON files...")
        
        assets_data = []
        tickets_data = []
        requests_data = []
        
        try:
            if os.path.exists('assets_data.json'):
                with open('assets_data.json', 'r') as f:
                    assets_data = json.load(f)
                print(f"✓ Loaded {len(assets_data)} assets from JSON")
        except Exception as e:
            print(f"✗ Error loading assets: {str(e)}")
        
        try:
            if os.path.exists('tickets_data.json'):
                with open('tickets_data.json', 'r') as f:
                    tickets_data = json.load(f)
                print(f"✓ Loaded {len(tickets_data)} tickets from JSON")
        except Exception as e:
            print(f"✗ Error loading tickets: {str(e)}")
        
        try:
            if os.path.exists('requests_data.json'):
                with open('requests_data.json', 'r') as f:
                    requests_data = json.load(f)
                print(f"✓ Loaded {len(requests_data)} requests from JSON")
        except Exception as e:
            print(f"✗ Error loading requests: {str(e)}")
        
        # Migrate data
        total_assets = migrate_assets(assets_data)
        total_tickets = migrate_tickets(tickets_data)
        total_requests = migrate_requests(requests_data)
        
        print("\n" + "=" * 60)
        print("Migration Summary")
        print("=" * 60)
        print(f"Assets migrated:   {total_assets}")
        print(f"Tickets migrated:  {total_tickets}")
        print(f"Requests migrated: {total_requests}")
        print("=" * 60)
        print("\n✓ Migration completed successfully!")

if __name__ == '__main__':
    try:
        run_migration()
    except Exception as e:
        print(f"\n✗ Migration failed: {str(e)}")
        import traceback
        traceback.print_exc()

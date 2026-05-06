"""
Export PostgreSQL database data to JSON files for backup
"""
import os
import json
from models import db, Asset, Ticket, Request
from flask import Flask

def export_to_json():
    """Export all database data to JSON files"""
    
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
        print("Exporting PostgreSQL Database to JSON")
        print("=" * 60)
        
        # Export assets
        print("\nExporting assets...")
        assets = Asset.query.all()
        assets_data = [asset.to_dict() for asset in assets]
        
        with open('assets_data_backup.json', 'w') as f:
            json.dump(assets_data, f, indent=2)
        print(f"✓ Exported {len(assets_data)} assets to assets_data_backup.json")
        
        # Export tickets
        print("\nExporting tickets...")
        tickets = Ticket.query.all()
        tickets_data = [ticket.to_dict() for ticket in tickets]
        
        with open('tickets_data_backup.json', 'w') as f:
            json.dump(tickets_data, f, indent=2)
        print(f"✓ Exported {len(tickets_data)} tickets to tickets_data_backup.json")
        
        # Export requests
        print("\nExporting requests...")
        requests = Request.query.all()
        requests_data = [req.to_dict() for req in requests]
        
        with open('requests_data_backup.json', 'w') as f:
            json.dump(requests_data, f, indent=2)
        print(f"✓ Exported {len(requests_data)} requests to requests_data_backup.json")
        
        print("\n" + "=" * 60)
        print("Export Summary")
        print("=" * 60)
        print(f"Assets exported:   {len(assets_data)}")
        print(f"Tickets exported:  {len(tickets_data)}")
        print(f"Requests exported: {len(requests_data)}")
        print("=" * 60)
        print("\n✓ Export completed successfully!")
        print("\nBackup files created:")
        print("  - assets_data_backup.json")
        print("  - tickets_data_backup.json")
        print("  - requests_data_backup.json")

if __name__ == '__main__':
    try:
        export_to_json()
    except Exception as e:
        print(f"\n✗ Export failed: {str(e)}")
        import traceback
        traceback.print_exc()

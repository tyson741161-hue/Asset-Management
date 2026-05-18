"""
Local runner - SQLite backend (no PostgreSQL required).
Migrates JSON data on first run, then starts the Flask server.

Usage:
    cd Asset-Management
    python run_local_sqlite.py
"""
import os
import json
from datetime import datetime

# Use SQLite instead of PostgreSQL
_base_dir = os.path.abspath(os.path.dirname(__file__))
_db_path = os.path.join(_base_dir, 'instance', 'asset_management.db')
os.makedirs(os.path.dirname(_db_path), exist_ok=True)
os.environ['DATABASE_URL'] = f'sqlite:///{_db_path}'

from flask import Flask
from models import db, Asset, Ticket, TicketReply, TicketNote, Request, EmailConfig

setup_app = Flask(__name__)
setup_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
setup_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(setup_app)


def parse_date(date_str):
    if not date_str:
        return datetime.utcnow()
    for fmt in ('%Y-%m-%dT%H:%M:%S.%f%z', '%Y-%m-%dT%H:%M:%S%z',
                '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d'):
        try:
            return datetime.strptime(date_str[:26], fmt[:len(date_str[:26])])
        except Exception:
            pass
    try:
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except Exception:
        return datetime.utcnow()


with setup_app.app_context():
    # Create tables
    db.create_all()
    print("[OK] Database tables ready.")

    # Migrate Assets
    if Asset.query.count() == 0:
        print("[..] Migrating assets from assets_data.json ...")
        try:
            with open('assets_data.json', 'r', encoding='utf-8') as f:
                assets_data = json.load(f)
            count = 0
            for a in assets_data:
                try:
                    asset = Asset(
                        id=a.get('id'),
                        asset_id=a.get('assetId'),
                        type=a.get('type') or 'Unknown',
                        model=a.get('model'),
                        status=a.get('status', 'available'),
                        serial_number=a.get('serialNumber'),
                        configuration=a.get('configuration'),
                        office_location=a.get('officeLocation'),
                        location=a.get('location'),
                        year=int(a['year']) if a.get('year') and str(a['year']).isdigit() else None,
                        current_condition=a.get('currentCondition'),
                        current_user=a.get('currentUser'),
                        last_user=a.get('lastUser'),
                        quantity=a.get('quantity'),
                        mouse_type=a.get('mouseType'),
                        firewall_name=a.get('firewallName'),
                        purchase_year=int(a['purchaseYear']) if a.get('purchaseYear') else None,
                        last_firmware_update=parse_date(a['lastFirmwareUpdate']).date() if a.get('lastFirmwareUpdate') else None,
                        ram_name=a.get('ramName'),
                        ram_size=a.get('ramSize'),
                        ram_ddr=a.get('ramDDR'),
                        ram_frequency=a.get('ramFrequency'),
                        mouse_name=a.get('accessories', {}).get('mouse') or a.get('mouseName'),
                        headphone_name=a.get('accessories', {}).get('headphone') or a.get('headphoneName'),
                        charger_name=a.get('accessories', {}).get('charger') or a.get('chargerName'),
                        monitor_name=a.get('accessories', {}).get('monitor') or a.get('monitorName'),
                    )
                    db.session.add(asset)
                    count += 1
                except Exception as e:
                    print(f"  [WARN] Skipping asset {a.get('id')}: {e}")
            db.session.commit()
            print(f"[OK] Migrated {count} assets.")
        except Exception as e:
            print(f"[ERR] Asset migration failed: {e}")
    else:
        print(f"[OK] Assets already in DB ({Asset.query.count()} records), skipping.")

    # Migrate Tickets
    if Ticket.query.count() == 0:
        print("[..] Migrating tickets from tickets_data.json ...")
        try:
            with open('tickets_data.json', 'r', encoding='utf-8') as f:
                tickets_data = json.load(f)
            count = 0
            for t in tickets_data:
                try:
                    ticket = Ticket(
                        id=t.get('id'),
                        ticket_number=t.get('ticket_number', 1001 + count),
                        subject=t.get('subject') or '(no subject)',
                        from_email=t.get('from_email') or 'unknown@unknown.com',
                        body=t.get('body'),
                        status=t.get('status', 'open'),
                        priority=t.get('priority', 'medium'),
                        date=parse_date(t.get('date')),
                    )
                    db.session.add(ticket)
                    db.session.flush()
                    for r in t.get('replies', []):
                        db.session.add(TicketReply(
                            ticket_id=ticket.id,
                            message=r.get('message', ''),
                            to_email=r.get('to'),
                            type=r.get('type', 'manual'),
                            date=parse_date(r.get('date')),
                        ))
                    for n in t.get('notes', []):
                        db.session.add(TicketNote(
                            ticket_id=ticket.id,
                            text=n.get('text', ''),
                            date=parse_date(n.get('date')),
                        ))
                    count += 1
                except Exception as e:
                    print(f"  [WARN] Skipping ticket {t.get('id')}: {e}")
            db.session.commit()
            print(f"[OK] Migrated {count} tickets.")
        except Exception as e:
            print(f"[ERR] Ticket migration failed: {e}")
    else:
        print(f"[OK] Tickets already in DB ({Ticket.query.count()} records), skipping.")

    # Migrate Requests
    if Request.query.count() == 0:
        print("[..] Migrating requests from requests_data.json ...")
        try:
            with open('requests_data.json', 'r', encoding='utf-8') as f:
                requests_data = json.load(f)
            count = 0
            for r in requests_data:
                try:
                    req = Request(
                        id=r.get('id'),
                        email=r.get('email') or 'unknown@unknown.com',
                        subject=r.get('subject') or '(no subject)',
                        description=r.get('description') or '',
                        date=parse_date(r.get('date')),
                    )
                    db.session.add(req)
                    count += 1
                except Exception as e:
                    print(f"  [WARN] Skipping request {r.get('id')}: {e}")
            db.session.commit()
            print(f"[OK] Migrated {count} requests.")
        except Exception as e:
            print(f"[ERR] Request migration failed: {e}")
    else:
        print(f"[OK] Requests already in DB ({Request.query.count()} records), skipping.")


print()
print("=" * 50)
print("  IT Asset Management System")
print("  URL   : http://localhost:5000")
print("  DB    : SQLite (instance/asset_management.db)")
print("  Login : admin / admin")
print("  PIN   : 4181")
print("=" * 50)
print()

import server as srv
srv.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
with srv.app.app_context():
    db.create_all()
srv.app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

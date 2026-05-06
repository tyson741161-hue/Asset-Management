#!/usr/bin/env python3
"""
Diagnostic script to check email fetching and ticket creation
Run this on the server to diagnose why tickets are not being created
"""

from imap_tools import MailBox, AND
from datetime import datetime

# Email configuration
IMAP_SERVER = 'imap.gmail.com'
IMAP_USERNAME = 'tyson741161@gmail.com'
IMAP_PASSWORD = 'sdxr csld bahs fpeg'

print("=" * 60)
print("EMAIL & TICKET DIAGNOSTIC TOOL")
print("=" * 60)
print()

# Step 1: Check IMAP connection
print("Step 1: Testing IMAP connection...")
try:
    with MailBox(IMAP_SERVER).login(IMAP_USERNAME, IMAP_PASSWORD) as mailbox:
        print("✓ Successfully connected to Gmail IMAP")
        print()
        
        # Step 2: Check unread emails
        print("Step 2: Checking for UNREAD emails...")
        unread_messages = list(mailbox.fetch(AND(seen=False), limit=20, reverse=True))
        print(f"Found {len(unread_messages)} UNREAD emails")
        
        if unread_messages:
            print("\nUnread emails:")
            for i, msg in enumerate(unread_messages, 1):
                print(f"\n  {i}. Subject: {msg.subject}")
                print(f"     From: {msg.from_}")
                print(f"     Date: {msg.date}")
                print(f"     UID: {msg.uid}")
                body_preview = (msg.text or msg.html or '')[:100]
                print(f"     Body: {body_preview}...")
        else:
            print("  ⚠ No unread emails found!")
            print("  This means all emails have been marked as read.")
        
        print()
        
        # Step 3: Check ALL recent emails (including read)
        print("Step 3: Checking ALL recent emails (last 10)...")
        all_messages = list(mailbox.fetch(limit=10, reverse=True))
        print(f"Found {len(all_messages)} total recent emails")
        
        if all_messages:
            print("\nRecent emails (including read):")
            for i, msg in enumerate(all_messages, 1):
                is_read = '\\Seen' in msg.flags
                status = "READ" if is_read else "UNREAD"
                print(f"\n  {i}. [{status}] Subject: {msg.subject}")
                print(f"     From: {msg.from_}")
                print(f"     Date: {msg.date}")
                print(f"     Flags: {msg.flags}")
        
        print()
        
except Exception as e:
    print(f"✗ Error connecting to Gmail: {str(e)}")
    import traceback
    traceback.print_exc()
    print()

# Step 4: Check database connection and tickets
print("Step 4: Checking database and existing tickets...")
try:
    from models import db, Ticket
    from flask import Flask
    import os
    
    app = Flask(__name__)
    database_url = os.environ.get('DATABASE_URL', 'postgresql://asset_admin:asset_secure_pass_2026@postgres:5432/asset_management')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        ticket_count = Ticket.query.count()
        print(f"✓ Database connected successfully")
        print(f"  Total tickets in database: {ticket_count}")
        
        if ticket_count > 0:
            latest_tickets = Ticket.query.order_by(Ticket.date.desc()).limit(5).all()
            print(f"\n  Latest {len(latest_tickets)} tickets:")
            for ticket in latest_tickets:
                print(f"    - #{ticket.ticket_number}: {ticket.subject}")
                print(f"      From: {ticket.from_email}")
                print(f"      Date: {ticket.date}")
                print(f"      Status: {ticket.status}")
        
        # Check next ticket number
        max_ticket = db.session.query(db.func.max(Ticket.ticket_number)).scalar()
        next_ticket_num = (max_ticket + 1) if max_ticket else 1001
        print(f"\n  Next ticket number will be: {next_ticket_num}")
        
except Exception as e:
    print(f"✗ Error checking database: {str(e)}")
    import traceback
    traceback.print_exc()

print()
print("=" * 60)
print("DIAGNOSTIC COMPLETE")
print("=" * 60)
print()
print("TROUBLESHOOTING TIPS:")
print("1. If no UNREAD emails found: Send a new test email to tyson741161@gmail.com")
print("2. If emails are marked as READ: They were already processed or read in Gmail")
print("3. Check the web UI at http://192.168.2.10:5000 and click 'Refresh Tickets'")
print("4. Auto-refresh happens every 30 seconds when on the Tickets tab")
print("5. Make sure you're logged in to the web interface (admin/admin)")
print()

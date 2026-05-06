#!/usr/bin/env python3
"""
Test the complete email-to-ticket creation flow
This simulates what happens when you click "Refresh Tickets" in the web interface
"""

import os
import sys

# Set up Flask app context
from flask import Flask
from models import db, Ticket
from server import fetch_emails_as_tickets

# Database configuration
database_url = os.environ.get('DATABASE_URL', 'postgresql://asset_admin:asset_secure_pass_2026@postgres:5432/asset_management')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

print("=" * 60)
print("TICKET CREATION TEST")
print("=" * 60)
print()

with app.app_context():
    # Show current ticket count
    print("Step 1: Checking current tickets in database...")
    current_count = Ticket.query.count()
    print(f"  Current ticket count: {current_count}")
    
    if current_count > 0:
        latest = Ticket.query.order_by(Ticket.date.desc()).first()
        print(f"  Latest ticket: #{latest.ticket_number} - {latest.subject}")
    
    # Get next ticket number
    max_ticket = db.session.query(db.func.max(Ticket.ticket_number)).scalar()
    next_ticket_num = (max_ticket + 1) if max_ticket else 1001
    print(f"  Next ticket number: {next_ticket_num}")
    print()
    
    # Fetch emails and create tickets
    print("Step 2: Fetching emails and creating tickets...")
    print("-" * 60)
    new_tickets = fetch_emails_as_tickets()
    print("-" * 60)
    print()
    
    # Show results
    print("Step 3: Results")
    if new_tickets:
        print(f"  ✓ Successfully created {len(new_tickets)} new ticket(s)!")
        print()
        print("  New tickets:")
        for ticket in new_tickets:
            print(f"    - Ticket #{ticket['ticket_number']}")
            print(f"      Subject: {ticket['subject']}")
            print(f"      From: {ticket['from_email']}")
            print(f"      Date: {ticket['date']}")
            print(f"      Status: {ticket['status']}")
            print()
    else:
        print("  ⚠ No new tickets created")
        print()
        print("  Possible reasons:")
        print("    1. No unread emails in the inbox")
        print("    2. All emails were already processed")
        print("    3. Email connection issue (check logs above)")
        print()
        print("  To test:")
        print("    1. Send a new email to tyson741161@gmail.com")
        print("    2. Don't open it in Gmail")
        print("    3. Run this script again")
        print()
    
    # Show final ticket count
    final_count = Ticket.query.count()
    print(f"  Final ticket count: {final_count}")
    print(f"  Tickets created: {final_count - current_count}")

print()
print("=" * 60)
print("TEST COMPLETE")
print("=" * 60)
print()
print("To view tickets in the web interface:")
print("  1. Go to http://192.168.2.10:5000")
print("  2. Login with admin/admin")
print("  3. Click 'Tickets' tab")
print()

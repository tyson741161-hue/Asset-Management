#!/usr/bin/env python3
"""
Check all recent emails to find the test email
"""

from imap_tools import MailBox

# Email configuration
IMAP_SERVER = 'imap.gmail.com'
IMAP_USERNAME = 'tyson741161@gmail.com'
IMAP_PASSWORD = 'sdxr csld bahs fpeg'

print("Checking ALL recent emails (including read ones)...\n")

try:
    with MailBox(IMAP_SERVER).login(IMAP_USERNAME, IMAP_PASSWORD) as mailbox:
        # Get ALL recent emails (not just unread)
        all_messages = list(mailbox.fetch(limit=20, reverse=True))
        
        print(f"Found {len(all_messages)} recent emails:\n")
        
        for i, msg in enumerate(all_messages, 1):
            status = "UNREAD" if '\\Seen' not in msg.flags else "READ"
            print(f"{i}. [{status}]")
            print(f"   From: {msg.from_}")
            print(f"   Subject: {msg.subject}")
            print(f"   Date: {msg.date}")
            print(f"   Body preview: {(msg.text or msg.html or '')[:100]}...")
            print()
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

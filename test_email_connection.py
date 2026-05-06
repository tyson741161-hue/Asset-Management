#!/usr/bin/env python3
"""
Test script to verify email connection and IMAP access
"""

from imap_tools import MailBox, AND

# Email configuration
IMAP_SERVER = 'imap.gmail.com'
IMAP_USERNAME = 'tyson741161@gmail.com'
IMAP_PASSWORD = 'sdxr csld bahs fpeg'  # Your App Password

print("=" * 60)
print("Testing Email Connection")
print("=" * 60)

print(f"\nIMAP Server: {IMAP_SERVER}")
print(f"Username: {IMAP_USERNAME}")
print(f"Password: {'*' * len(IMAP_PASSWORD)} (length: {len(IMAP_PASSWORD)})")

try:
    print("\n1. Connecting to mailbox...")
    with MailBox(IMAP_SERVER).login(IMAP_USERNAME, IMAP_PASSWORD) as mailbox:
        print("✓ Successfully connected!")
        
        print("\n2. Checking for unread emails...")
        unread_messages = list(mailbox.fetch(AND(seen=False), limit=10, reverse=True))
        print(f"✓ Found {len(unread_messages)} unread email(s)")
        
        if unread_messages:
            print("\n3. Unread emails:")
            for i, msg in enumerate(unread_messages, 1):
                print(f"\n   Email #{i}:")
                print(f"   From: {msg.from_}")
                print(f"   Subject: {msg.subject}")
                print(f"   Date: {msg.date}")
                print(f"   Body preview: {(msg.text or msg.html or '')[:100]}...")
        else:
            print("\n   No unread emails found.")
            print("   Try sending a test email to tyson741161@gmail.com")
        
        print("\n4. Checking all recent emails (last 5)...")
        all_messages = list(mailbox.fetch(limit=5, reverse=True))
        print(f"✓ Found {len(all_messages)} recent email(s)")
        
        if all_messages:
            print("\n   Recent emails:")
            for i, msg in enumerate(all_messages, 1):
                # Check if message has been seen using flags
                status = "READ" if '\\Seen' in msg.flags else "UNREAD"
                print(f"   {i}. [{status}] From: {msg.from_} | Subject: {msg.subject}")
        
        print("\n" + "=" * 60)
        print("✓ Email connection test SUCCESSFUL!")
        print("=" * 60)
        
except Exception as e:
    print("\n" + "=" * 60)
    print("✗ Email connection test FAILED!")
    print("=" * 60)
    print(f"\nError: {str(e)}")
    print("\nPossible issues:")
    print("1. IMAP is not enabled in Gmail settings")
    print("2. App Password is incorrect")
    print("3. 2-Factor Authentication is not enabled")
    print("4. Internet connection issue")
    print("\nTo fix:")
    print("1. Go to Gmail Settings → Forwarding and POP/IMAP")
    print("2. Enable IMAP")
    print("3. Generate a new App Password at https://myaccount.google.com/apppasswords")
    
    import traceback
    print("\nFull error details:")
    traceback.print_exc()

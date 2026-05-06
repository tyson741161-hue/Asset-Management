#!/usr/bin/env python3
"""
Mark all current emails as READ so only NEW emails from now on will be fetched
"""

from imap_tools import MailBox, AND

# Email configuration
IMAP_SERVER = 'imap.gmail.com'
IMAP_USERNAME = 'tyson741161@gmail.com'
IMAP_PASSWORD = 'sdxr csld bahs fpeg'

print("=" * 60)
print("Marking all current emails as READ")
print("=" * 60)

try:
    with MailBox(IMAP_SERVER).login(IMAP_USERNAME, IMAP_PASSWORD) as mailbox:
        print("\nConnected to mailbox successfully")
        
        # Get all UNREAD emails
        unread_messages = list(mailbox.fetch(AND(seen=False)))
        print(f"Found {len(unread_messages)} unread emails")
        
        if unread_messages:
            print("\nMarking emails as read:")
            for msg in unread_messages:
                print(f"  - {msg.subject[:50]}...")
                mailbox.flag(msg.uid, ['\\Seen'], True)
            
            print(f"\n✓ Successfully marked {len(unread_messages)} emails as READ")
            print("\nFrom now on, only NEW emails will be fetched as tickets!")
        else:
            print("\nNo unread emails found. All emails are already marked as read.")
        
        print("\n" + "=" * 60)
        print("Done! You can now start fresh.")
        print("=" * 60)
        
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()

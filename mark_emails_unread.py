#!/usr/bin/env python3
"""
Mark recent emails as UNREAD so they can be fetched again by the ticket system
Use this if you want to re-process emails that were already marked as read
"""

from imap_tools import MailBox
import sys

# Email configuration
IMAP_SERVER = 'imap.gmail.com'
IMAP_USERNAME = 'tyson741161@gmail.com'
IMAP_PASSWORD = 'sdxr csld bahs fpeg'

def mark_recent_emails_unread(limit=5):
    """Mark the most recent emails as unread"""
    print(f"Connecting to {IMAP_SERVER}...")
    
    try:
        with MailBox(IMAP_SERVER).login(IMAP_USERNAME, IMAP_PASSWORD) as mailbox:
            print("Connected successfully!")
            print()
            
            # Get recent emails
            messages = list(mailbox.fetch(limit=limit, reverse=True))
            
            if not messages:
                print("No emails found.")
                return
            
            print(f"Found {len(messages)} recent emails:")
            print()
            
            for i, msg in enumerate(messages, 1):
                is_read = '\\Seen' in msg.flags
                status = "READ" if is_read else "UNREAD"
                
                print(f"{i}. [{status}] {msg.subject}")
                print(f"   From: {msg.from_}")
                print(f"   Date: {msg.date}")
                print()
            
            # Ask for confirmation
            print("=" * 60)
            response = input(f"Mark these {len(messages)} emails as UNREAD? (yes/no): ").strip().lower()
            
            if response != 'yes':
                print("Cancelled.")
                return
            
            print()
            print("Marking emails as unread...")
            
            marked_count = 0
            for msg in messages:
                try:
                    # Remove the \Seen flag to mark as unread
                    mailbox.flag(msg.uid, ['\\Seen'], False)
                    marked_count += 1
                    print(f"✓ Marked as unread: {msg.subject}")
                except Exception as e:
                    print(f"✗ Failed to mark: {msg.subject} - {str(e)}")
            
            print()
            print(f"Successfully marked {marked_count} emails as UNREAD")
            print()
            print("Next steps:")
            print("1. Go to http://192.168.2.10:5000")
            print("2. Login with admin/admin")
            print("3. Click on 'Tickets' tab")
            print("4. Click 'Refresh Tickets' button")
            print("5. The emails should now appear as new tickets!")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    # Get number of emails to mark from command line, default to 5
    limit = 5
    if len(sys.argv) > 1:
        try:
            limit = int(sys.argv[1])
        except ValueError:
            print(f"Invalid number: {sys.argv[1]}")
            print("Usage: python mark_emails_unread.py [number_of_emails]")
            sys.exit(1)
    
    print("=" * 60)
    print("MARK EMAILS AS UNREAD")
    print("=" * 60)
    print()
    
    mark_recent_emails_unread(limit)

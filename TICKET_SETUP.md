# Ticket System Setup Instructions

The ticket system automatically converts emails sent to tyson741161@gmail.com into support tickets.

## Prerequisites

1. **Gmail App Password** (same as email setup)
2. **IMAP Access Enabled** on Gmail

## Setup Steps

### 1. Enable IMAP in Gmail

1. Go to Gmail Settings (gear icon → See all settings)
2. Click on "Forwarding and POP/IMAP" tab
3. Enable IMAP
4. Click "Save Changes"

### 2. Create Gmail App Password

1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification (if not already enabled)
3. Go to https://myaccount.google.com/apppasswords
4. Select "Mail" and "Other (Custom name)"
5. Name it "Asset Management System"
6. Click "Generate"
7. Copy the 16-character password

### 3. Update server.py

Open `server.py` and update these lines:

```python
app.config['MAIL_PASSWORD'] = 'your-16-char-app-password'
IMAP_PASSWORD = 'your-16-char-app-password'  # Same password
```

### 4. Install Required Packages

```bash
pip install -r requirements.txt
```

This will install:
- Flask
- flask-mail
- imap-tools

### 5. Restart the Server

```bash
python server.py
```

## How It Works

1. **Receiving Emails:**
   - Any email sent to tyson741161@gmail.com becomes a ticket
   - Click "Refresh Tickets" to check for new emails
   - Unread emails are automatically converted to tickets

2. **Ticket Status:**
   - **New** - Just received
   - **Open** - Being worked on
   - **Resolved** - Completed

3. **Managing Tickets:**
   - View ticket details by clicking "View"
   - Update status by clicking "Update Status"
   - Filter by status or search tickets

## Testing

1. Send an email to tyson741161@gmail.com from any email address
2. Login to the Asset Management System
3. Click on "Tickets" tab
4. Click "Refresh Tickets" button
5. Your email should appear as a new ticket

## Troubleshooting

**"No tickets found":**
- Make sure IMAP is enabled in Gmail
- Check that App Password is correctly set
- Click "Refresh Tickets" to fetch new emails

**"Failed to refresh tickets":**
- Verify App Password is correct
- Check internet connection
- Make sure 2FA is enabled on Gmail account

**Emails not appearing:**
- Only unread emails are fetched
- Mark emails as unread in Gmail to re-fetch them
- Check spam folder in Gmail

## Security Notes

- Never commit your App Password to version control
- Use environment variables for production
- The App Password gives full access to the email account
- Revoke App Password if compromised

## Alternative: Use Environment Variables

For better security, use environment variables:

1. Create `.env` file:
```
MAIL_PASSWORD=your-app-password
IMAP_PASSWORD=your-app-password
```

2. Update server.py:
```python
import os
from dotenv import load_dotenv

load_dotenv()

app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '')
IMAP_PASSWORD = os.getenv('IMAP_PASSWORD', '')
```

3. Install python-dotenv:
```bash
pip install python-dotenv
```

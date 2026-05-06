# Ticket System Troubleshooting Guide

## How the Ticket System Works

The IT Asset Management System automatically converts emails sent to **tyson741161@gmail.com** into support tickets.

### Email Fetching Process

1. **Only UNREAD emails** are fetched and converted to tickets
2. After creating a ticket, the email is marked as READ to prevent duplicates
3. Emails are fetched in two ways:
   - **Auto-refresh**: Every 30 seconds when you're viewing the Tickets tab
   - **Manual refresh**: Click the "Refresh Tickets" button

### Why Your Email Might Not Appear as a Ticket

1. **Email was already marked as read** - If you opened the email in Gmail before the system fetched it
2. **Not on the Tickets tab** - Auto-refresh only works when viewing the Tickets tab
3. **Not logged in** - You must be logged in to the web interface (admin/admin)
4. **Email was already processed** - The system already created a ticket and marked it as read

## Step-by-Step Troubleshooting

### On the Server (192.168.2.10)

#### 1. Check if Docker containers are running
```bash
docker ps
```
You should see two containers:
- `asset-management-system` (the web app)
- `asset-management-db` (PostgreSQL database)

#### 2. Check application logs
```bash
docker logs asset-management-system
```
Look for:
- "Starting to fetch emails..."
- "Found X unread emails"
- "Creating ticket from email: [subject]"
- Any error messages

#### 3. Run the diagnostic script
```bash
cd ~/asset-management
docker exec -it asset-management-system python diagnose_email_issue.py
```

This will show you:
- IMAP connection status
- Number of unread emails
- Recent emails (read and unread)
- Existing tickets in database
- Next ticket number

#### 4. Check recent emails (including read ones)
```bash
docker exec -it asset-management-system python check_recent_emails.py
```

### On Your Cloud PC or Any Computer

#### 1. Access the web interface
Open browser and go to: **http://192.168.2.10:5000**

#### 2. Login
- Username: `admin`
- Password: `admin`

#### 3. Go to Tickets tab
Click on the "Tickets" tab in the navigation

#### 4. Click "Refresh Tickets" button
This manually triggers email fetching

#### 5. Wait for auto-refresh
Stay on the Tickets tab - it will automatically check for new emails every 30 seconds

## Testing the Ticket System

### Send a Test Email

1. **From any email account**, send an email to: **tyson741161@gmail.com**
   - Subject: "Test Ticket - [Your Name]"
   - Body: "This is a test ticket to verify the system is working"

2. **Important**: Do NOT open this email in Gmail! Let the system fetch it first.

3. **Wait 30 seconds** or click "Refresh Tickets" in the web interface

4. The email should appear as a new ticket with:
   - Ticket number starting from 1001
   - Status: Open
   - All email details

### If the Test Email Doesn't Appear

1. **Check if it was marked as read**:
   ```bash
   docker exec -it asset-management-system python check_recent_emails.py
   ```

2. **Send another test email** (don't open it in Gmail)

3. **Immediately refresh tickets** in the web interface

4. **Check the logs**:
   ```bash
   docker logs asset-management-system --tail 50
   ```

## Common Issues and Solutions

### Issue: "No unread emails found"
**Solution**: All emails have been marked as read. Send a new test email and don't open it in Gmail.

### Issue: Tickets not appearing in web interface
**Solution**: 
- Make sure you're logged in (admin/admin)
- Click "Refresh Tickets" button
- Check browser console for errors (F12)

### Issue: "ERROR fetching emails"
**Solution**: Check the error message in logs:
```bash
docker logs asset-management-system --tail 100
```

### Issue: Email appears but no ticket created
**Solution**: Check if ticket already exists with same timestamp ID:
```bash
docker exec -it asset-management-system python diagnose_email_issue.py
```

## Verifying Email Configuration

The system is configured to use:
- **IMAP Server**: imap.gmail.com
- **Email**: tyson741161@gmail.com
- **App Password**: sdxr csld bahs fpeg

To verify the configuration is working:
```bash
docker exec -it asset-management-system python test_email_connection.py
```

## Manual Email Fetch (For Testing)

If you want to manually trigger email fetching from the server:

```bash
docker exec -it asset-management-system python -c "
from server import app, fetch_emails_as_tickets
with app.app_context():
    tickets = fetch_emails_as_tickets()
    print(f'Created {len(tickets)} new tickets')
"
```

## Checking Ticket Status in Database

To see all tickets directly from the database:

```bash
docker exec -it asset-management-db psql -U asset_admin -d asset_management -c "SELECT ticket_number, subject, from_email, status, date FROM tickets ORDER BY date DESC LIMIT 10;"
```

## Next Steps

1. **Run the diagnostic script** to see current state
2. **Send a fresh test email** (don't open it in Gmail)
3. **Refresh tickets** in the web interface
4. **Check the logs** if issues persist

## Support

If you continue to have issues:
1. Run `diagnose_email_issue.py` and share the output
2. Check `docker logs asset-management-system` for errors
3. Verify you can access http://192.168.2.10:5000
4. Ensure you're logged in as admin/admin

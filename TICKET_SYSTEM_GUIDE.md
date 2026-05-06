# Ticket System - Quick Start Guide

## ✅ System Status

Your IT Asset Management System is **successfully deployed** on the server at **192.168.2.10:5000**

The ticket system is **working correctly** - it automatically converts emails sent to **tyson741161@gmail.com** into support tickets.

## 🎯 How to Use the Ticket System

### For End Users (Creating Tickets)

Simply send an email to: **tyson741161@gmail.com**

- The email subject becomes the ticket subject
- The email body becomes the ticket description
- The sender's email is recorded
- A ticket number is automatically assigned (starting from 1001)

### For Admins (Managing Tickets)

1. **Access the web interface**: http://192.168.2.10:5000
2. **Login**: admin / admin
3. **Click "Tickets" tab**
4. **View tickets**: All emails appear as tickets with status badges
5. **Auto-refresh**: New tickets appear automatically every 30 seconds
6. **Manual refresh**: Click "Refresh Tickets" button anytime

### Ticket Management Features

- **View Details**: Click "View" to see full ticket information
- **Reply**: Send email responses directly from the interface
- **Add Notes**: Add internal notes (not sent to customer)
- **Update Status**: Change status (Open → In Progress → Resolved → Closed)
- **Auto-closure Email**: When you close a ticket, an automatic email is sent to the customer

## 🔍 Troubleshooting: "My Email Didn't Become a Ticket"

### Most Common Reason

**The email was already marked as READ** - The system only fetches UNREAD emails to avoid duplicates.

### Solution 1: Send a Fresh Test Email

1. From any email account, send to: **tyson741161@gmail.com**
2. **Important**: Do NOT open this email in Gmail
3. Wait 30 seconds or click "Refresh Tickets" in the web interface
4. The ticket should appear

### Solution 2: Check What Happened (On Server)

SSH into your server and run the diagnostic:

```bash
cd ~/asset-management
docker exec -it asset-management-system python diagnose_email_issue.py
```

This shows:
- How many unread emails exist
- Recent emails (read and unread)
- Existing tickets in database
- Any error messages

### Solution 3: Re-process Existing Emails

If you want to convert emails that were already marked as read:

```bash
cd ~/asset-management
docker exec -it asset-management-system python mark_emails_unread.py
```

This will:
1. Show you the 5 most recent emails
2. Ask for confirmation
3. Mark them as UNREAD
4. Then you can refresh tickets in the web interface

### Solution 4: Test the Complete Flow

```bash
cd ~/asset-management
docker exec -it asset-management-system python test_ticket_creation.py
```

This simulates clicking "Refresh Tickets" and shows exactly what happens.

## 📊 Checking System Status

### View Application Logs

```bash
docker logs asset-management-system --tail 50
```

Look for:
- "Starting to fetch emails..."
- "Found X unread emails"
- "Creating ticket from email: [subject]"

### View All Containers

```bash
docker ps
```

Should show:
- `asset-management-system` (web app)
- `asset-management-db` (PostgreSQL)

### Check Recent Emails

```bash
docker exec -it asset-management-system python check_recent_emails.py
```

Shows the last 20 emails with their READ/UNREAD status.

## 🎬 Step-by-Step Test

### Test 1: Send and Verify

1. **Send test email** to tyson741161@gmail.com
   - Subject: "Test Ticket - [Your Name]"
   - Body: "Testing the ticket system"

2. **Don't open the email in Gmail!**

3. **Open web interface**: http://192.168.2.10:5000

4. **Login**: admin / admin

5. **Go to Tickets tab**

6. **Click "Refresh Tickets"**

7. **Verify**: Your email should appear as a new ticket

### Test 2: Reply to Ticket

1. **Click "View"** on any ticket

2. **Click "Reply to Ticket"**

3. **Type your response**

4. **Click "Send Reply"**

5. **Check**: The recipient should receive your email

### Test 3: Close Ticket

1. **Click "Update Status"** on any ticket

2. **Select "Closed"**

3. **Click "Update Status"**

4. **Check**: An automatic closure email is sent to the customer

## 🔧 Advanced Troubleshooting

### Check Database Directly

```bash
docker exec -it asset-management-db psql -U asset_admin -d asset_management
```

Then run:
```sql
-- See all tickets
SELECT ticket_number, subject, from_email, status, date 
FROM tickets 
ORDER BY date DESC 
LIMIT 10;

-- Count tickets
SELECT COUNT(*) FROM tickets;

-- Exit
\q
```

### Restart the Application

```bash
cd ~/asset-management
docker-compose restart asset-management
```

### View Full Logs

```bash
docker logs asset-management-system -f
```

(Press Ctrl+C to stop following logs)

### Check Email Configuration

```bash
docker exec -it asset-management-system python test_email_connection.py
```

## 📝 Important Notes

1. **Only UNREAD emails** are converted to tickets
2. **After processing**, emails are marked as READ to prevent duplicates
3. **Auto-refresh** only works when you're on the Tickets tab
4. **Ticket numbers** start from 1001 and increment automatically
5. **Email credentials** are already configured in the Docker container

## 🚀 Quick Commands Reference

```bash
# Check if system is running
docker ps

# View logs
docker logs asset-management-system --tail 50

# Run diagnostic
docker exec -it asset-management-system python diagnose_email_issue.py

# Check recent emails
docker exec -it asset-management-system python check_recent_emails.py

# Mark emails as unread (to reprocess)
docker exec -it asset-management-system python mark_emails_unread.py

# Test ticket creation
docker exec -it asset-management-system python test_ticket_creation.py

# Restart application
docker-compose restart asset-management

# Stop everything
docker-compose down

# Start everything
docker-compose up -d
```

## 📧 Email Configuration

- **IMAP Server**: imap.gmail.com
- **Email**: tyson741161@gmail.com
- **App Password**: sdxr csld bahs fpeg
- **SMTP Server**: smtp.gmail.com (for sending replies)

## 🎯 Next Steps

1. **Send a test email** to tyson741161@gmail.com (don't open it in Gmail)
2. **Access the web interface** at http://192.168.2.10:5000
3. **Login** with admin/admin
4. **Go to Tickets tab** and click "Refresh Tickets"
5. **Verify** your test email appears as a ticket

If you have any issues, run the diagnostic script:
```bash
docker exec -it asset-management-system python diagnose_email_issue.py
```

## ✅ Success Indicators

You'll know everything is working when:
- ✓ You can access http://192.168.2.10:5000
- ✓ You can login with admin/admin
- ✓ Emails sent to tyson741161@gmail.com appear as tickets
- ✓ Auto-refresh shows new tickets every 30 seconds
- ✓ You can reply to tickets and customers receive emails
- ✓ Closing tickets sends automatic closure emails

Your system is ready to use! 🎉

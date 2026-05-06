# Email Setup Instructions

To enable email functionality for the Request feature, you need to configure Gmail App Password.

## Steps to Set Up Gmail App Password:

1. **Enable 2-Factor Authentication on Gmail:**
   - Go to https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Create App Password:**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Name it "Asset Management System"
   - Click "Generate"
   - Copy the 16-character password

3. **Update server.py:**
   - Open `server.py`
   - Find the line: `app.config['MAIL_PASSWORD'] = ''`
   - Replace with: `app.config['MAIL_PASSWORD'] = 'your-16-char-app-password'`

4. **Install flask-mail:**
   ```bash
   pip install flask-mail
   ```

5. **Restart the server:**
   ```bash
   python server.py
   ```

## Alternative: Use Environment Variable (More Secure)

Instead of hardcoding the password, use an environment variable:

1. Create a `.env` file:
   ```
   MAIL_PASSWORD=your-16-char-app-password
   ```

2. Update server.py:
   ```python
   import os
   app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '')
   ```

## Testing

1. Login to the system
2. Click on "Request" tab
3. Fill in Subject and Description
4. Click "Submit Request"
5. Check yatrihikes@gmail.com for the email

## Troubleshooting

- **"Less secure app access"**: Gmail no longer supports this. Use App Password instead.
- **"Authentication failed"**: Make sure 2FA is enabled and you're using the App Password, not your regular password.
- **"Connection refused"**: Check if port 587 is open and not blocked by firewall.

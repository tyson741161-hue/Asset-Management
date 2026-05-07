from flask import Flask, render_template, request, jsonify, session
from flask_mail import Mail, Message
from imap_tools import MailBox, AND
import json
import os
from datetime import datetime
from models import db, Asset, Ticket, TicketReply, TicketNote, Request, EmailConfig

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Database configuration
database_url = os.environ.get('DATABASE_URL', 'postgresql://asset_admin:asset_secure_pass_2026@localhost:5432/asset_management')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Default email configuration (will be overridden by DB config)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_DEFAULT_SENDER'] = ''

mail = Mail(app)


# ── Helper: get active email config from DB ──────────────────────────────────
def get_email_config():
    """Return the active EmailConfig row, or None."""
    try:
        return EmailConfig.query.filter_by(is_active=True).first()
    except Exception:
        return None


def reconfigure_mail(cfg):
    """Apply an EmailConfig to Flask-Mail at runtime."""
    if not cfg:
        return
    app.config['MAIL_SERVER'] = cfg.smtp_server
    app.config['MAIL_PORT'] = cfg.smtp_port
    app.config['MAIL_USE_TLS'] = cfg.use_tls
    app.config['MAIL_USERNAME'] = cfg.email_address
    app.config['MAIL_PASSWORD'] = cfg.app_password
    app.config['MAIL_DEFAULT_SENDER'] = cfg.email_address
    # Re-init mail with new config
    mail.init_app(app)


# ── Fetch emails from configured mailbox ─────────────────────────────────────
def fetch_emails_as_tickets():
    print("Starting to fetch emails...")

    cfg = get_email_config()
    if not cfg:
        print("ERROR: No email configuration found! Configure mail in Settings.")
        return []

    try:
        new_tickets = []

        max_ticket = db.session.query(db.func.max(Ticket.ticket_number)).scalar()
        next_ticket_num = (max_ticket + 1) if max_ticket else 1001

        print(f"Connecting to {cfg.imap_server} as {cfg.email_address}...")

        with MailBox(cfg.imap_server).login(cfg.email_address, cfg.app_password) as mailbox:
            print("Successfully connected to mailbox")

            messages = list(mailbox.fetch(AND(seen=False), limit=50, reverse=True))
            print(f"Found {len(messages)} unread emails")

            for msg in messages:
                ticket_id = int(msg.date.timestamp() * 1000)

                existing_ticket = Ticket.query.filter_by(id=ticket_id).first()
                if existing_ticket:
                    print(f"Ticket {ticket_id} already exists, skipping")
                    mailbox.flag(msg.uid, ['\\Seen'], True)
                    continue

                print(f"Creating ticket from email: {msg.subject}")

                ticket = Ticket(
                    id=ticket_id,
                    ticket_number=next_ticket_num,
                    subject=msg.subject or '',
                    from_email=msg.from_,
                    body=msg.text or msg.html or '',
                    date=msg.date,
                    status='open',
                    priority='medium',
                )

                db.session.add(ticket)
                new_tickets.append(ticket)
                next_ticket_num += 1

                mailbox.flag(msg.uid, ['\\Seen'], True)
                print(f"Marked email as read: {msg.subject}")

        db.session.commit()
        print(f"Successfully created {len(new_tickets)} new tickets")
        return [t.to_dict() for t in new_tickets]

    except Exception as e:
        db.session.rollback()
        print(f"ERROR fetching emails: {str(e)}")
        import traceback
        traceback.print_exc()
        return []


# ══════════════════════════════════════════════════════════════════════════════
#  ROUTES
# ══════════════════════════════════════════════════════════════════════════════

@app.route('/')
def index():
    return render_template('index.html')


# ── Auth ─────────────────────────────────────────────────────────────────────

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username == 'admin' and password == 'admin':
        session['logged_in'] = True
        # Apply mail config on login
        cfg = get_email_config()
        if cfg:
            reconfigure_mail(cfg)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'})


@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})


@app.route('/api/verify-code', methods=['POST'])
def verify_code():
    data = request.json
    code = data.get('code')
    if code == '4181':
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


# ── Assets ───────────────────────────────────────────────────────────────────

@app.route('/api/assets', methods=['GET'])
def get_assets():
    if not session.get('logged_in'):
        return jsonify({'error': 'Not authenticated'}), 401

    try:
        assets = Asset.query.all()
        return jsonify([asset.to_dict() for asset in assets])
    except Exception as e:
        print(f"Error fetching assets: {str(e)}")
        return jsonify({'error': 'Failed to fetch assets'}), 500


@app.route('/api/assets', methods=['POST'])
def add_asset():
    if not session.get('logged_in'):
        return jsonify({'error': 'Not authenticated'}), 401

    try:
        data = request.json

        asset = Asset(
            id=int(datetime.now().timestamp() * 1000),
            type=data.get('type'),
            asset_id=data.get('assetId'),
            model=data.get('model'),
            status=data.get('status', 'available'),
            serial_number=data.get('serialNumber'),
            configuration=data.get('configuration'),
            office_location=data.get('officeLocation'),
            location=data.get('location'),
            year=int(data['year']) if data.get('year') and str(data['year']).isdigit() else None,
            current_condition=data.get('currentCondition'),
            current_user=data.get('currentUser'),
            last_user=data.get('lastUser'),
            quantity=data.get('quantity'),
            mouse_type=data.get('mouseType'),
            firewall_name=data.get('firewallName'),
            purchase_year=int(data['purchaseYear']) if data.get('purchaseYear') else None,
            last_firmware_update=datetime.fromisoformat(data['lastFirmwareUpdate']).date() if data.get('lastFirmwareUpdate') else None,
            ram_name=data.get('ramName'),
            ram_size=data.get('ramSize'),
            ram_ddr=data.get('ramDDR'),
            ram_frequency=data.get('ramFrequency')
        )

        # Handle laptop accessories
        if data.get('accessories'):
            accessories = data['accessories']
            asset.mouse_name = accessories.get('mouse')
            asset.headphone_name = accessories.get('headphone')
            asset.charger_name = accessories.get('charger')
            asset.monitor_name = accessories.get('monitor')
        else:
            asset.mouse_name = data.get('mouseName')
            asset.headphone_name = data.get('headphoneName')
            asset.charger_name = data.get('chargerName')
            asset.monitor_name = data.get('monitorName')

        db.session.add(asset)
        db.session.commit()

        return jsonify({'success': True, 'asset': asset.to_dict()})

    except Exception as e:
        db.session.rollback()
        print(f"Error adding asset: {str(e)}")
        return jsonify({'error': 'Failed to add asset'}), 500


@app.route('/api/assets/<int:asset_id>', methods=['PUT'])
def update_asset(asset_id):
    if not session.get('logged_in'):
        return jsonify({'error': 'Not authenticated'}), 401

    try:
        asset = Asset.query.get(asset_id)
        if not asset:
            return jsonify({'error': 'Asset not found'}), 404

        data = request.json

        if 'type' in data:
            asset.type = data['type']
        if 'assetId' in data:
            asset.asset_id = data['assetId']
        if 'model' in data:
            asset.model = data['model']
        if 'status' in data:
            asset.status = data['status']
        if 'serialNumber' in data:
            asset.serial_number = data['serialNumber']
        if 'configuration' in data:
            asset.configuration = data['configuration']
        if 'officeLocation' in data:
            asset.office_location = data['officeLocation']
        if 'location' in data:
            asset.location = data['location']
        if 'year' in data:
            asset.year = int(data['year']) if data['year'] and str(data['year']).isdigit() else None
        if 'currentCondition' in data:
            asset.current_condition = data['currentCondition']
        if 'currentUser' in data:
            asset.current_user = data['currentUser']
        if 'lastUser' in data:
            asset.last_user = data['lastUser']
        if 'quantity' in data:
            asset.quantity = data['quantity']
        if 'mouseType' in data:
            asset.mouse_type = data['mouseType']
        if 'firewallName' in data:
            asset.firewall_name = data['firewallName']
        if 'purchaseYear' in data:
            asset.purchase_year = int(data['purchaseYear']) if data['purchaseYear'] else None
        if 'lastFirmwareUpdate' in data:
            asset.last_firmware_update = datetime.fromisoformat(data['lastFirmwareUpdate']).date() if data['lastFirmwareUpdate'] else None
        if 'ramName' in data:
            asset.ram_name = data['ramName']
        if 'ramSize' in data:
            asset.ram_size = data['ramSize']
        if 'ramDDR' in data:
            asset.ram_ddr = data['ramDDR']
        if 'ramFrequency' in data:
            asset.ram_frequency = data['ramFrequency']

        # Handle laptop accessories
        if 'accessories' in data:
            accessories = data['accessories']
            asset.mouse_name = accessories.get('mouse')
            asset.headphone_name = accessories.get('headphone')
            asset.charger_name = accessories.get('charger')
            asset.monitor_name = accessories.get('monitor')
        else:
            if 'mouseName' in data:
                asset.mouse_name = data['mouseName']
            if 'headphoneName' in data:
                asset.headphone_name = data['headphoneName']
            if 'chargerName' in data:
                asset.charger_name = data['chargerName']
            if 'monitorName' in data:
                asset.monitor_name = data['monitorName']

        db.session.commit()

        return jsonify({'success': True, 'asset': asset.to_dict()})

    except Exception as e:
        db.session.rollback()
        print(f"Error updating asset: {str(e)}")
        return jsonify({'error': 'Failed to update asset'}), 500


@app.route('/api/assets/<int:asset_id>', methods=['DELETE'])
def delete_asset(asset_id):
    if not session.get('logged_in'):
        return jsonify({'error': 'Not authenticated'}), 401

    try:
        asset = Asset.query.get(asset_id)
        if not asset:
            return jsonify({'error': 'Asset not found'}), 404

        db.session.delete(asset)
        db.session.commit()

        return jsonify({'success': True})

    except Exception as e:
        db.session.rollback()
        print(f"Error deleting asset: {str(e)}")
        return jsonify({'error': 'Failed to delete asset'}), 500


# ── Requests ─────────────────────────────────────────────────────────────────

@app.route('/api/requests', methods=['GET'])
def get_requests():
    if not session.get('logged_in'):
        return jsonify({'error': 'Not authenticated'}), 401

    try:
        requests_list = Request.query.order_by(Request.date.desc()).all()
        return jsonify([req.to_dict() for req in requests_list])
    except Exception as e:
        print(f"Error fetching requests: {str(e)}")
        return jsonify({'error': 'Failed to fetch requests'}), 500


@app.route('/api/send-request', methods=['POST'])
def send_request():
    if not session.get('logged_in'):
        return jsonify({'error': 'Not authenticated'}), 401

    data = request.json
    email = data.get('email')
    subject = data.get('subject')
    description = data.get('description')

    try:
        # Reconfigure mail before sending
        cfg = get_email_config()
        if cfg:
            reconfigure_mail(cfg)

        msg = Message(
            subject=f"Asset Request: {subject}",
            recipients=[email],
            body=f"""
Asset Management System - New Request

Subject: {subject}

Description:
{description}

---
This request was submitted from the Asset Management System.
            """
        )

        mail.send(msg)

        new_request = Request(
            id=int(datetime.now().timestamp() * 1000),
            email=email,
            subject=subject,
            description=description,
            date=datetime.now()
        )

        db.session.add(new_request)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Request submitted successfully!'
        })
    except Exception as e:
        db.session.rollback()
        print(f"Error sending email: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to send request. Please check email configuration.'
        }), 500


# ── Tickets ──────────────────────────────────────────────────────────────────

@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    if not session.get('logged_in'):
        return jsonify({'error': 'Not authenticated'}), 401

    try:
        tickets = Ticket.query.order_by(Ticket.date.desc()).all()
        return jsonify([ticket.to_dict() for ticket in tickets])
    except Exception as e:
        print(f"Error fetching tickets: {str(e)}")
        return jsonify({'error': 'Failed to fetch tickets'}), 500


@app.route('/api/tickets/stats', methods=['GET'])
def get_ticket_stats():
    """Return counts for each ticket status for the dashboard cards."""
    if not session.get('logged_in'):
        return jsonify({'error': 'Not authenticated'}), 401

    try:
        total = Ticket.query.count()
        open_count = Ticket.query.filter_by(status='open').count()
        in_progress = Ticket.query.filter_by(status='in-progress').count()
        resolved = Ticket.query.filter_by(status='resolved').count()
        closed = Ticket.query.filter_by(status='closed').count()
        urgent = Ticket.query.filter_by(priority='urgent').count()
        high = Ticket.query.filter_by(priority='high').count()

        return jsonify({
            'total': total,
            'open': open_count,
            'in_progress': in_progress,
            'resolved': resolved,
            'closed': closed,
            'urgent': urgent,
            'high': high,
        })
    except Exception as e:
        print(f"Error fetching ticket stats: {str(e)}")
        return jsonify({'error': 'Failed to fetch stats'}), 500


@app.route('/api/tickets/create', methods=['POST'])
def create_ticket():
    """Manually create a ticket (not from email)."""
    if not session.get('logged_in'):
        return jsonify({'error': 'Not authenticated'}), 401

    try:
        data = request.json
        max_ticket = db.session.query(db.func.max(Ticket.ticket_number)).scalar()
        next_num = (max_ticket + 1) if max_ticket else 1001

        ticket = Ticket(
            id=int(datetime.now().timestamp() * 1000),
            ticket_number=next_num,
            subject=data.get('subject', '(No subject)'),
            from_email=data.get('from_email', 'manual@local'),
            body=data.get('body', ''),
            status='open',
            priority=data.get('priority', 'medium'),
            category=data.get('category', ''),
            date=datetime.now(),
        )
        db.session.add(ticket)
        db.session.commit()
        return jsonify({'success': True, 'ticket': ticket.to_dict()})
    except Exception as e:
        db.session.rollback()
        print(f"Error creating ticket: {str(e)}")
        return jsonify({'error': 'Failed to create ticket'}), 500


@app.route('/api/tickets/refresh', methods=['POST'])
def refresh_tickets():
    if not session.get('logged_in'):
        return jsonify({'error': 'Not authenticated'}), 401

    try:
        new_tickets = fetch_emails_as_tickets()
        return jsonify({'success': True, 'new_tickets': len(new_tickets)})
    except Exception as e:
        print(f"Error refreshing tickets: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/tickets/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    """Update ticket properties (priority, assignee, category, status)."""
    if not session.get('logged_in'):
        return jsonify({'error': 'Not authenticated'}), 401

    try:
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return jsonify({'error': 'Ticket not found'}), 404

        data = request.json

        if 'priority' in data:
            ticket.priority = data['priority']
        if 'assigned_to' in data:
            ticket.assigned_to = data['assigned_to']
        if 'category' in data:
            ticket.category = data['category']
        if 'status' in data:
            old_status = ticket.status
            ticket.status = data['status']

            # Send automatic email when ticket is closed
            if data['status'] == 'closed' and old_status != 'closed':
                try:
                    cfg = get_email_config()
                    if cfg:
                        reconfigure_mail(cfg)

                    closure_message = f"""Dear Customer,

Your support ticket has been closed.

Ticket Subject: {ticket.subject}
Status: Closed

Thank you for reaching out to us. If you have any further questions or concerns, please don't hesitate to contact us again.

Best regards,
IT Asset Management Support Team
"""

                    msg = Message(
                        subject=f"Ticket Closed: {ticket.subject}",
                        recipients=[ticket.from_email],
                        body=closure_message
                    )

                    mail.send(msg)
                    print(f"Closure email sent to {ticket.from_email}")

                    reply = TicketReply(
                        ticket_id=ticket.id,
                        message=closure_message,
                        to_email=ticket.from_email,
                        type='auto-closure',
                        date=datetime.now()
                    )
                    db.session.add(reply)

                except Exception as e:
                    print(f"Error sending closure email: {str(e)}")

        db.session.commit()
        return jsonify({'success': True, 'ticket': ticket.to_dict()})

    except Exception as e:
        db.session.rollback()
        print(f"Error updating ticket: {str(e)}")
        return jsonify({'error': 'Failed to update ticket'}), 500


@app.route('/api/tickets/<int:ticket_id>/status', methods=['PUT'])
def update_ticket_status(ticket_id):
    if not session.get('logged_in'):
        return jsonify({'error': 'Not authenticated'}), 401

    try:
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return jsonify({'error': 'Ticket not found'}), 404

        data = request.json
        new_status = data.get('status')

        old_status = ticket.status
        ticket.status = new_status

        if new_status == 'closed' and old_status != 'closed':
            try:
                cfg = get_email_config()
                if cfg:
                    reconfigure_mail(cfg)

                closure_message = f"""Dear Customer,

Your support ticket has been closed.

Ticket Subject: {ticket.subject}
Status: Closed

Thank you for reaching out to us. If you have any further questions or concerns, please don't hesitate to contact us again.

Best regards,
IT Asset Management Support Team
"""

                msg = Message(
                    subject=f"Ticket Closed: {ticket.subject}",
                    recipients=[ticket.from_email],
                    body=closure_message
                )

                mail.send(msg)
                print(f"Closure email sent to {ticket.from_email}")

                reply = TicketReply(
                    ticket_id=ticket.id,
                    message=closure_message,
                    to_email=ticket.from_email,
                    type='auto-closure',
                    date=datetime.now()
                )
                db.session.add(reply)

            except Exception as e:
                print(f"Error sending closure email: {str(e)}")

        db.session.commit()
        return jsonify({'success': True})

    except Exception as e:
        db.session.rollback()
        print(f"Error updating ticket status: {str(e)}")
        return jsonify({'error': 'Failed to update ticket status'}), 500


@app.route('/api/tickets/reply', methods=['POST'])
def reply_to_ticket():
    if not session.get('logged_in'):
        return jsonify({'error': 'Not authenticated'}), 401

    data = request.json
    ticket_id = data.get('ticket_id')
    to_email = data.get('to')
    subject = data.get('subject')
    message = data.get('message')

    try:
        cfg = get_email_config()
        if cfg:
            reconfigure_mail(cfg)

        msg = Message(
            subject=subject,
            recipients=[to_email],
            body=message
        )

        mail.send(msg)

        ticket = Ticket.query.get(ticket_id)
        if ticket:
            reply = TicketReply(
                ticket_id=ticket.id,
                message=message,
                to_email=to_email,
                type='manual',
                date=datetime.now()
            )
            db.session.add(reply)
            db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Reply sent successfully!'
        })
    except Exception as e:
        db.session.rollback()
        print(f"Error sending reply: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to send reply. Please check email configuration.'
        }), 500


@app.route('/api/tickets/<int:ticket_id>/note', methods=['POST'])
def add_ticket_note(ticket_id):
    if not session.get('logged_in'):
        return jsonify({'error': 'Not authenticated'}), 401

    try:
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return jsonify({'error': 'Ticket not found'}), 404

        data = request.json
        note_text = data.get('note')

        note = TicketNote(
            ticket_id=ticket.id,
            text=note_text,
            date=datetime.now()
        )

        db.session.add(note)
        db.session.commit()

        return jsonify({'success': True})

    except Exception as e:
        db.session.rollback()
        print(f"Error adding note: {str(e)}")
        return jsonify({'error': 'Failed to add note'}), 500


# ── Email Settings ───────────────────────────────────────────────────────────

@app.route('/api/settings/email', methods=['GET'])
def get_email_settings():
    if not session.get('logged_in'):
        return jsonify({'error': 'Not authenticated'}), 401

    cfg = get_email_config()
    if cfg:
        return jsonify({'configured': True, 'config': cfg.to_dict(mask_password=True)})
    else:
        return jsonify({'configured': False, 'config': None})


@app.route('/api/settings/email', methods=['POST'])
def save_email_settings():
    if not session.get('logged_in'):
        return jsonify({'error': 'Not authenticated'}), 401

    data = request.json

    try:
        # Deactivate all existing configs
        EmailConfig.query.update({'is_active': False})

        cfg = EmailConfig(
            email_address=data['email_address'],
            app_password=data['app_password'],
            smtp_server=data.get('smtp_server', 'smtp.gmail.com'),
            smtp_port=data.get('smtp_port', 587),
            imap_server=data.get('imap_server', 'imap.gmail.com'),
            use_tls=data.get('use_tls', True),
            is_active=True,
        )

        db.session.add(cfg)
        db.session.commit()

        # Apply immediately
        reconfigure_mail(cfg)

        return jsonify({'success': True, 'message': 'Email configuration saved!'})

    except Exception as e:
        db.session.rollback()
        print(f"Error saving email config: {str(e)}")
        return jsonify({'success': False, 'message': f'Failed to save: {str(e)}'}), 500


@app.route('/api/settings/email/test', methods=['POST'])
def test_email_settings():
    if not session.get('logged_in'):
        return jsonify({'error': 'Not authenticated'}), 401

    data = request.json
    email_addr = data.get('email_address', '')
    password = data.get('app_password', '')
    imap_srv = data.get('imap_server', 'imap.gmail.com')
    smtp_srv = data.get('smtp_server', 'smtp.gmail.com')

    results = {'imap': False, 'smtp': False, 'imap_error': '', 'smtp_error': ''}

    # Test IMAP
    try:
        with MailBox(imap_srv).login(email_addr, password) as mb:
            results['imap'] = True
    except Exception as e:
        results['imap_error'] = str(e)

    # Test SMTP
    try:
        import smtplib
        server = smtplib.SMTP(smtp_srv, data.get('smtp_port', 587))
        server.ehlo()
        if data.get('use_tls', True):
            server.starttls()
        server.login(email_addr, password)
        server.quit()
        results['smtp'] = True
    except Exception as e:
        results['smtp_error'] = str(e)

    success = results['imap'] and results['smtp']
    return jsonify({'success': success, 'results': results})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

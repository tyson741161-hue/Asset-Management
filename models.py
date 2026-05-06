"""
Database models for IT Asset Management System
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Asset(db.Model):
    __tablename__ = 'assets'
    
    id = db.Column(db.BigInteger, primary_key=True)
    asset_id = db.Column(db.String(100))
    type = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(200))
    status = db.Column(db.String(50), default='available')
    serial_number = db.Column(db.String(100))
    configuration = db.Column(db.Text)
    office_location = db.Column(db.String(100))
    location = db.Column(db.String(100))  # For accessories
    year = db.Column(db.Integer)
    current_condition = db.Column(db.String(100))
    current_user = db.Column('current_user_name', db.String(200))
    last_user = db.Column('last_user_name', db.String(200))
    
    # Mouse specific
    quantity = db.Column(db.Integer)
    mouse_type = db.Column(db.String(50))
    
    # Firewall specific
    firewall_name = db.Column(db.String(200))
    purchase_year = db.Column(db.Integer)
    last_firmware_update = db.Column(db.Date)
    
    # RAM specific
    ram_name = db.Column(db.String(200))
    ram_size = db.Column(db.String(50))
    ram_ddr = db.Column(db.String(20))
    ram_frequency = db.Column(db.String(50))
    
    # Laptop accessories
    mouse_name = db.Column(db.String(200))
    headphone_name = db.Column(db.String(200))
    charger_name = db.Column(db.String(200))
    monitor_name = db.Column(db.String(200))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert asset to dictionary"""
        data = {
            'id': self.id,
            'type': self.type,
            'status': self.status,
        }
        
        # Add non-null fields
        if self.asset_id:
            data['assetId'] = self.asset_id
        if self.model:
            data['model'] = self.model
        if self.serial_number:
            data['serialNumber'] = self.serial_number
        if self.configuration:
            data['configuration'] = self.configuration
        if self.office_location:
            data['officeLocation'] = self.office_location
        if self.location:
            data['location'] = self.location
        if self.year:
            data['year'] = self.year
        if self.current_condition:
            data['currentCondition'] = self.current_condition
        if self.current_user:
            data['currentUser'] = self.current_user
        if self.last_user:
            data['lastUser'] = self.last_user
        if self.quantity:
            data['quantity'] = self.quantity
        if self.mouse_type:
            data['mouseType'] = self.mouse_type
        if self.firewall_name:
            data['firewallName'] = self.firewall_name
        if self.purchase_year:
            data['purchaseYear'] = self.purchase_year
        if self.last_firmware_update:
            data['lastFirmwareUpdate'] = self.last_firmware_update.isoformat()
        if self.ram_name:
            data['ramName'] = self.ram_name
        if self.ram_size:
            data['ramSize'] = self.ram_size
        if self.ram_ddr:
            data['ramDDR'] = self.ram_ddr
        if self.ram_frequency:
            data['ramFrequency'] = self.ram_frequency
        if self.mouse_name:
            data['mouseName'] = self.mouse_name
        if self.headphone_name:
            data['headphoneName'] = self.headphone_name
        if self.charger_name:
            data['chargerName'] = self.charger_name
        if self.monitor_name:
            data['monitorName'] = self.monitor_name
            
        return data


class Ticket(db.Model):
    __tablename__ = 'tickets'
    
    id = db.Column(db.BigInteger, primary_key=True)
    ticket_number = db.Column(db.Integer, unique=True, nullable=False)
    subject = db.Column(db.String(500), nullable=False)
    from_email = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text)
    status = db.Column(db.String(50), default='open')
    date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    replies = db.relationship('TicketReply', backref='ticket', lazy=True, cascade='all, delete-orphan')
    notes = db.relationship('TicketNote', backref='ticket', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert ticket to dictionary"""
        return {
            'id': self.id,
            'ticket_number': self.ticket_number,
            'subject': self.subject,
            'from_email': self.from_email,
            'body': self.body,
            'status': self.status,
            'date': self.date.isoformat(),
            'replies': [reply.to_dict() for reply in self.replies],
            'notes': [note.to_dict() for note in self.notes]
        }


class TicketReply(db.Model):
    __tablename__ = 'ticket_replies'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.BigInteger, db.ForeignKey('tickets.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    to_email = db.Column(db.String(200))
    type = db.Column(db.String(50))  # 'manual' or 'auto-closure'
    date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert reply to dictionary"""
        return {
            'message': self.message,
            'to': self.to_email,
            'type': self.type,
            'date': self.date.isoformat()
        }


class TicketNote(db.Model):
    __tablename__ = 'ticket_notes'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.BigInteger, db.ForeignKey('tickets.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert note to dictionary"""
        return {
            'text': self.text,
            'date': self.date.isoformat()
        }


class Request(db.Model):
    __tablename__ = 'requests'
    
    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert request to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'subject': self.subject,
            'description': self.description,
            'date': self.date.isoformat()
        }

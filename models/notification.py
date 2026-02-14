"""
Notification models for contact and consultation requests
"""
from datetime import datetime
from models import db
import json


class ContactMessage(db.Model):
    """Store contact form submissions"""
    __tablename__ = 'contact_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), default='')
    company = db.Column(db.String(150), default='')
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    newsletter = db.Column(db.Boolean, default=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'company': self.company,
            'subject': self.subject,
            'message': self.message,
            'newsletter': self.newsletter,
            'isRead': self.is_read,
            'createdAt': self.created_at.isoformat(),
            'updatedAt': self.updated_at.isoformat()
        }


class ConsultationRequest(db.Model):
    """Store consultation form submissions"""
    __tablename__ = 'consultation_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    company = db.Column(db.String(150), default='')
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    preferred_date = db.Column(db.String(20), nullable=False)
    preferred_time = db.Column(db.String(20), nullable=False)
    newsletter = db.Column(db.Boolean, default=False)
    cart_items = db.Column(db.Text)  # Store as JSON string
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_cart_items(self, items):
        """Store cart items as JSON"""
        self.cart_items = json.dumps(items)
    
    def get_cart_items(self):
        """Retrieve cart items from JSON"""
        if self.cart_items:
            return json.loads(self.cart_items)
        return []
    
    def to_dict(self):
        return {
            'id': self.id,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'company': self.company,
            'subject': self.subject,
            'message': self.message,
            'preferredDate': self.preferred_date,
            'preferredTime': self.preferred_time,
            'newsletter': self.newsletter,
            'cartItems': self.get_cart_items(),
            'isRead': self.is_read,
            'createdAt': self.created_at.isoformat(),
            'updatedAt': self.updated_at.isoformat()
        }

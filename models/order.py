"""
Order and OrderItem models
"""
from datetime import datetime
from models import db


class Order(db.Model):
    """Order model"""
    
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # User information
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Shipping information
    shipping_first_name = db.Column(db.String(50), nullable=False)
    shipping_last_name = db.Column(db.String(50), nullable=False)
    shipping_email = db.Column(db.String(120), nullable=False)
    shipping_phone = db.Column(db.String(20))
    shipping_company = db.Column(db.String(100))
    shipping_address_line1 = db.Column(db.String(200), nullable=False)
    shipping_address_line2 = db.Column(db.String(200))
    shipping_city = db.Column(db.String(100), nullable=False)
    shipping_state = db.Column(db.String(100), nullable=False)
    shipping_postal_code = db.Column(db.String(20), nullable=False)
    shipping_country = db.Column(db.String(100), nullable=False)
    
    # Billing information (can be same as shipping)
    billing_first_name = db.Column(db.String(50))
    billing_last_name = db.Column(db.String(50))
    billing_email = db.Column(db.String(120))
    billing_phone = db.Column(db.String(20))
    billing_company = db.Column(db.String(100))
    billing_address_line1 = db.Column(db.String(200))
    billing_address_line2 = db.Column(db.String(200))
    billing_city = db.Column(db.String(100))
    billing_state = db.Column(db.String(100))
    billing_postal_code = db.Column(db.String(20))
    billing_country = db.Column(db.String(100))
    
    # Order totals
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    tax_amount = db.Column(db.Numeric(10, 2), default=0)
    shipping_cost = db.Column(db.Numeric(10, 2), default=0)
    discount_amount = db.Column(db.Numeric(10, 2), default=0)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Payment information
    payment_method = db.Column(db.String(50))  # credit_card, paypal, bank_transfer
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, failed, refunded
    payment_transaction_id = db.Column(db.String(200))
    payment_date = db.Column(db.DateTime)
    
    # Order status
    status = db.Column(db.String(20), default='pending')  # pending, processing, shipped, delivered, cancelled
    
    # Additional information
    customer_notes = db.Column(db.Text)
    admin_notes = db.Column(db.Text)
    tracking_number = db.Column(db.String(100))
    shipping_carrier = db.Column(db.String(100))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    shipped_at = db.Column(db.DateTime)
    delivered_at = db.Column(db.DateTime)
    cancelled_at = db.Column(db.DateTime)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.order_number}>'
    
    @property
    def item_count(self):
        """Get total number of items in order"""
        return sum(item.quantity for item in self.items)
    
    @property
    def shipping_full_name(self):
        """Get full shipping name"""
        return f"{self.shipping_first_name} {self.shipping_last_name}"
    
    @property
    def billing_full_name(self):
        """Get full billing name"""
        if self.billing_first_name and self.billing_last_name:
            return f"{self.billing_first_name} {self.billing_last_name}"
        return self.shipping_full_name
    
    @property
    def shipping_address(self):
        """Get formatted shipping address"""
        address = self.shipping_address_line1
        if self.shipping_address_line2:
            address += f", {self.shipping_address_line2}"
        address += f", {self.shipping_city}, {self.shipping_state} {self.shipping_postal_code}"
        address += f", {self.shipping_country}"
        return address
    
    def to_dict(self, include_items=False):
        """Convert order to dictionary"""
        data = {
            'id': self.id,
            'order_number': self.order_number,
            'user_id': self.user_id,
            'status': self.status,
            'payment_status': self.payment_status,
            'payment_method': self.payment_method,
            'subtotal': float(self.subtotal),
            'tax_amount': float(self.tax_amount),
            'shipping_cost': float(self.shipping_cost),
            'discount_amount': float(self.discount_amount),
            'total_amount': float(self.total_amount),
            'item_count': self.item_count,
            'shipping_address': self.shipping_address,
            'tracking_number': self.tracking_number,
            'shipping_carrier': self.shipping_carrier,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'shipped_at': self.shipped_at.isoformat() if self.shipped_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None
        }
        
        if include_items:
            data['items'] = [item.to_dict() for item in self.items.all()]
        
        return data
    
    @staticmethod
    def generate_order_number():
        """Generate a unique order number"""
        import random
        import string
        timestamp = datetime.utcnow().strftime('%Y%m%d')
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"ORD-{timestamp}-{random_str}"


class OrderItem(db.Model):
    """Order item model"""
    
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    # Product snapshot (in case product details change)
    product_name = db.Column(db.String(200), nullable=False)
    product_sku = db.Column(db.String(100))
    product_image = db.Column(db.String(500))
    
    # Pricing
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Additional information
    customization_notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<OrderItem {self.id} - {self.product_name}>'
    
    def to_dict(self):
        """Convert order item to dictionary"""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'product_sku': self.product_sku,
            'product_image': self.product_image,
            'unit_price': float(self.unit_price),
            'quantity': self.quantity,
            'subtotal': float(self.subtotal),
            'customization_notes': self.customization_notes
        }
"""
Wishlist model for saved products
"""
from datetime import datetime
from models import db


class Wishlist(db.Model):
    """Wishlist model for users to save products"""
    
    __tablename__ = 'wishlist'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    # Metadata
    notes = db.Column(db.Text)  # User notes about the product
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Unique constraint to prevent duplicate entries
    __table_args__ = (
        db.UniqueConstraint('user_id', 'product_id', name='unique_user_product'),
    )
    
    def __repr__(self):
        return f'<Wishlist User:{self.user_id} Product:{self.product_id}>'
    
    def to_dict(self):
        """Convert wishlist item to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'product': self.product.to_dict() if self.product else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
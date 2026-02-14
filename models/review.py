"""
Review model for product reviews
"""
from datetime import datetime
from models import db


class Review(db.Model):
    """Product review model"""
    
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Relationships
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Review content
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    title = db.Column(db.String(200))
    comment = db.Column(db.Text, nullable=False)
    
    # Review metadata
    is_verified_purchase = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)
    helpful_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    approved_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Review {self.id} for Product {self.product_id}>'
    
    def to_dict(self):
        """Convert review to dictionary"""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'user_id': self.user_id,
            'user_name': self.user.full_name if self.user else 'Anonymous',
            'rating': self.rating,
            'title': self.title,
            'comment': self.comment,
            'is_verified_purchase': self.is_verified_purchase,
            'helpful_count': self.helpful_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
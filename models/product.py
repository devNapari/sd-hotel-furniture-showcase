"""
Product and Category models
"""
from datetime import datetime
from models import db


class Category(db.Model):
    """Product category model"""
    
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    is_active = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy='dynamic')
    subcategories = db.relationship('Category', backref=db.backref('parent', remote_side=[id]))
    
    def __repr__(self):
        return f'<Category {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'image_url': self.image_url,
            'parent_id': self.parent_id,
            'is_active': self.is_active
        }


class Product(db.Model):
    """Product model"""
    
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic information
    name = db.Column(db.String(200), nullable=False, index=True)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    sku = db.Column(db.String(100), unique=True, index=True)
    description = db.Column(db.Text)
    short_description = db.Column(db.String(500))
    
    # Pricing
    price = db.Column(db.Numeric(10, 2), nullable=False)
    compare_at_price = db.Column(db.Numeric(10, 2))  # Original price for discounts
    cost_price = db.Column(db.Numeric(10, 2))  # Cost for profit calculation
    
    # Inventory
    stock_quantity = db.Column(db.Integer, default=0)
    low_stock_threshold = db.Column(db.Integer, default=10)
    track_inventory = db.Column(db.Boolean, default=True)
    allow_backorder = db.Column(db.Boolean, default=False)
    
    # Product details
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    brand = db.Column(db.String(100))
    material = db.Column(db.String(200))
    color = db.Column(db.String(100))
    dimensions = db.Column(db.String(200))  # e.g., "72x36x30 inches"
    weight = db.Column(db.Numeric(10, 2))  # in pounds or kg
    
    # Features and specifications
    features = db.Column(db.JSON)  # List of features
    specifications = db.Column(db.JSON)  # Dict of specifications
    
    # SEO
    meta_title = db.Column(db.String(200))
    meta_description = db.Column(db.String(500))
    meta_keywords = db.Column(db.String(500))
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    is_new = db.Column(db.Boolean, default=False)
    is_on_sale = db.Column(db.Boolean, default=False)
    
    # Statistics
    view_count = db.Column(db.Integer, default=0)
    purchase_count = db.Column(db.Integer, default=0)
    average_rating = db.Column(db.Numeric(3, 2), default=0.0)
    review_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime)
    
    # Relationships
    images = db.relationship('ProductImage', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic')
    wishlist_items = db.relationship('Wishlist', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    @property
    def in_stock(self):
        """Check if product is in stock"""
        if not self.track_inventory:
            return True
        return self.stock_quantity > 0 or self.allow_backorder
    
    @property
    def is_low_stock(self):
        """Check if product is low on stock"""
        if not self.track_inventory:
            return False
        return 0 < self.stock_quantity <= self.low_stock_threshold
    
    @property
    def discount_percentage(self):
        """Calculate discount percentage"""
        if self.compare_at_price and self.compare_at_price > self.price:
            return int(((self.compare_at_price - self.price) / self.compare_at_price) * 100)
        return 0
    
    @property
    def main_image(self):
        """Get the main product image from ProductImage table (uploaded images only)

        Returns:
            str or None: Path to primary image, or None if no uploaded images
        """
        # Check ProductImage table for primary image
        image = self.images.filter_by(is_primary=True).first()
        if image:
            return image.image_url

        # Fall back to first image if no primary
        image = self.images.first()
        if image:
            return image.image_url

        # Return None if no uploaded images
        return None
    
    def to_dict(self, include_images=False, include_reviews=False):
        """Convert product to dictionary with image priority system"""
        data = {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'sku': self.sku,
            'description': self.description,
            'short_description': self.short_description,
            'price': float(self.price),
            'compare_at_price': float(self.compare_at_price) if self.compare_at_price else None,
            'category': self.category.to_dict() if self.category else None,
            'brand': self.brand,
            'material': self.material,
            'color': self.color,
            'dimensions': self.dimensions,
            'weight': float(self.weight) if self.weight else None,
            'features': self.features,
            'specifications': self.specifications,
            'in_stock': self.in_stock,
            'is_low_stock': self.is_low_stock,
            'stock_quantity': self.stock_quantity if self.track_inventory else None,
            'is_featured': self.is_featured,
            'is_new': self.is_new,
            'is_on_sale': self.is_on_sale,
            'discount_percentage': self.discount_percentage,
            'average_rating': float(self.average_rating),
            'review_count': self.review_count,
            'main_image': self.main_image,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_images:
            data['images'] = [img.to_dict() for img in self.images.all()]
        
        if include_reviews:
            data['reviews'] = [review.to_dict() for review in self.reviews.limit(5).all()]
        
        return data
    
    def update_rating(self):
        """Update average rating and review count"""
        reviews = self.reviews.filter_by(is_approved=True).all()
        if reviews:
            self.review_count = len(reviews)
            self.average_rating = sum(r.rating for r in reviews) / len(reviews)
        else:
            self.review_count = 0
            self.average_rating = 0.0
        db.session.commit()


class ProductImage(db.Model):
    """Product image model"""
    
    __tablename__ = 'product_images'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    alt_text = db.Column(db.String(200))
    is_primary = db.Column(db.Boolean, default=False)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ProductImage {self.id} for Product {self.product_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'image_url': self.image_url,
            'alt_text': self.alt_text,
            'is_primary': self.is_primary,
            'display_order': self.display_order
        }
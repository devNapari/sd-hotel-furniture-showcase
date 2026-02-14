"""
Database models for SD Hotel Furniture application
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from datetime import datetime

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()

# Import all models
from models.user import User
from models.product import Product, Category, ProductImage
from models.order import Order, OrderItem
from models.review import Review
from models.wishlist import Wishlist
from models.notification import ContactMessage, ConsultationRequest

__all__ = [
    'db',
    'bcrypt',
    'User',
    'Product',
    'Category',
    'ProductImage',
    'Order',
    'OrderItem',
    'Review',
    'Wishlist',
    'ContactMessage',
    'ConsultationRequest'

]
"""
SD Hotel Furniture Showcase - Flask Application with Database Integration
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from flask_mail import Mail
from datetime import datetime

# Import configuration
from config import config

# Import database and models
from models import db, bcrypt
from models.user import User
from models.product import Product, Category, ProductImage
from models.order import Order, OrderItem
from models.review import Review
from models.wishlist import Wishlist
from models.blog import BlogPost, BlogCategory, BlogComment


def create_app(config_name=None):
    """Application factory pattern"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate = Migrate(app, db)
    
    # Initialize Flask-Mail
    mail = Mail(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.api import api_bp, init_mail
    from routes.blog import blog_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(blog_bp, url_prefix='/blog')
    
    # Initialize mail in API routes
    init_mail(mail)
    
    # Initialize Flask-Admin
    from admin import init_admin
    init_admin(app)
    
    # Context processor to make current_user available in all templates
    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)
    
    return app


# Create app instance
app = create_app()


# ============================================================================
# MAIN ROUTES
# ============================================================================

@app.route('/')
def index():
    """Render the main homepage"""
    return render_template('index.html')


@app.route('/products')
def products():
    """Render the products page"""
    return render_template('products.html')


@app.route('/shop')
def shop():
    """Render the shop page"""
    return render_template('shop.html')


@app.route('/projects')
def projects():
    """Render the projects page"""
    return render_template('projects.html')


@app.route('/about')
def about():
    """Render the about page"""
    return render_template('about.html')


@app.route('/contact')
def contact():
    """Render the contact page"""
    return render_template('contact.html')


# ============================================================================
# API ENDPOINTS (Legacy - for backward compatibility)
# ============================================================================

@app.route('/api/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'message': 'SD Hotel Furniture API is running',
        'database': 'connected' if db.engine else 'disconnected',
        'timestamp': datetime.utcnow().isoformat()
    })


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Not found'}), 404
    return render_template('index.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    if request.path.startswith('/api/'):
        return jsonify({
            'status': 'error',
            'message': 'Internal server error'
        }), 500
    return jsonify({'error': 'Internal server error'}), 500


@app.errorhandler(403)
def forbidden(error):
    """Handle 403 errors"""
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Forbidden'}), 403
    return jsonify({'error': 'Forbidden'}), 403


# ============================================================================
# CLI COMMANDS
# ============================================================================

@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print('Database initialized!')


@app.cli.command()
def seed_db():
    """Seed the database with sample data"""
    from scripts.seed_data import seed_database
    seed_database()
    print('Database seeded with sample data!')


@app.cli.command()
def create_admin():
    """Create an admin user"""
    email = input('Enter admin email: ')
    username = input('Enter admin username: ')
    password = input('Enter admin password: ')
    
    # Check if user already exists
    if User.query.filter_by(email=email).first():
        print('User with this email already exists!')
        return
    
    if User.query.filter_by(username=username).first():
        print('User with this username already exists!')
        return
    
    # Create admin user
    admin = User.create_user(
        email=email,
        username=username,
        password=password,
        role='admin',
        is_active=True,
        is_verified=True
    )
    
    db.session.add(admin)
    db.session.commit()
    
    print(f'Admin user {username} created successfully!')


if __name__ == '__main__':
    # Run the application
    # Debug mode should be False in production
    app.run(debug=True, host='0.0.0.0', port=5000)
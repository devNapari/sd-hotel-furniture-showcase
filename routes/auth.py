"""
Authentication routes for login, registration, and user management
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime

from models import db
from models.user import User
from models.order import Order
from models.wishlist import Wishlist

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Your account has been deactivated. Please contact support.', 'danger')
                return redirect(url_for('auth.login'))
            
            login_user(user, remember=remember)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.full_name}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').lower()
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        first_name = request.form.get('first_name', '')
        last_name = request.form.get('last_name', '')
        
        # Validation
        if not all([email, username, password, confirm_password]):
            flash('All fields are required.', 'danger')
            return redirect(url_for('auth.register'))
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('auth.register'))
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return redirect(url_for('auth.register'))
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already taken.', 'danger')
            return redirect(url_for('auth.register'))
        
        # Create user
        user = User.create_user(
            email=email,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role='customer'
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@auth_bp.route('/profile')
@login_required
def profile():
    """User profile page"""
    return render_template('auth/profile.html')


@auth_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit user profile"""
    if request.method == 'POST':
        current_user.first_name = request.form.get('first_name', '')
        current_user.last_name = request.form.get('last_name', '')
        current_user.phone = request.form.get('phone', '')
        current_user.company = request.form.get('company', '')
        current_user.address_line1 = request.form.get('address_line1', '')
        current_user.address_line2 = request.form.get('address_line2', '')
        current_user.city = request.form.get('city', '')
        current_user.state = request.form.get('state', '')
        current_user.postal_code = request.form.get('postal_code', '')
        current_user.country = request.form.get('country', '')
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/edit_profile.html')


@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change user password"""
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not current_user.check_password(current_password):
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('auth.change_password'))
        
        if new_password != confirm_password:
            flash('New passwords do not match.', 'danger')
            return redirect(url_for('auth.change_password'))
        
        if len(new_password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return redirect(url_for('auth.change_password'))
        
        current_user.set_password(new_password)
        db.session.commit()
        
        flash('Password changed successfully!', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/change_password.html')


@auth_bp.route('/orders')
@login_required
def orders():
    """View user's orders"""
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('auth/orders.html', orders=user_orders)


@auth_bp.route('/orders/<int:order_id>/delete', methods=['POST'])
@login_required
def delete_order(order_id):
    """Delete a user's order"""
    order = Order.query.get_or_404(order_id)
    
    # Ensure the order belongs to the current user
    if order.user_id != current_user.id:
        flash('You do not have permission to delete this order.', 'danger')
        return redirect(url_for('auth.orders'))
    
    # Only allow deletion of pending or cancelled orders
    if order.status not in ['pending', 'cancelled']:
        flash('Only pending or cancelled orders can be deleted.', 'warning')
        return redirect(url_for('auth.orders'))
    
    db.session.delete(order)
    db.session.commit()
    
    flash('Order deleted successfully.', 'success')
    return redirect(url_for('auth.orders'))


@auth_bp.route('/wishlist')
@login_required
def wishlist():
    """View user's wishlist"""
    wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).order_by(Wishlist.created_at.desc()).all()
    return render_template('auth/wishlist.html', wishlist_items=wishlist_items)


@auth_bp.route('/wishlist/<int:wishlist_id>/delete', methods=['POST'])
@login_required
def delete_wishlist_item(wishlist_id):
    """Delete a wishlist item"""
    wishlist_item = Wishlist.query.get_or_404(wishlist_id)
    
    # Ensure the wishlist item belongs to the current user
    if wishlist_item.user_id != current_user.id:
        flash('You do not have permission to delete this item.', 'danger')
        return redirect(url_for('auth.wishlist'))
    
    db.session.delete(wishlist_item)
    db.session.commit()
    
    flash('Item removed from wishlist.', 'success')
    return redirect(url_for('auth.wishlist'))


@auth_bp.route('/wishlist/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_wishlist(product_id):
    """Add a product to wishlist"""
    from models.product import Product
    
    product = Product.query.get_or_404(product_id)
    
    # Check if already in wishlist
    existing = Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if existing:
        return jsonify({'success': False, 'message': 'Product already in wishlist'}), 400
    
    wishlist_item = Wishlist(user_id=current_user.id, product_id=product_id)
    db.session.add(wishlist_item)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Product added to wishlist'})
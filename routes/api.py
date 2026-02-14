"""
API routes for products, orders, and other data
"""
from flask import Blueprint, jsonify, request, current_app
from flask_login import login_required, current_user
from sqlalchemy import or_
from flask_mail import Mail, Message
from datetime import datetime
import os
import threading

from models import db
from models.product import Product, Category
from models.order import Order, OrderItem
from models.review import Review
from models.wishlist import Wishlist
from models.notification import ContactMessage, ConsultationRequest

from models import db
from models.product import Product, Category
from models.order import Order, OrderItem
from models.review import Review
from models.wishlist import Wishlist

# Mail will be initialized in app.py
mail = None

def init_mail(mail_instance):
    """Initialize mail instance"""
    global mail
    mail = mail_instance


def send_email_async(msg):
    """Send email asynchronously without blocking the request"""
    try:
        with current_app.app_context():
            mail.send(msg)
            print(f"[EMAIL] Successfully sent to {msg.recipients}")
    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send email: {str(e)}")


def send_contact_notification_email(contact_message):
    """Send email notification to admin for new contact message"""
    try:
        admin_email = current_app.config.get('ADMIN_EMAIL')
        
        if not admin_email or not mail:
            print(f"[EMAIL] Skipping email - Admin email: {admin_email}, Mail: {mail}")
            return False
        
        # Create email content
        subject = f"New Contact Message: {contact_message.subject}"
        
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; border: 1px solid #ddd; padding: 20px;">
                    <h2 style="color: #d4af37; border-bottom: 2px solid #d4af37; padding-bottom: 10px;">
                        New Contact Message
                    </h2>
                    
                    <p><strong>From:</strong> {contact_message.first_name} {contact_message.last_name}</p>
                    <p><strong>Email:</strong> <a href="mailto:{contact_message.email}">{contact_message.email}</a></p>
                    <p><strong>Phone:</strong> {contact_message.phone if contact_message.phone else 'Not provided'}</p>
                    <p><strong>Company:</strong> {contact_message.company if contact_message.company else 'Not provided'}</p>
                    <p><strong>Subject:</strong> {contact_message.subject}</p>
                    <p><strong>Newsletter Signup:</strong> {'Yes' if contact_message.newsletter else 'No'}</p>
                    
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                    
                    <h3 style="color: #333;">Message:</h3>
                    <p style="background-color: #f9f9f9; padding: 15px; border-left: 4px solid #d4af37;">
                        {contact_message.message}
                    </p>
                    
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                    
                    <p><strong>Received:</strong> {contact_message.created_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p><strong>Message ID:</strong> #{contact_message.id}</p>
                    
                    <div style="background-color: #f0f0f0; padding: 15px; margin-top: 20px; border-radius: 5px;">
                        <p style="margin: 0;"><strong>⚠️ Action Required:</strong></p>
                        <p style="margin: 10px 0 0 0;">
                            Please <strong>log in to the admin dashboard</strong> to view and respond to this message.
                            You can manage all contact messages and consultations from your admin panel.
                        </p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Create message
        msg = Message(
            subject=subject,
            recipients=[admin_email],
            html=html_body
        )
        
        # Send asynchronously
        thread = threading.Thread(target=send_email_async, args=(msg,))
        thread.daemon = True
        thread.start()
        
        return True
    except Exception as e:
        print(f"[EMAIL] Error preparing contact notification: {str(e)}")
        return False


def send_consultation_notification_email(consultation_request):
    """Send email notification to admin for new consultation request"""
    try:
        admin_email = current_app.config.get('ADMIN_EMAIL')
        
        if not admin_email or not mail:
            print(f"[EMAIL] Skipping email - Admin email: {admin_email}, Mail: {mail}")
            return False
        
        # Get cart items
        cart_items = consultation_request.get_cart_items()
        cart_html = ""
        if cart_items:
            cart_html = "<h3 style='color: #333;'>Cart Items:</h3><table style='width: 100%; border-collapse: collapse;'>"
            cart_html += "<tr style='background-color: #f0f0f0;'><th style='border: 1px solid #ddd; padding: 10px; text-align: left;'>Product</th><th style='border: 1px solid #ddd; padding: 10px; text-align: center;'>Quantity</th><th style='border: 1px solid #ddd; padding: 10px; text-align: right;'>Price</th><th style='border: 1px solid #ddd; padding: 10px; text-align: right;'>Total</th></tr>"
            
            total = 0
            for item in cart_items:
                price = float(item.get('price', 0))
                quantity = int(item.get('quantity', 1))
                item_total = price * quantity
                total += item_total
                cart_html += f"<tr><td style='border: 1px solid #ddd; padding: 10px;'>{item.get('name', 'Unknown')}</td><td style='border: 1px solid #ddd; padding: 10px; text-align: center;'>{quantity}</td><td style='border: 1px solid #ddd; padding: 10px; text-align: right;'>GHS {price:.2f}</td><td style='border: 1px solid #ddd; padding: 10px; text-align: right;'>GHS {item_total:.2f}</td></tr>"
            
            cart_html += f"<tr style='background-color: #f9f9f9; font-weight: bold;'><td colspan='3' style='border: 1px solid #ddd; padding: 10px; text-align: right;'>Total:</td><td style='border: 1px solid #ddd; padding: 10px; text-align: right;'>GHS {total:.2f}</td></tr>"
            cart_html += "</table>"
        
        # Create email content
        subject = f"New Consultation Request: {consultation_request.subject}"
        
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; border: 1px solid #ddd; padding: 20px;">
                    <h2 style="color: #d4af37; border-bottom: 2px solid #d4af37; padding-bottom: 10px;">
                        New Consultation Request
                    </h2>
                    
                    <p><strong>From:</strong> {consultation_request.first_name} {consultation_request.last_name}</p>
                    <p><strong>Email:</strong> <a href="mailto:{consultation_request.email}">{consultation_request.email}</a></p>
                    <p><strong>Phone:</strong> {consultation_request.phone}</p>
                    <p><strong>Company:</strong> {consultation_request.company if consultation_request.company else 'Not provided'}</p>
                    <p><strong>Subject:</strong> {consultation_request.subject}</p>
                    
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                    
                    <h3 style="color: #333;">Consultation Details:</h3>
                    <p><strong>Preferred Date:</strong> {consultation_request.preferred_date}</p>
                    <p><strong>Preferred Time:</strong> {consultation_request.preferred_time}</p>
                    <p><strong>Newsletter Signup:</strong> {'Yes' if consultation_request.newsletter else 'No'}</p>
                    
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                    
                    <h3 style="color: #333;">Message:</h3>
                    <p style="background-color: #f9f9f9; padding: 15px; border-left: 4px solid #d4af37;">
                        {consultation_request.message}
                    </p>
                    
                    {f'<hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">{cart_html}' if cart_html else ''}
                    
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                    
                    <p><strong>Received:</strong> {consultation_request.created_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p><strong>Request ID:</strong> #{consultation_request.id}</p>
                    
                    <div style="background-color: #f0f0f0; padding: 15px; margin-top: 20px; border-radius: 5px;">
                        <p style="margin: 0;"><strong>⚠️ Action Required:</strong></p>
                        <p style="margin: 10px 0 0 0;">
                            Please <strong>log in to the admin dashboard</strong> to view and respond to this consultation request.
                            You can manage all consultations and messages from your admin panel.
                        </p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Create message
        msg = Message(
            subject=subject,
            recipients=[admin_email],
            html=html_body
        )
        
        # Send asynchronously
        thread = threading.Thread(target=send_email_async, args=(msg,))
        thread.daemon = True
        thread.start()
        
        return True
    except Exception as e:
        print(f"[EMAIL] Error preparing consultation notification: {str(e)}")
        return False

api_bp = Blueprint('api', __name__)


# ============================================================================
# PRODUCT API
# ============================================================================

@api_bp.route('/products', methods=['GET'])
def get_products():
    """Get all products with optional filtering"""
    try:
        # Get query parameters
        category_id = request.args.get('category_id', type=int)
        search = request.args.get('search', '')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        is_featured = request.args.get('is_featured', type=bool)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 100, type=int)  # Increased from 12 to 100
        
        # Build query
        query = Product.query.filter_by(is_active=True)
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        if search:
            query = query.filter(
                or_(
                    Product.name.ilike(f'%{search}%'),
                    Product.description.ilike(f'%{search}%')
                )
            )
        
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        
        if is_featured:
            query = query.filter_by(is_featured=True)
        
        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'status': 'success',
            'products': [p.to_dict() for p in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@api_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a single product by ID"""
    try:
        product = Product.query.get_or_404(product_id)
        
        # Increment view count
        product.view_count += 1
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'product': product.to_dict(include_images=True, include_reviews=True)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@api_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all categories"""
    try:
        categories = Category.query.filter_by(is_active=True).all()
        return jsonify({
            'status': 'success',
            'categories': [c.to_dict() for c in categories]
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ============================================================================
# WISHLIST API
# ============================================================================

@api_bp.route('/wishlist', methods=['GET'])
@login_required
def get_wishlist():
    """Get user's wishlist"""
    try:
        wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).all()
        return jsonify({
            'status': 'success',
            'items': [item.to_dict() for item in wishlist_items]
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@api_bp.route('/wishlist/<int:product_id>', methods=['POST'])
@login_required
def add_to_wishlist(product_id):
    """Add product to wishlist"""
    try:
        product = Product.query.get_or_404(product_id)
        
        # Check if already in wishlist
        existing = Wishlist.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first()
        
        if existing:
            return jsonify({
                'status': 'info',
                'message': 'Product already in wishlist'
            })
        
        wishlist_item = Wishlist(
            user_id=current_user.id,
            product_id=product_id
        )
        
        db.session.add(wishlist_item)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Product added to wishlist'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@api_bp.route('/wishlist/<int:product_id>', methods=['DELETE'])
@login_required
def remove_from_wishlist(product_id):
    """Remove product from wishlist"""
    try:
        wishlist_item = Wishlist.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first_or_404()
        
        db.session.delete(wishlist_item)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Product removed from wishlist'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ============================================================================
# REVIEW API
# ============================================================================

@api_bp.route('/products/<int:product_id>/reviews', methods=['GET'])
def get_product_reviews(product_id):
    """Get reviews for a product"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        reviews = Review.query.filter_by(
            product_id=product_id,
            is_approved=True
        ).order_by(Review.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'status': 'success',
            'reviews': [r.to_dict() for r in reviews.items],
            'total': reviews.total,
            'pages': reviews.pages
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@api_bp.route('/products/<int:product_id>/reviews', methods=['POST'])
@login_required
def create_review(product_id):
    """Create a review for a product"""
    try:
        data = request.get_json()
        
        # Check if user already reviewed this product
        existing = Review.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first()
        
        if existing:
            return jsonify({
                'status': 'error',
                'message': 'You have already reviewed this product'
            }), 400
        
        review = Review(
            product_id=product_id,
            user_id=current_user.id,
            rating=data.get('rating'),
            title=data.get('title', ''),
            comment=data.get('comment'),
            is_approved=False  # Requires admin approval
        )
        
        db.session.add(review)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Review submitted for approval',
            'review': review.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ============================================================================
# ORDER API
# ============================================================================

@api_bp.route('/orders', methods=['GET'])
@login_required
def get_orders():
    """Get user's orders"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        orders = Order.query.filter_by(user_id=current_user.id).order_by(
            Order.created_at.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'status': 'success',
            'orders': [o.to_dict() for o in orders.items],
            'total': orders.total,
            'pages': orders.pages
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@api_bp.route('/orders/<int:order_id>', methods=['GET'])
@login_required
def get_order(order_id):
    """Get a single order"""
    try:
        order = Order.query.filter_by(
            id=order_id,
            user_id=current_user.id
        ).first_or_404()
        
        return jsonify({
            'status': 'success',
            'order': order.to_dict(include_items=True)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ============================================================================
# CONTACT FORM API
# ============================================================================

@api_bp.route('/contact', methods=['POST'])
def submit_contact_form():
    """Handle contact form submission and save to database"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['firstName', 'lastName', 'email', 'subject', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'status': 'error',
                    'message': f'{field} is required'
                }), 400
        
        # Extract form data
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        email = data.get('email')
        phone = data.get('phone', '')
        company = data.get('company', '')
        subject = data.get('subject')
        message_text = data.get('message')
        # Convert newsletter checkbox: 'on' (string) or True (boolean) → 1, else → 0
        newsletter_raw = data.get('newsletter', False)
        newsletter = 1 if (newsletter_raw == 'on' or newsletter_raw is True) else 0
        
        # Save to database
        contact_msg = ContactMessage(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            company=company,
            subject=subject,
            message=message_text,
            newsletter=newsletter
        )
        
        db.session.add(contact_msg)
        db.session.commit()
        
        print(f"[CONTACT FORM] New message from {first_name} {last_name} ({email})")
        print(f"  Subject: {subject}")
        print(f"  Message: {message_text[:100]}...")
        
        # Send email notification to admin (asynchronous)
        send_contact_notification_email(contact_msg)
        
        return jsonify({
            'status': 'success',
            'message': 'Your message has been received! We will get back to you soon.',
            'id': contact_msg.id
        })
            
    except Exception as e:
        print(f"Error saving contact form: {str(e)}")
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': 'Error saving your message. Please try again.'
        }), 500


# ============================================================================
# CONSULTATION FORM API
# ============================================================================

@api_bp.route('/consultation', methods=['POST'])
def submit_consultation_form():
    """Handle consultation form submission and save to database"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['firstName', 'lastName', 'email', 'phone', 'subject', 'message', 'preferredDate', 'preferredTime']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'status': 'error',
                    'message': f'{field} is required'
                }), 400
        
        # Extract form data
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        email = data.get('email')
        phone = data.get('phone')
        company = data.get('company', '')
        subject = data.get('subject')
        message_text = data.get('message')
        preferred_date = data.get('preferredDate')
        preferred_time = data.get('preferredTime')
        # Convert newsletter checkbox: 'on' (string) or True (boolean) → 1, else → 0
        newsletter_raw = data.get('newsletter', False)
        newsletter = 1 if (newsletter_raw == 'on' or newsletter_raw is True) else 0
        cart_items = data.get('cartItems', [])
        
        # Save to database
        consultation = ConsultationRequest(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            company=company,
            subject=subject,
            message=message_text,
            preferred_date=preferred_date,
            preferred_time=preferred_time,
            newsletter=newsletter
        )
        
        # Store cart items as JSON
        consultation.set_cart_items(cart_items)
        
        db.session.add(consultation)
        db.session.commit()
        
        # Calculate cart total for logging
        cart_total = sum(item.get('price', 0) * item.get('quantity', 1) for item in cart_items)
        
        print(f"[CONSULTATION] New request from {first_name} {last_name} ({email})")
        print(f"  Subject: {subject}")
        print(f"  Preferred Date/Time: {preferred_date} @ {preferred_time}")
        print(f"  Message: {message_text[:100]}...")
        if cart_items:
            print(f"  Cart Items ({len(cart_items)} total): ${cart_total:.2f}")
        
        # Send email notification to admin (asynchronous)
        send_consultation_notification_email(consultation)
        
        return jsonify({
            'status': 'success',
            'message': 'Your consultation request has been received! We will contact you within 24 hours.',
            'id': consultation.id
        })
            
    except Exception as e:
        print(f"Error saving consultation form: {str(e)}")
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': 'Error saving your consultation request. Please try again.'
        }), 500


# ============================================================================
# NOTIFICATIONS API
# ============================================================================

@api_bp.route('/admin/notifications/count', methods=['GET'])
@login_required
def get_notifications_count():
    """Get count of unread notifications"""
    try:
        contact_count = ContactMessage.query.filter_by(is_read=False).count()
        consultation_count = ConsultationRequest.query.filter_by(is_read=False).count()
        
        return jsonify({
            'status': 'success',
            'contacts': contact_count,
            'consultations': consultation_count,
            'total': contact_count + consultation_count
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@api_bp.route('/admin/notifications/contacts', methods=['GET'])
@login_required
def get_contact_messages():
    """Get all contact messages"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        unread_only = request.args.get('unread_only', False, type=bool)
        
        query = ContactMessage.query
        if unread_only:
            query = query.filter_by(is_read=False)
        
        # Order by newest first
        pagination = query.order_by(ContactMessage.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'status': 'success',
            'messages': [msg.to_dict() for msg in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@api_bp.route('/admin/notifications/consultations', methods=['GET'])
@login_required
def get_consultation_requests():
    """Get all consultation requests"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        unread_only = request.args.get('unread_only', False, type=bool)
        
        query = ConsultationRequest.query
        if unread_only:
            query = query.filter_by(is_read=False)
        
        # Order by newest first
        pagination = query.order_by(ConsultationRequest.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'status': 'success',
            'requests': [req.to_dict() for req in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@api_bp.route('/admin/notifications/contact/<int:message_id>/read', methods=['POST'])
@login_required
def mark_contact_read(message_id):
    """Mark contact message as read"""
    try:
        msg = ContactMessage.query.get_or_404(message_id)
        msg.is_read = True
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Message marked as read'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@api_bp.route('/admin/notifications/consultation/<int:request_id>/read', methods=['POST'])
@login_required
def mark_consultation_read(request_id):
    """Mark consultation request as read"""
    try:
        req = ConsultationRequest.query.get_or_404(request_id)
        req.is_read = True
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Request marked as read'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@api_bp.route('/admin/notifications/contact/<int:message_id>', methods=['DELETE'])
@login_required
def delete_contact_message(message_id):
    """Delete contact message"""
    try:
        msg = ContactMessage.query.get_or_404(message_id)
        db.session.delete(msg)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Message deleted'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@api_bp.route('/admin/notifications/consultation/<int:request_id>', methods=['DELETE'])
@login_required
def delete_consultation_request(request_id):
    """Delete consultation request"""
    try:
        req = ConsultationRequest.query.get_or_404(request_id)
        db.session.delete(req)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Request deleted'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


# ============================================================================
# HEALTH CHECK
# ============================================================================

@api_bp.route('/health', methods=['GET'])
def health():
    """API health check"""
    return jsonify({
        'status': 'healthy',
        'message': 'API is running'
    })
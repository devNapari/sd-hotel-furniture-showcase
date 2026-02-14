"""
Admin Panel Configuration
Provides Flask-Admin interface for managing the application
"""

from flask import redirect, url_for, request, flash, current_app
from markupsafe import Markup
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules
from flask_login import current_user
from wtforms import TextAreaField, SelectField, StringField, BooleanField
from wtforms.validators import DataRequired, ValidationError, URL, Optional
from flask_admin.form.upload import FileUploadField
import re
import json
import os
import uuid
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from datetime import datetime
from models import db
from models.user import User
from models.product import Product, Category, ProductImage
from models.order import Order, OrderItem
from models.review import Review
from models.wishlist import Wishlist
from models.blog import BlogPost, BlogCategory, BlogComment
from sqlalchemy.exc import IntegrityError


class SecureModelView(ModelView):
    """Base model view with authentication"""
    
    def is_accessible(self):
        """Only allow access to authenticated admin users"""
        return current_user.is_authenticated and current_user.is_admin
    
    def inaccessible_callback(self, name, **kwargs):
        """Redirect to login page if not authorized"""
        return redirect(url_for('auth.login', next=request.url))


class SecureAdminIndexView(AdminIndexView):
    """Custom admin index view with authentication"""

    @expose('/')
    def index(self):
        """Admin dashboard with statistics"""
        if not current_user.is_authenticated or not current_user.is_admin:
            return redirect(url_for('auth.login', next=request.url))
        
        # Get statistics
        stats = {
            'total_users': User.query.count(),
            'total_products': Product.query.count(),
            'total_orders': Order.query.count(),
            'total_reviews': Review.query.count(),
            'total_blog_posts': BlogPost.query.count(),
            'active_products': Product.query.filter_by(is_active=True).count(),
            'pending_orders': Order.query.filter_by(status='pending').count(),
            'pending_reviews': Review.query.filter_by(is_approved=False).count(),
            'published_posts': BlogPost.query.filter_by(status='published').count(),
            'pending_comments': BlogComment.query.filter_by(is_approved=False).count(),
        }
        
        # Get recent orders
        recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
        
        # Get recent users
        recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
        
        return self.render('admin/dashboard.html', 
                         stats=stats, 
                         recent_orders=recent_orders,
                         recent_users=recent_users)


class UserAdmin(SecureModelView):
    """Admin view for User model"""
    
    column_list = ['id', 'username', 'email', 'role', 'is_active', 'is_verified', 'created_at']
    column_searchable_list = ['username', 'email', 'first_name', 'last_name']
    column_filters = ['role', 'is_active', 'is_verified', 'created_at']
    column_editable_list = ['is_active', 'is_verified', 'role']
    column_default_sort = ('created_at', True)
    
    form_excluded_columns = ['password_hash', 'orders', 'reviews', 'wishlist_items']
    
    column_labels = {
        'is_active': 'Active',
        'is_verified': 'Verified',
        'created_at': 'Registered',
        'last_login': 'Last Login'
    }
    
    def scaffold_form(self):
        """Customize form"""
        form_class = super(UserAdmin, self).scaffold_form()
        return form_class


    def _generate_unique_slug(self, session, Model, base_slug, current_id=None):
        """Generate a unique slug by appending -1, -2, ... if needed."""
        slug = base_slug
        i = 1
        query = session.query(Model).filter_by(slug=slug)
        if current_id:
            query = query.filter(Model.id != current_id)
        while query.first() is not None:
            slug = f"{base_slug}-{i}"
            i += 1
            query = session.query(Model).filter_by(slug=slug)
            if current_id:
                query = query.filter(Model.id != current_id)
        return slug


class ProductAdmin(SecureModelView):
    """Enhanced Admin view for Product model with comprehensive image management"""
    
    column_list = ['id', 'name', 'sku', 'price', 'stock_quantity', 'category', 'is_active', 'is_featured']
    column_searchable_list = ['name', 'sku', 'description']
    column_filters = ['category_id', 'is_active', 'is_featured', 'is_new', 'is_on_sale', 'created_at']
    column_editable_list = ['price', 'stock_quantity', 'is_active', 'is_featured']
    column_default_sort = ('created_at', True)
    
    # Allow editing slug in admin so admins can preview/edit generated slug
    form_excluded_columns = ['view_count', 'purchase_count', 'created_at', 'updated_at', 'images', 'reviews', 'order_items', 'wishlist_items']
    
    # EXPLICITLY include upload_images in the form
    form_columns = ['name', 'slug', 'sku', 'description', 'short_description', 'price', 'compare_at_price', 'cost_price', 'category_id', 'brand', 'material', 'color', 'dimensions', 'weight', 'features', 'specifications', 'meta_title', 'meta_description', 'meta_keywords', 'is_active', 'is_featured', 'is_new', 'is_on_sale', 'stock_quantity', 'low_stock_threshold', 'track_inventory', 'allow_backorder', 'upload_images']
    
    column_labels = {
        'sku': 'SKU',
        'category': 'Category',
        'category_id': 'Category *',  # Add asterisk to show it's required
        'is_active': 'Active',
        'is_featured': 'Featured',
        'is_new': 'New',
        'is_on_sale': 'On Sale',
        'stock_quantity': 'Stock',
        'low_stock_threshold': 'Low Stock Alert',
        'track_inventory': 'Track Inventory',
        'allow_backorder': 'Allow Backorder'
    }
    
    # Inline form configuration for better field ordering
    inline_models = None
    
    column_formatters = {
        'price': lambda v, c, m, p: f'${m.price:.2f}',
        'compare_at_price': lambda v, c, m, p: f'${m.compare_at_price:.2f}' if m.compare_at_price else '-',
    }
    
    form_overrides = {
        'features': TextAreaField,
        'specifications': TextAreaField,
    }
    
    form_widget_args = {
        'features': {
            'rows': 5,
            'placeholder': 'Enter features as JSON array, e.g.: ["Feature 1", "Feature 2"]'
        },
        'specifications': {
            'rows': 5,
            'placeholder': 'Enter specifications as JSON object, e.g.: {"Material": "Wood", "Color": "Brown"}'
        },
        'name': {
            'placeholder': 'Enter product name'
        },
        'sku': {
            'placeholder': 'Enter unique SKU (e.g., GR-001)'
        },
        'price': {
            'placeholder': 'Enter price (e.g., 299.99)'
        },
        'description': {
            'rows': 6,
            'placeholder': 'Enter detailed product description'
        },
        'short_description': {
            'rows': 3,
            'placeholder': 'Enter brief description (shown in product listings)'
        },
        'slug': {
            'placeholder': 'URL-friendly slug (auto-generated from name if left blank)',
            'description': 'Editable URL slug. Leave blank to auto-generate and ensure uniqueness.'
        }
    }
    
    # Add helpful text for fields
    form_args = {
        'category_id': {
            'label': 'Category *',
            'description': 'Select the product category (required)'
        },
        'name': {
            'description': 'Product name as it will appear on the website'
        },
        'sku': {
            'description': 'Unique product identifier for inventory management'
        },
        'price': {
            'description': 'Selling price in USD'
        },
        'stock_quantity': {
            'description': 'Current stock level'
        },
        'is_active': {
            'description': 'Uncheck to hide product from shop. New products are active by default.',
            'default': True
        }
    }
    
    # Image upload configuration - ONLY uploaded images (no external URLs)
    form_extra_fields = {
        'upload_images': FileUploadField(
            'Upload Product Images',
            base_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads', 'products'),
            relative_path='',
            allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'],
            description='Upload product images (you can select multiple files at once)',
            render_kw={'multiple': True}
        )
    }
    
    def scaffold_form(self):
        """Customize form to show category as dropdown and add image management fields"""
        form_class = super(ProductAdmin, self).scaffold_form()
        
        print(f"[DEBUG] scaffold_form called")
        
        # Override category_id field to show as dropdown with category names
        def get_categories():
            """Get list of active categories for dropdown"""
            categories = Category.query.filter_by(is_active=True).order_by(Category.name).all()
            return [(0, '-- Select Category --')] + [(c.id, c.name) for c in categories]
        
        form_class.category_id = SelectField(
            'Category *',
            choices=get_categories,
            coerce=int,
            description='Select the product category (required)'
        )
        
        print(f"[DEBUG] Added category_id SelectField")
        # upload_images field is defined in form_extra_fields
        
        return form_class
    
    def _generate_unique_slug(self, session, Model, base_slug, current_id=None):
        """Generate a unique slug by appending -1, -2, ... if needed."""
        slug = base_slug
        i = 1
        query = session.query(Model).filter_by(slug=slug)
        if current_id:
            query = query.filter(Model.id != current_id)
        while query.first() is not None:
            slug = f"{base_slug}-{i}"
            i += 1
            query = session.query(Model).filter_by(slug=slug)
            if current_id:
                query = query.filter(Model.id != current_id)
        return slug
    
    def _handle_image_management(self, form, model, is_created):
        """Handle image management - ONLY uploaded images, no external URLs"""

        print(f"\n[DEBUG] ========== _handle_image_management called ==========")
        print(f"[DEBUG] Form type: {type(form)}")
        print(f"[DEBUG] Model: {model.name} (ID: {model.id})")
        print(f"[DEBUG] is_created: {is_created}")

        # Initialize pending images list
        if not hasattr(model, '_pending_images'):
            model._pending_images = []
            print(f"[DEBUG] Initialized _pending_images list")

        # Check if upload_images field exists and has data
        if hasattr(form, 'upload_images') and form.upload_images.data:
            upload_field = form.upload_images
            print(f"[DEBUG] upload_images field exists and has data")
            print(f"[DEBUG] upload_images.data type: {type(upload_field.data)}")
            print(f"[DEBUG] Processing files...")
            self._process_uploaded_images(upload_field.data, model)
        else:
            print(f"[DEBUG] upload_images field missing or empty")
    
    def on_model_change(self, form, model, is_created):
        """Validate and process model before saving, handle image uploads and URLs"""
        try:
            # Ensure new products are active by default
            if is_created and model.is_active is None:
                model.is_active = True

            # Validate required fields
            if not model.category_id or model.category_id == 0:
                raise ValidationError('Category is required. Please select a category from the dropdown.')

            if not model.name or not model.name.strip():
                raise ValidationError('Product name is required.')

            if not model.sku or not model.sku.strip():
                raise ValidationError('SKU is required.')

            if not model.price or model.price <= 0:
                raise ValidationError('Price must be greater than 0.')

            # Generate slug from name if not provided, or normalize provided slug
            if not model.slug:
                base_slug = re.sub(r'[^\w\s-]', '', model.name.lower())
                base_slug = re.sub(r'[-\s]+', '-', base_slug).strip('-')
            else:
                base_slug = re.sub(r'[^\w\s-]', '', str(model.slug).lower())
                base_slug = re.sub(r'[-\s]+', '-', base_slug).strip('-')

            if not base_slug:
                raise ValidationError('Product name/slug must contain at least one alphanumeric character')

            # Ensure slug is unique (append -1, -2... if needed)
            current_id = model.id if not is_created else None
            model.slug = self._generate_unique_slug(db.session, Product, base_slug, current_id=current_id)

            # Validate and parse JSON fields
            if model.features:
                if isinstance(model.features, str):
                    try:
                        model.features = json.loads(model.features)
                    except json.JSONDecodeError:
                        raise ValidationError('Features must be valid JSON array. Example: ["Feature 1", "Feature 2"]')

            if model.specifications:
                if isinstance(model.specifications, str):
                    try:
                        model.specifications = json.loads(model.specifications)
                    except json.JSONDecodeError:
                        raise ValidationError('Specifications must be valid JSON object. Example: {"Material": "Wood"}')

            # Handle image management based on priority system
            self._handle_image_management(form, model, is_created)

            # Call parent method to save the product
            super(ProductAdmin, self).on_model_change(form, model, is_created)

        except ValidationError as e:
            flash(str(e), 'error')
            raise
        except Exception as e:
            flash(f'Error saving product: {str(e)}', 'error')
            raise
    
    
    def create_model(self, form):
        """Create model with IntegrityError retry for slug conflicts, then process pending images"""
        print(f"\n[DEBUG] create_model called")
        try:
            model = super(ProductAdmin, self).create_model(form)
            print(f"[DEBUG] Model created with ID: {model.id}")

            # Process pending images after model is created and committed
            # Pass is_update=False since this is a new product (no old images to delete)
            self._process_pending_images(model, is_update=False)

        except IntegrityError as e:
            # Slug collision despite uniqueness check — retry with appended timestamp
            if 'slug' in str(e).lower():
                db.session.rollback()
                flash('Slug collision detected. Retrying with unique suffix...', 'info')

                # Append timestamp to base slug and retry
                import time
                base_slug = model.slug or re.sub(r'[^\w\s-]', '', model.name.lower())
                base_slug = re.sub(r'[-\s]+', '-', base_slug).strip('-')
                model.slug = f"{base_slug}-{int(time.time() % 10000)}"

                # Regenerate to ensure absolute uniqueness
                model.slug = self._generate_unique_slug(db.session, Product, model.slug, current_id=None)
                model = super(ProductAdmin, self).create_model(form)

                # Process pending images after retry creation
                self._process_pending_images(model, is_update=False)
            else:
                db.session.rollback()
                raise

        return model
    
    def update_model(self, form, model):
        """Update model with IntegrityError retry for slug conflicts, then process pending images"""
        try:
            # Call parent update_model - it modifies model in place and returns bool
            # But we still have access to the model object, so process images here
            super(ProductAdmin, self).update_model(form, model)

            # Process pending images after model is updated and committed
            # Pass is_update=True to delete old images
            self._process_pending_images(model, is_update=True)

        except IntegrityError as e:
            # Slug collision — retry with appended timestamp
            if 'slug' in str(e).lower():
                db.session.rollback()
                flash('Slug collision detected. Retrying with unique suffix...', 'info')

                # Append timestamp to base slug and retry
                import time
                base_slug = model.slug or re.sub(r'[^\w\s-]', '', model.name.lower())
                base_slug = re.sub(r'[-\s]+', '-', base_slug).strip('-')
                model.slug = f"{base_slug}-{int(time.time() % 10000)}"

                # Regenerate to ensure absolute uniqueness
                model.slug = self._generate_unique_slug(db.session, Product, model.slug, current_id=model.id)
                super(ProductAdmin, self).update_model(form, model)

                # Process pending images after retry update
                self._process_pending_images(model, is_update=True)
            else:
                db.session.rollback()
                raise

        return True
    
    def _process_uploaded_images(self, uploaded_files, model):
        """Process uploaded image files with latest image tracking"""
        print(f"[DEBUG] _process_uploaded_images called")
        print(f"[DEBUG] uploaded_files type: {type(uploaded_files)}")
        print(f"[DEBUG] uploaded_files: {uploaded_files}")
        
        if not uploaded_files:
            print(f"[DEBUG] No files to process, returning")
            return
        
        # Create upload directory if it doesn't exist
        upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads', 'products')
        os.makedirs(upload_dir, exist_ok=True)
        print(f"[DEBUG] Upload directory: {upload_dir}")
        
        # Initialize pending images list if it doesn't exist
        if not hasattr(model, '_pending_images'):
            model._pending_images = []
            print(f"[DEBUG] Initialized _pending_images list")
        
        # Handle FileStorage object (single file) vs list of files
        # FileStorage is iterable but we need to treat it as a single file
        if isinstance(uploaded_files, FileStorage):
            files = [uploaded_files]
            print(f"[DEBUG] Single FileStorage object detected, wrapping in list")
        elif hasattr(uploaded_files, '__iter__') and not isinstance(uploaded_files, str):
            files = list(uploaded_files)
            print(f"[DEBUG] Multiple files detected")
        else:
            files = [uploaded_files]
            print(f"[DEBUG] Single file detected")
        
        print(f"[DEBUG] Processing {len(files)} files")
        
        for index, file in enumerate(files):
            if not file:
                print(f"[DEBUG] Skipping empty file at index {index}")
                continue
                
            try:
                # Secure filename and add UUID prefix to ensure uniqueness
                original_filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4().hex[:8]}_{original_filename}"
                
                print(f"[DEBUG] Original filename: {file.filename}")
                print(f"[DEBUG] Secure filename: {original_filename}")
                print(f"[DEBUG] Unique filename: {unique_filename}")
                
                # Reset file stream to beginning in case it was read
                file.stream.seek(0)
                
                # Save file
                file_path = os.path.join(upload_dir, unique_filename)
                file.save(file_path)
                print(f"[DEBUG] File saved to: {file_path}")
                
                # Check file size to verify it was saved correctly
                file_size = os.path.getsize(file_path)
                print(f"[DEBUG] File size: {file_size} bytes")
                
                if file_size == 0:
                    print(f"[ERROR] File size is 0! File may not have been saved correctly")
                    flash(f"Error: Image file is empty", 'error')
                    continue
                
                # Create ProductImage record - store in pending list to be processed after product is saved
                image_url = f"/static/uploads/products/{unique_filename}"
                
                model._pending_images.append({
                    'image_url': image_url,
                    'alt_text': f"{model.name} - Image {index + 1}",
                    'is_primary': (index == 0),
                    'display_order': index
                })
                print(f"[DEBUG] Added to pending images: {image_url}")
                
            except Exception as e:
                print(f"[ERROR] Exception uploading file {index}: {str(e)}")
                flash(f"Error uploading image {index + 1}: {str(e)}", 'warning')
    
    
    def _process_pending_images(self, model, is_update=True):
        """Process pending images after product is saved
        
        For updates: Delete ALL old images first, then add new ones
        For creates: Just add new images
        """
        print(f"[DEBUG] _process_pending_images called for product {model.id}: {model.name}")
        print(f"[DEBUG] is_update: {is_update}")
        print(f"[DEBUG] Has _pending_images attr: {hasattr(model, '_pending_images')}")
        
        if hasattr(model, '_pending_images'):
            print(f"[DEBUG] Pending images list: {model._pending_images}")
        
        if hasattr(model, '_pending_images') and model._pending_images:
            try:
                # If this is an update, delete all existing images for this product
                if is_update:
                    old_images = ProductImage.query.filter_by(product_id=model.id).all()
                    if old_images:
                        print(f"[DEBUG] Deleting {len(old_images)} old images for product update")
                        for old_img in old_images:
                            # Delete the actual file from disk
                            try:
                                file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static' + old_img.image_url)
                                if os.path.exists(file_path):
                                    os.remove(file_path)
                                    print(f"[DEBUG] Deleted file: {file_path}")
                            except Exception as e:
                                print(f"[WARNING] Could not delete file {old_img.image_url}: {str(e)}")
                            
                            db.session.delete(old_img)
                        
                        db.session.commit()
                        print(f"[DEBUG] Committed deletion of old images")
                
                print(f"[DEBUG] Processing {len(model._pending_images)} pending images")
                for img_data in model._pending_images:
                    product_image = ProductImage(
                        product_id=model.id,
                        image_url=img_data['image_url'],
                        alt_text=img_data['alt_text'],
                        is_primary=img_data['is_primary'],
                        display_order=img_data['display_order']
                    )
                    db.session.add(product_image)
                    print(f"[DEBUG] Added ProductImage: product_id={model.id}, image_url={img_data['image_url']}, is_primary={img_data['is_primary']}")
                
                # Commit pending images to database
                db.session.commit()
                print(f"[DEBUG] Committed {len(model._pending_images)} images to database")
                
                # Refresh the model to reload relationships from database
                # This ensures model.images is refreshed so main_image property returns correct data
                db.session.refresh(model)
                print(f"[DEBUG] Refreshed model relationships - model.main_image should now return: {model.main_image}")
                
                # Clear pending images
                model._pending_images = []
            except Exception as e:
                db.session.rollback()
                print(f"[ERROR] Failed to process pending images: {str(e)}")
                flash(f'Error saving images: {str(e)}', 'error')
                raise
        else:
            print(f"[DEBUG] No pending images to process")


class CategoryAdmin(SecureModelView):
    """Admin view for Category model"""
    
    column_list = ['id', 'name', 'slug', 'parent', 'is_active']
    column_searchable_list = ['name', 'description']
    column_filters = ['parent_id', 'is_active']
    column_editable_list = ['name', 'is_active']
    
    form_excluded_columns = ['slug', 'products', 'subcategories', 'created_at', 'updated_at']
    
    column_labels = {
        'is_active': 'Active',
        'display_order': 'Display Order',
        'parent': 'Parent Category'
    }
    
    def on_model_change(self, form, model, is_created):
        """Generate slug from name if not provided"""
        try:
            if not model.slug:
                model.slug = re.sub(r'[^\w\s-]', '', model.name.lower())
                model.slug = re.sub(r'[-\s]+', '-', model.slug).strip('-')
            
            # Ensure slug is not empty
            if not model.slug:
                raise ValidationError('Category name must contain at least one alphanumeric character')
            
            super(CategoryAdmin, self).on_model_change(form, model, is_created)
            
        except ValidationError as e:
            flash(str(e), 'error')
            raise
        except Exception as e:
            flash(f'Error saving category: {str(e)}', 'error')
            raise



class ProductImageAdmin(SecureModelView):
    """Admin view for ProductImage model"""
    
    column_list = ['id', 'product', 'image_url', 'alt_text', 'is_primary', 'display_order']
    column_searchable_list = ['alt_text']
    column_filters = ['product_id', 'is_primary']
    column_editable_list = ['is_primary', 'display_order']
    column_default_sort = ('display_order', False)
    
    column_labels = {
        'is_primary': 'Primary Image',
        'display_order': 'Order'
    }


class OrderAdmin(SecureModelView):
    """Admin view for Order model"""
    
    column_list = ['id', 'order_number', 'user', 'status', 'payment_status', 'total_amount', 'created_at']
    column_searchable_list = ['order_number', 'tracking_number']
    column_filters = ['user_id', 'status', 'payment_status', 'payment_method', 'created_at']
    column_editable_list = ['status', 'payment_status']
    column_default_sort = ('created_at', True)
    
    form_excluded_columns = ['order_number', 'items', 'created_at', 'updated_at']
    
    column_labels = {
        'order_number': 'Order #',
        'payment_status': 'Payment',
        'total_amount': 'Total',
        'created_at': 'Date'
    }
    
    column_formatters = {
        'total_amount': lambda v, c, m, p: f'${m.total_amount:.2f}',
    }


class OrderItemAdmin(SecureModelView):
    """Admin view for OrderItem model"""
    
    column_list = ['id', 'order', 'product_name', 'quantity', 'unit_price', 'subtotal']
    column_searchable_list = ['product_name', 'product_sku']
    column_filters = ['order_id']
    
    form_excluded_columns = ['created_at']
    
    column_labels = {
        'product_name': 'Product',
        'product_sku': 'SKU',
        'unit_price': 'Price',
        'subtotal': 'Subtotal'
    }
    
    column_formatters = {
        'unit_price': lambda v, c, m, p: f'${m.unit_price:.2f}',
        'subtotal': lambda v, c, m, p: f'${m.subtotal:.2f}',
    }


class ReviewAdmin(SecureModelView):
    """Admin view for Review model"""
    
    column_list = ['id', 'product', 'user', 'rating', 'is_approved', 'is_verified_purchase', 'created_at']
    column_searchable_list = ['title', 'comment']
    column_filters = ['product_id', 'user_id', 'rating', 'is_approved', 'is_verified_purchase', 'created_at']
    column_editable_list = ['is_approved']
    column_default_sort = ('created_at', True)
    
    form_excluded_columns = ['created_at', 'updated_at']
    
    column_labels = {
        'is_approved': 'Approved',
        'is_verified_purchase': 'Verified Purchase',
        'created_at': 'Date'
    }


class WishlistAdmin(SecureModelView):
    """Admin view for Wishlist model"""
    
    column_list = ['id', 'user', 'product', 'notes', 'created_at']
    column_searchable_list = ['notes']
    column_filters = ['user_id', 'product_id', 'created_at']
    column_default_sort = ('created_at', True)
    
    form_excluded_columns = ['created_at']


class BlogPostAdmin(SecureModelView):
    """Admin view for BlogPost model"""
    
    column_list = ['id', 'title', 'category', 'status', 'is_featured', 'views', 'published_at']
    column_searchable_list = ['title', 'content', 'excerpt']
    column_filters = ['status', 'is_featured', 'published_at', 'created_at']
    column_editable_list = []
    column_default_sort = ('created_at', True)
    
    form_excluded_columns = ['slug', 'views', 'created_at', 'updated_at']
    
    column_labels = {
        'is_featured': 'Featured',
        'published_at': 'Published',
        'created_at': 'Created',
        'meta_title': 'SEO Title',
        'meta_description': 'SEO Description',
        'featured_image': 'Featured Image',
        'author_id': 'Author'
    }
    
    form_overrides = {
        'content': TextAreaField,
        'excerpt': TextAreaField,
        'status': SelectField,
        'category': SelectField,
        'author': SelectField,
    }
    
    form_args = {
        'author': {
            'description': 'Select the blog post author'
        },
        'status': {
            'choices': [
                ('published', 'Published'),
                ('draft', 'Draft'),
                ('archived', 'Archived')
            ],
            'default': 'published',
            'description': 'Post status - Published posts are visible to all users'
        },
        'category': {
            'choices': [
                ('general', 'General'),
                ('news', 'News'),
                ('tips', 'Tips'),
                ('furniture', 'Furniture'),
                ('design', 'Design'),
                ('updates', 'Updates')
            ],
            'default': 'general',
            'description': 'Blog post category'
        },
        'featured_image': {
            'description': 'Upload an image or enter image URL'
        }
    }
    
    form_widget_args = {
        'content': {
            'rows': 15,
            'placeholder': 'Enter blog post content (supports HTML)'
        },
        'excerpt': {
            'rows': 3,
            'placeholder': 'Brief summary of the post (optional)'
        },
        'tags': {
            'placeholder': 'Enter tags separated by commas (e.g., furniture, design, tips)'
        },
        'featured_image': {
            'placeholder': 'Enter image URL or upload an image below'
        }
    }
    
    # Configure image upload
    form_extra_fields = {
        'upload_image': FileUploadField(
            'Upload Image',
            base_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads', 'blog'),
            relative_path='uploads/blog/',
            allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp']
        )
    }
    
    def scaffold_form(self):
        """Customize form"""
        form_class = super(BlogPostAdmin, self).scaffold_form()
        return form_class
    
    def on_model_change(self, form, model, is_created):
        """Generate slug, handle image upload, and set published date"""
        try:
            # Auto-set author to current user if not provided
            if not model.author_id:
                model.author_id = current_user.id
            
            # Handle image upload
            if hasattr(form, 'upload_image') and form.upload_image.data:
                # Create upload directory if it doesn't exist
                upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads', 'blog')
                os.makedirs(upload_dir, exist_ok=True)
                
                # Save the uploaded file
                file = form.upload_image.data
                filename = secure_filename(file.filename)
                # Add unique identifier to prevent overwrites
                name, ext = os.path.splitext(filename)
                unique_filename = f"{name}_{uuid.uuid4().hex[:8]}{ext}"
                
                file_path = os.path.join(upload_dir, unique_filename)
                file.save(file_path)
                
                # Set the featured_image to the relative URL
                model.featured_image = f"/static/uploads/blog/{unique_filename}"
            
            # Generate slug from title if not provided
            if not model.slug:
                model.slug = re.sub(r'[^\w\s-]', '', model.title.lower())
                model.slug = re.sub(r'[-\s]+', '-', model.slug).strip('-')
            
            # Set published date when status changes to published
            if model.status == 'published' and not model.published_at:
                model.published_at = datetime.utcnow()
            
            super(BlogPostAdmin, self).on_model_change(form, model, is_created)
            
        except Exception as e:
            flash(f'Error saving blog post: {str(e)}', 'error')
            raise


class BlogCategoryAdmin(SecureModelView):
    """Admin view for BlogCategory model"""
    
    column_list = ['id', 'name', 'slug', 'description', 'created_at']
    column_searchable_list = ['name', 'description']
    column_editable_list = ['name']
    
    form_excluded_columns = ['slug', 'created_at']
    
    def on_model_change(self, form, model, is_created):
        """Generate slug from name"""
        try:
            if not model.slug:
                model.slug = re.sub(r'[^\w\s-]', '', model.name.lower())
                model.slug = re.sub(r'[-\s]+', '-', model.slug).strip('-')
            
            super(BlogCategoryAdmin, self).on_model_change(form, model, is_created)
            
        except Exception as e:
            flash(f'Error saving category: {str(e)}', 'error')
            raise


class BlogCommentAdmin(SecureModelView):
    """Admin view for BlogComment model"""
    
    column_list = ['id', 'post', 'user', 'content', 'is_approved', 'created_at']
    column_searchable_list = ['content']
    column_filters = ['is_approved', 'created_at']
    column_editable_list = []
    column_default_sort = ('created_at', True)
    
    form_excluded_columns = ['created_at', 'updated_at']
    
    column_labels = {
        'is_approved': 'Approved',
        'created_at': 'Date'
    }
    
    column_formatters = {
        'content': lambda v, c, m, p: m.content[:100] + '...' if len(m.content) > 100 else m.content,
    }


def init_admin(app):
    """Initialize Flask-Admin with custom views"""
    
    admin = Admin(
        app,
        name=Markup('AM AWUNI<br><span style="color:#f59e0b;">FURNITURE &</span><br><span style="color:#f59e0b;">CONSTRUCTION</span>'),
        template_mode='bootstrap4',
        index_view=SecureAdminIndexView(name='Dashboard', url='/admin'),
        base_template='admin/custom_base.html'
    )
    
    # Add model views
    admin.add_view(UserAdmin(User, db.session, name='Users', category='User Management'))
    
    admin.add_view(ProductAdmin(Product, db.session, name='Products', category='Catalog'))
    admin.add_view(CategoryAdmin(Category, db.session, name='Categories', category='Catalog'))
    admin.add_view(ProductImageAdmin(ProductImage, db.session, name='Product Images', category='Catalog'))
    
    admin.add_view(OrderAdmin(Order, db.session, name='Orders', category='Sales'))
    admin.add_view(OrderItemAdmin(OrderItem, db.session, name='Order Items', category='Sales'))
    
    admin.add_view(ReviewAdmin(Review, db.session, name='Reviews', category='Content'))
    admin.add_view(WishlistAdmin(Wishlist, db.session, name='Wishlists', category='Content'))
    
    admin.add_view(BlogPostAdmin(BlogPost, db.session, name='Blog Posts', category='Blog'))
    admin.add_view(BlogCategoryAdmin(BlogCategory, db.session, name='Blog Categories', category='Blog'))
    admin.add_view(BlogCommentAdmin(BlogComment, db.session, name='Blog Comments', category='Blog'))
    
    return admin
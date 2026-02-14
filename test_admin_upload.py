#!/usr/bin/env python
"""Simulate admin form submission with image upload"""

from app import app
from admin import ProductAdmin
from flask import Flask
from models import db
from models.product import Product, Category
from werkzeug.datastructures import FileStorage
from io import BytesIO
import os

print("\n" + "="*70)
print("SIMULATING ADMIN FORM SUBMISSION WITH IMAGE")
print("="*70)

with app.app_context():
    try:
        # Create test category
        test_cat = Category.query.filter_by(name='Admin Test Category').first()
        if not test_cat:
            test_cat = Category(name='Admin Test Category', slug='admin-test-cat')
            db.session.add(test_cat)
            db.session.commit()
        
        print(f"\n[SETUP] Test category ready: {test_cat.name}")
        
        # Create a ProductAdmin instance
        admin = ProductAdmin(Product, db.session)
        print(f"[SETUP] ProductAdmin instance created")
        
        # Check form configuration
        print(f"\n[STEP 1] Checking form configuration...")
        print(f"  form_extra_fields keys: {list(admin.form_extra_fields.keys())}")
        
        # Create a test product
        test_product = Product(
            name='Admin Test Upload Product',
            slug='admin-test-upload-product',
            sku='ADMIN-TEST-001',
            description='Testing admin upload',
            price=299.99,
            stock_quantity=10,
            category_id=test_cat.id,
            is_active=True
        )
        
        print(f"\n[STEP 2] Created test product object")
        print(f"  Product ID before save: {test_product.id}")
        
        # Manually call _handle_image_management with a mock form
        class MockForm:
            def __init__(self):
                # Create a mock uploaded file
                file_content = b"<svg></svg>"  # Minimal SVG content
                self.upload_images = FileStorage(
                    stream=BytesIO(file_content),
                    filename="test_admin_upload.svg",
                    content_type="image/svg+xml"
                )
                # Also test as a list
                self.upload_images = [self.upload_images]
        
        mock_form = MockForm()
        print(f"\n[STEP 3] Created mock form with test image")
        print(f"  Mock image filename: {mock_form.upload_images[0].filename if mock_form.upload_images else 'None'}")
        
        # Call _handle_image_management
        print(f"\n[STEP 4] Calling _handle_image_management...")
        admin._handle_image_management(mock_form, test_product, is_created=True)
        
        # Check if pending images were set
        print(f"\n[STEP 5] Checking pending images...")
        if hasattr(test_product, '_pending_images'):
            print(f"  Pending images count: {len(test_product._pending_images)}")
            for img in test_product._pending_images:
                print(f"    - {img}")
        else:
            print(f"  No _pending_images attribute")
        
        # Save the product
        print(f"\n[STEP 6] Saving product...")
        db.session.add(test_product)
        db.session.commit()
        product_id = test_product.id
        print(f"  Product saved with ID: {product_id}")
        
        # Process pending images
        print(f"\n[STEP 7] Processing pending images...")
        admin._process_pending_images(test_product)
        
        # Check the result
        print(f"\n[STEP 8] Verifying product images...")
        from models.product import ProductImage
        images = ProductImage.query.filter_by(product_id=product_id).all()
        print(f"  ProductImages in DB: {len(images)}")
        for img in images:
            print(f"    - {img.image_url} (primary: {img.is_primary})")
        
        # Check main_image
        refreshed = Product.query.get(product_id)
        print(f"\n[STEP 9] Checking main_image property...")
        print(f"  main_image: {refreshed.main_image}")
        
        if refreshed.main_image == '/static/images/default-product.svg':
            print(f"  ✗ PROBLEM: main_image is still default SVG!")
        else:
            print(f"  ✓ SUCCESS: main_image shows uploaded image")
        
        print("\n" + "="*70)
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()

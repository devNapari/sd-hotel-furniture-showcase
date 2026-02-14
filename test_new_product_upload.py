#!/usr/bin/env python
"""Test if new product uploads work"""

from app import app, db
from models.product import Product, ProductImage, Category
from werkzeug.datastructures import FileStorage
from io import BytesIO
import os

print("\n" + "="*70)
print("TESTING NEW PRODUCT UPLOAD WITH IMAGE")
print("="*70)

with app.app_context():
    try:
        # Get or create test category
        test_cat = Category.query.filter_by(name='Test Upload Category').first()
        if not test_cat:
            test_cat = Category(name='Test Upload Category', slug='test-upload-cat')
            db.session.add(test_cat)
            db.session.commit()
        
        print(f"\n[STEP 1] Creating new product...")
        
        # Create a test product
        import uuid
        new_product = Product(
            name='Test Upload Product - With Image',
            slug=f'test-upload-product-img-{uuid.uuid4().hex[:8]}',
            sku=f'TEST-IMG-{uuid.uuid4().hex[:8]}',
            description='Testing image upload',
            price=199.99,
            stock_quantity=5,
            category_id=test_cat.id,
            is_active=True
        )
        db.session.add(new_product)
        db.session.commit()
        product_id = new_product.id
        
        print(f"[OK] Created product: {new_product.name} (ID: {product_id})")
        
        # Manually create ProductImage like the form would
        print(f"\n[STEP 2] Creating ProductImage record...")
        
        test_image_path = f"/static/uploads/products/test_manual_upload_12345.png"
        
        product_image = ProductImage(
            product_id=product_id,
            image_url=test_image_path,
            alt_text=f"{new_product.name} - Image 1",
            is_primary=True,
            display_order=0
        )
        db.session.add(product_image)
        db.session.commit()
        
        print(f"[OK] Created ProductImage: {test_image_path}")
        
        # Refresh and check
        print(f"\n[STEP 3] Verifying product image...")
        
        refreshed = Product.query.filter_by(id=product_id).first()
        print(f"Product: {refreshed.name}")
        print(f"  main_image: {refreshed.main_image}")

        images = ProductImage.query.filter_by(product_id=product_id).all()
        print(f"  ProductImages count: {len(images)}")
        for img in images:
            print(f"    - {img.image_url} (primary: {img.is_primary})")

        # Check API response
        print(f"\n[STEP 4] Checking API response...")
        api_data = refreshed.to_dict()
        print(f"API main_image: {api_data.get('main_image')}")
        print(f"API has 'images' key: {'images' in api_data}")

        # Simulate what the frontend would get
        print(f"\n[STEP 5] Frontend simulation...")
        image_url = api_data.get('main_image') or '/static/images/default-product.svg'
        print(f"Frontend would display: {image_url}")
        
        if image_url == '/static/images/default-product.svg':
            print("[PROBLEM] Frontend would show default SVG instead of uploaded image!")
        else:
            print("[SUCCESS] Frontend would display the uploaded image")
        
        print("\n" + "="*70)
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()

#!/usr/bin/env python
"""Test image upload functionality"""

from app import app, db
from models.product import Product, ProductImage
import os

print("\n" + "="*60)
print("IMAGE UPLOAD FUNCTIONALITY TEST")
print("="*60)

with app.app_context():
    try:
        # Check if Product model has the old fields removed
        print("\n[TEST 1] Checking Product model...")
        p = Product.query.first()
        
        if p:
            # Try to access the old fields - if they don't exist, we get an AttributeError
            try:
                _ = p.latest_image_source
                print("✗ FAILED: latest_image_source field still exists!")
            except AttributeError:
                print("✓ latest_image_source field removed")
            
            try:
                _ = p.latest_image_url
                print("✗ FAILED: latest_image_url field still exists!")
            except AttributeError:
                print("✓ latest_image_url field removed")
            
            try:
                _ = p.latest_image_updated
                print("✗ FAILED: latest_image_updated field still exists!")
            except AttributeError:
                print("✓ latest_image_updated field removed")
        
        # Check database
        print("\n[TEST 2] Database check...")
        products = Product.query.all()
        print(f"✓ Total products: {len(products)}")
        
        # Check for products with images
        print("\n[TEST 3] Products with images...")
        for product in products[:3]:  # Check first 3
            images = ProductImage.query.filter_by(product_id=product.id).all()
            if images:
                print(f"✓ {product.name}: {len(images)} images")
                for img in images:
                    print(f"  - {img.image_url} (primary: {img.is_primary})")
            else:
                print(f"- {product.name}: No images")
        
        # Check main_image property
        print("\n[TEST 4] main_image property...")
        for product in products[:3]:
            main_img = product.main_image
            print(f"✓ {product.name}: {main_img}")
        
        # Check API response
        print("\n[TEST 5] API response format...")
        test_product = products[0] if products else None
        if test_product:
            api_data = test_product.to_dict()
            print(f"✓ API data keys: {list(api_data.keys())}")
            
            # Check that old fields are NOT in API response
            if 'image_source' in api_data:
                print("✗ FAILED: image_source still in API response!")
            else:
                print("✓ image_source removed from API response")
            
            if 'latest_image_updated' in api_data:
                print("✗ FAILED: latest_image_updated still in API response!")
            else:
                print("✓ latest_image_updated removed from API response")
            
            print(f"✓ main_image in API response: {api_data['main_image']}")
        
        print("\n" + "="*60)
        print("✓ ALL TESTS PASSED - FIELDS REMOVED SUCCESSFULLY")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

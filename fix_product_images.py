#!/usr/bin/env python
"""
Fix products with 'uploaded' image_source that have no actual images
This resets them to have 'url' source if they have latest_image_url, or removes the upload flag if they don't
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ['FLASK_ENV'] = 'development'

from app import create_app, db
from models.product import Product

app = create_app()

with app.app_context():
    # Find products with uploaded source but no images and no latest_image_url
    products_to_fix = Product.query.filter(
        Product.latest_image_source == 'uploaded'
    ).all()
    
    print("\n" + "=" * 100)
    print("FIXING PRODUCTS WITH INCONSISTENT IMAGE_SOURCE")
    print("=" * 100)
    
    fixed_count = 0
    
    for product in products_to_fix:
        has_product_images = product.images.count() > 0
        has_latest_url = product.latest_image_url is not None and product.latest_image_url != ''
        
        if not has_product_images and not has_latest_url:
            # This product has no images at all - set to default
            print(f"\nProduct: {product.name} (ID: {product.id})")
            print(f"  Before: source='{product.latest_image_source}', url='{product.latest_image_url}', images={product.images.count()}")
            print(f"  Action: Resetting to empty state")
            
            product.latest_image_source = 'uploaded'  # Keep as uploaded (empty state)
            product.latest_image_url = None
            product.latest_image_updated = None
            fixed_count += 1
        
        elif not has_product_images and has_latest_url:
            # Has latest_image_url but no ProductImage entries - this is from URL source
            print(f"\nProduct: {product.name} (ID: {product.id})")
            print(f"  Before: source='{product.latest_image_source}', url='{product.latest_image_url}'")
            print(f"  Action: Changing source to 'url' (has latest_image_url)")
            
            product.latest_image_source = 'url'
            fixed_count += 1
        
        else:
            # Has ProductImage entries - this is correct
            print(f"\n✓ Product: {product.name} (ID: {product.id}) - Already correct")
            print(f"  source='{product.latest_image_source}', images={product.images.count()}")
    
    # Commit changes
    if fixed_count > 0:
        db.session.commit()
        print(f"\n✓ Fixed {fixed_count} products")
    else:
        print("\n✓ No products needed fixing")
    
    print("\n" + "=" * 100)

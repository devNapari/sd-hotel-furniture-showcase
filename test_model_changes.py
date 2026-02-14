#!/usr/bin/env python
"""
Simple test to verify the model changes are working
"""
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Flask app
os.environ['FLASK_ENV'] = 'development'

from app import create_app, db
from models.product import Product, ProductImage

app = create_app()

with app.app_context():
    # Get first 5 products
    products = Product.query.limit(5).all()
    
    print("\n" + "=" * 80)
    print("PRODUCT IMAGE CONFIGURATION TEST")
    print("=" * 80)
    
    for product in products:
        print(f"\nProduct: {product.name}")
        print(f"  ID: {product.id}")
        print(f"  Latest Image Source: {product.latest_image_source}")
        print(f"  Latest Image URL: {product.latest_image_url}")
        print(f"  Main Image (from property): {product.main_image}")
        
        # Check images in ProductImage table
        images = product.images.all()
        print(f"  Images in ProductImage table: {len(images)}")
        for img in images:
            print(f"    - {img.image_url} (primary: {img.is_primary})")
        
        # Verify the main_image property logic
        if images:
            primary = product.images.filter_by(is_primary=True).first()
            if primary:
                print(f"  ✓ Has primary image in table: {primary.image_url}")
            else:
                first = product.images.first()
                if first:
                    print(f"  ✓ Has first image in table: {first.image_url}")
    
    print("\n" + "=" * 80)

#!/usr/bin/env python
"""
Check which products have uploaded images
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ['FLASK_ENV'] = 'development'

from app import create_app, db
from models.product import Product, ProductImage

app = create_app()

with app.app_context():
    # Find products with uploaded images
    products_with_uploads = []
    
    all_products = Product.query.all()
    
    for product in all_products:
        for img in product.images.all():
            if img.image_url.startswith('/static/uploads/products/'):
                products_with_uploads.append({
                    'product': product.name,
                    'product_id': product.id,
                    'image_url': img.image_url,
                    'is_primary': img.is_primary,
                    'latest_source': product.latest_image_source,
                    'latest_url': product.latest_image_url,
                    'main_image': product.main_image
                })
    
    print("\n" + "=" * 100)
    print("PRODUCTS WITH UPLOADED IMAGES")
    print("=" * 100)
    
    if products_with_uploads:
        print(f"\nFound {len(products_with_uploads)} images in ProductImage table")
        for item in products_with_uploads:
            print(f"\nProduct: {item['product']} (ID: {item['product_id']})")
            print(f"  Image URL in Table: {item['image_url']}")
            print(f"  Is Primary: {item['is_primary']}")
            print(f"  Latest Source: {item['latest_source']}")
            print(f"  Latest URL: {item['latest_url']}")
            print(f"  Main Image (property): {item['main_image']}")
    else:
        print("\nNo products with uploaded images found")
        print("\nProducts with images in ProductImage table:")
        for product in Product.query.all():
            if product.images.count() > 0:
                for img in product.images.all():
                    print(f"  {product.name}: {img.image_url}")
    
    print("\n" + "=" * 100)

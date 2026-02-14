#!/usr/bin/env python
"""Debug product images"""
from app import create_app
from models import db
from models.product import Product, ProductImage

app = create_app()
with app.app_context():
    print("Checking product images...\n")
    
    # Check products with images
    products = Product.query.all()
    print(f"Total products: {len(products)}")
    
    print("\nProducts and their images:")
    for p in products[-10:]:  # Last 10 products
        images = ProductImage.query.filter_by(product_id=p.id).all()
        print(f"\nProduct ID {p.id}: {p.name}")
        print(f"  Slug: {p.slug}")
        print(f"  latest_image_url: {p.latest_image_url}")
        print(f"  latest_image_source: {p.latest_image_source}")
        print(f"  Images count: {len(images)}")
        if images:
            for img in images:
                print(f"    - {img.image_url} (primary: {img.is_primary})")
        else:
            print(f"    - NO IMAGES")

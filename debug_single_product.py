#!/usr/bin/env python
"""Debug specific product to see why image might be broken"""
from app import create_app
from models import db
from models.product import Product

app = create_app()
with app.app_context():
    # Get a newly added product (ID 17 or higher)
    product = Product.query.filter_by(id=17).first()
    
    if product:
        print(f"Product: {product.name}")
        print(f"ID: {product.id}")
        print(f"latest_image_source: {product.latest_image_source}")
        print(f"latest_image_url: {product.latest_image_url}")
        print(f"images count: {product.images.count()}")
        print(f"is_active: {product.is_active}")
        print(f"category_id: {product.category_id}")
        print()
        
        # Test the main_image property
        print(f"main_image property value:")
        try:
            img = product.main_image
            print(f"  {img}")
        except Exception as e:
            print(f"  ERROR: {e}")
        
        print()
        
        # Test the to_dict method
        print(f"to_dict() response:")
        try:
            d = product.to_dict()
            print(f"  main_image: {d.get('main_image')}")
            print(f"  image_source: {d.get('image_source')}")
        except Exception as e:
            print(f"  ERROR: {e}")
    else:
        print("Product not found")

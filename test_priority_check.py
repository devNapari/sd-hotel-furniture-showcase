#!/usr/bin/env python
"""Test image priority for different product types"""
from app import create_app
from models.product import Product

app = create_app()
with app.app_context():
    # Test 1: Product with ProductImage
    p1 = Product.query.filter_by(id=1).first()
    print('Product 1 (Luxury King Bed Frame):')
    print(f'  ProductImages: {p1.images.count()}')
    print(f'  latest_image_source: {p1.latest_image_source}')
    print(f'  main_image: {p1.main_image}')
    print()
    
    # Test 2: Product with URL 
    p2 = Product.query.filter_by(id=12).first()
    print('Product 12 (New Sofa Bed):')
    print(f'  ProductImages: {p2.images.count()}')
    print(f'  latest_image_source: {p2.latest_image_source}')
    print(f'  main_image: {p2.main_image}')
    print()
    
    # Test 3: No images
    p3 = Product.query.filter_by(id=17).first()
    print('Product 17 (Adams Amina):')
    print(f'  ProductImages: {p3.images.count()}')
    print(f'  latest_image_source: {p3.latest_image_source}')
    print(f'  main_image: {p3.main_image}')

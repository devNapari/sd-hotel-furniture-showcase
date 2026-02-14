#!/usr/bin/env python
"""
Test the complete API flow for uploaded images
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ['FLASK_ENV'] = 'development'

from app import create_app

app = create_app()

# Create a test client
client = app.test_client()

# Test the API
response = client.get('/api/products?per_page=100')
data = response.get_json()

if data['status'] == 'success':
    print("\n" + "=" * 100)
    print("API RESPONSE CHECK - UPLOADED IMAGES")
    print("=" * 100)
    
    products = data['products']
    uploaded_products = [p for p in products if p.get('image_source') == 'uploaded' or 
                         (p.get('main_image') and '/static/uploads/products/' in p.get('main_image', ''))]
    
    print(f"\nTotal products: {len(products)}")
    print(f"Products with uploaded images: {len(uploaded_products)}")
    
    for product in uploaded_products:
        print(f"\n✓ Product: {product['name']} (ID: {product['id']})")
        print(f"  Main Image: {product.get('main_image')}")
        print(f"  Image Source: {product.get('image_source')}")
        print(f"  Latest URL: {product.get('latest_image_url')}")
        print(f"  Status: {'✓ READY TO DISPLAY' if product.get('main_image') else '✗ NO IMAGE'}")
    
    # Check if all products have main_image
    no_image = [p for p in products if not p.get('main_image')]
    if no_image:
        print(f"\n⚠ {len(no_image)} products have no main_image")
    
    print("\n" + "=" * 100)
else:
    print(f"Error: {data.get('message')}")

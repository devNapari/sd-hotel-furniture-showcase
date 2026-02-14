#!/usr/bin/env python
"""Test complete API flow exactly as browser would"""
import json
from app import create_app

app = create_app()
with app.test_client() as client:
    response = client.get('/api/products?per_page=100')
    data = response.get_json()
    
    print("API Response Structure Check:")
    print(f"Status Code: {response.status_code}")
    print(f"Response Keys: {list(data.keys())}")
    print(f"data['status']: {data.get('status')}")
    print(f"Type of data['products']: {type(data.get('products'))}")
    print(f"Number of products: {len(data.get('products', []))}")
    
    # Simulate the condition in shop.js
    if data.get('status') == 'success':
        print("\n✓ shop.js condition (data.status === 'success') is TRUE")
        print(f"✓ shop.js will use API data with {len(data['products'])} products")
    else:
        print("\n✗ shop.js condition (data.status === 'success') is FALSE")
        print("✗ shop.js will fall back to SHOP_PRODUCTS (static data)")

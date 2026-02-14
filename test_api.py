#!/usr/bin/env python
"""Test the API endpoint directly"""
import json
from app import create_app

app = create_app()
with app.test_client() as client:
    # Test API endpoint
    response = client.get('/api/products')
    data = response.get_json()
    
    print(f"API Response Status: {response.status_code}")
    print(f"API Response Status field: {data.get('status')}")
    print(f"Total products returned by API: {len(data.get('products', []))}")
    
    if data.get('products'):
        print("\nFirst 5 products from API:")
        for p in data['products'][:5]:
            print(f"  ID: {p.get('id')}, Name: {p.get('name')}, Slug: {p.get('slug')}, Price: {p.get('price')}")
        
        print("\nLast 5 products from API:")
        for p in data['products'][-5:]:
            print(f"  ID: {p.get('id')}, Name: {p.get('name')}, Slug: {p.get('slug')}, Price: {p.get('price')}")
    else:
        print("\nNo products returned!")
        print(f"Full response: {json.dumps(data, indent=2)}")

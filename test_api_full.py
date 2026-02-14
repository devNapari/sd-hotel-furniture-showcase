#!/usr/bin/env python
"""Test the API endpoint with per_page=100"""
import json
from app import create_app

app = create_app()
with app.test_client() as client:
    # Test API endpoint with per_page=100
    response = client.get('/api/products?per_page=100')
    data = response.get_json()
    
    print(f"API Response Status: {response.status_code}")
    print(f"API Response Status field: {data.get('status')}")
    print(f"Total products returned by API (per_page=100): {len(data.get('products', []))}")
    
    if data.get('products'):
        print("\nAll returned products:")
        for i, p in enumerate(data['products'], 1):
            print(f"  {i}. ID: {p.get('id')}, Name: {p.get('name')}, is_active: {p.get('is_active', 'N/A')}")
    else:
        print("\nNo products returned!")
        print(f"Full response: {json.dumps(data, indent=2)}")

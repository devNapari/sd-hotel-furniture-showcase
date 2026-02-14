#!/usr/bin/env python
"""Check raw API response for newly added products"""
import json
from app import create_app

app = create_app()
with app.test_client() as client:
    response = client.get('/api/products?per_page=100')
    data = response.get_json()
    
    print("Checking if main_image field is in API response:\n")
    
    # Check last product
    if data['products']:
        p = data['products'][-1]
        print(f"Last Product ID: {p.get('id')}")
        print(f"Name: {p.get('name')}")
        print(f"\nAll fields in product object:")
        for key in sorted(p.keys()):
            value = p[key]
            if isinstance(value, str) and len(value) > 80:
                print(f"  {key}: {value[:80]}...")
            else:
                print(f"  {key}: {value}")

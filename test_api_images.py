#!/usr/bin/env python
"""Test what the API returns for product images"""
import json
from app import create_app

app = create_app()
with app.test_client() as client:
    response = client.get('/api/products?per_page=100')
    data = response.get_json()
    
    print("Products returned by API (checking main_image):\n")
    for p in data['products'][-10:]:  # Last 10
        print(f"ID: {p.get('id')}, Name: {p.get('name')}")
        print(f"  main_image: {p.get('main_image')}")
        print(f"  image_source: {p.get('image_source')}")
        print()

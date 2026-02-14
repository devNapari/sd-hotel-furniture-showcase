"""
Simulate the actual cart that would be sent from the browser
using real products from the database
"""
import sys
sys.path.insert(0, r'c:\Users\zoe\Downloads\New folder\New folder\sd-hotel-furniture-showcase')

from app import app, db
from models.product import Product
import requests
import json
from datetime import datetime, timedelta

with app.app_context():
    # Get actual products that would appear in cart
    products = Product.query.filter_by(is_active=True).limit(3).all()
    
    # Build cart items like JavaScript would
    cart_items = []
    for product in products:
        cart_item = {
            "id": product.id,
            "name": product.name,
            "price": float(product.price),
            "image": product.main_image,  # This is what to_dict() returns
            "quantity": 1
        }
        cart_items.append(cart_item)
        print(f"Added to cart: {product.name}")
        print(f"  - ID: {product.id}")
        print(f"  - Price: ${product.price}")
        print(f"  - Image: {product.main_image}")
        print()
    
    # Now simulate the form submission
    consultation_data = {
        "firstName": "Test",
        "lastName": "User",
        "email": "test@example.com",
        "phone": "+1234567890",
        "company": "Test Company",
        "subject": "Test with Real Products",
        "message": "I would like more information about these products.",
        "preferredDate": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
        "preferredTime": "14:00",
        "newsletter": False,
        "cartItems": cart_items
    }
    
    print("=" * 80)
    print("SENDING CONSULTATION WITH REAL PRODUCTS:")
    print("=" * 80)
    print(json.dumps(consultation_data, indent=2))
    print("=" * 80)
    
    response = requests.post(
        'http://127.0.0.1:5000/api/consultation',
        json=consultation_data,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"\nResponse Status: {response.status_code}")
    print(f"Response: {response.json()}")

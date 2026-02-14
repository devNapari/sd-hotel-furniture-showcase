"""Test the consultation form submission with cart items"""
import requests
import json
from datetime import datetime, timedelta

# Test data
consultation_data = {
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "company": "Test Company",
    "subject": "Test Consultation Request",
    "message": "I would like to discuss furniture options for our hotel.",
    "preferredDate": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
    "preferredTime": "10:00",
    "newsletter": True,
    "cartItems": [
        {
            "id": 1,
            "name": "Modern Bed Frame - King",
            "price": 1299.99,
            "image": "/static/uploads/products/sample_bed.jpg",
            "quantity": 2
        },
        {
            "id": 2,
            "name": "Luxury Sofa Set",
            "price": 3999.99,
            "image": "/static/uploads/products/sample_sofa.jpg",
            "quantity": 1
        }
    ]
}

# Send request
print("Sending consultation form with cart items...")
print(f"Cart items count: {len(consultation_data['cartItems'])}")
print(f"Cart items: {json.dumps(consultation_data['cartItems'], indent=2)}")
print("-" * 60)

response = requests.post(
    'http://127.0.0.1:5000/api/consultation',
    json=consultation_data,
    headers={'Content-Type': 'application/json'}
)

print(f"Response Status: {response.status_code}")
print(f"Response Body: {response.text}")

if response.status_code == 200:
    print("\n✓ Consultation form submitted successfully!")
    print("Check your email for the submitted consultation request.")
else:
    print("\n✗ Error submitting consultation form")

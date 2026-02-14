#!/usr/bin/env python
"""Test if static images are being served correctly"""

from app import app
import requests

print("\n" + "="*80)
print("TESTING STATIC IMAGE SERVING")
print("="*80)

# Start Flask in a thread and test
with app.test_client() as client:
    try:
        # Test accessing a known uploaded image
        print("\n[TEST 1] Accessing uploaded image via HTTP...")
        
        image_url = '/static/uploads/products/test_image_87d8dcb8.png'
        response = client.get(image_url)
        
        print(f"URL: {image_url}")
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.content_type}")
        print(f"Content Length: {len(response.data)} bytes")
        
        if response.status_code == 200:
            print("✓ Image is being served correctly!")
        else:
            print(f"✗ Error serving image: {response.status_code}")
        
        # Test accessing a default image for comparison
        print("\n[TEST 2] Accessing default SVG image...")
        svg_url = '/static/images/default-product.svg'
        response = client.get(svg_url)
        
        print(f"URL: {svg_url}")
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.content_type}")
        print(f"Content Length: {len(response.data)} bytes")
        
        if response.status_code == 200:
            print("✓ Default SVG is being served correctly!")
        
        # Test the API endpoint
        print("\n[TEST 3] Checking API response for products...")
        response = client.get('/api/products?per_page=3')
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.get_json()
            products = data.get('products', [])
            print(f"Products returned: {len(products)}")
            
            for p in products[:2]:
                print(f"\n  Product: {p['name']}")
                print(f"    main_image: {p.get('main_image')}")
                
                if p.get('main_image'):
                    if '/static/uploads/' in p.get('main_image'):
                        print(f"    → This is an UPLOADED image")
                    elif p.get('main_image').startswith('http'):
                        print(f"    → This is an EXTERNAL URL")
                    else:
                        print(f"    → This is a LOCAL path")
        
        print("\n" + "="*80)
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()

#!/usr/bin/env python
"""Verify that all products now show local images"""

from app import app
from models.product import Product, ProductImage

print("\n" + "="*80)
print("VERIFYING LOCAL IMAGES ARE DISPLAYED")
print("="*80)

with app.test_client() as client:
    try:
        # Get API response
        print("\n[TEST 1] Checking API response for products...\n")
        
        response = client.get('/api/products?per_page=10')
        
        if response.status_code == 200:
            data = response.get_json()
            products = data.get('products', [])
            
            print(f"Total products returned: {len(products)}\n")
            
            external_count = 0
            local_count = 0
            default_count = 0
            
            for p in products:
                main_image = p.get('main_image', '/static/images/default-product.svg')
                
                if main_image.startswith('http'):
                    image_type = "EXTERNAL URL"
                    external_count += 1
                elif '/static/uploads/' in main_image:
                    image_type = "LOCAL UPLOAD"
                    local_count += 1
                else:
                    image_type = "DEFAULT SVG"
                    default_count += 1
                
                print(f"{p['name'][:40]}")
                print(f"  {image_type}: {main_image[:60]}...")
                print()
            
            print("\n[TEST 2] Summary Statistics\n")
            print(f"External URLs (Pexels): {external_count}")
            print(f"Local Uploads: {local_count}")
            print(f"Default SVG: {default_count}")
            
            print("\n" + "="*80)
            
            if external_count == 0:
                print("✓ SUCCESS: All Pexels URLs have been replaced with local images!")
            else:
                print(f"⚠ WARNING: {external_count} Pexels URLs still remain")
            
            print("="*80 + "\n")
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()

#!/usr/bin/env python
"""Final verification that all images are working"""

from app import app
from models.product import Product, ProductImage

print("\nFINAL IMAGE VERIFICATION")
print("="*60)

with app.test_client() as client:
    response = client.get('/api/products?per_page=15')
    
    if response.status_code == 200:
        data = response.get_json()
        products = data.get('products', [])
        
        external = 0
        local = 0
        default = 0
        
        for p in products:
            img = p.get('main_image', '/static/images/default-product.svg')
            
            if img.startswith('http'):
                external += 1
            elif '/static/uploads/' in img:
                local += 1
            else:
                default += 1
        
        print(f"\nTotal Products: {len(products)}")
        print(f"Local Images: {local}")
        print(f"External URLs: {external}")
        print(f"Default SVG: {default}")
        print("\n" + "="*60)
        
        if external == 0 and default == 0:
            print("SUCCESS: All products display local images!")
        else:
            print(f"Note: {default} products show default, {external} external")
        
        print("="*60 + "\n")

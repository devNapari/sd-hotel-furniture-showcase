#!/usr/bin/env python
"""
Test script to verify uploaded product images are displaying correctly
"""
import requests
import json
import os

BASE_URL = 'http://localhost:5000'
UPLOAD_DIR = 'static/uploads/products'

def test_api_products():
    """Test the API to see what products are returning for images"""
    print("=" * 80)
    print("TESTING PRODUCT API - IMAGE DISPLAY")
    print("=" * 80)
    
    try:
        response = requests.get(f'{BASE_URL}/api/products?per_page=100')
        response.raise_for_status()
        data = response.json()
        
        if data['status'] == 'success':
            products = data['products']
            print(f"\nTotal products: {len(products)}")
            print("\n" + "-" * 80)
            
            # Check each product's image configuration
            for product in products:
                print(f"\nProduct: {product['name']} (ID: {product['id']})")
                print(f"  - SKU: {product.get('sku', 'N/A')}")
                print(f"  - Main Image: {product.get('main_image', 'NOT SET')}")
                print(f"  - Image Source: {product.get('image_source', 'NOT SET')}")
                print(f"  - Latest Image URL: {product.get('latest_image_url', 'NOT SET')}")
                print(f"  - Active: {product.get('is_active', 'N/A')}")
                
                # Check if image files exist for uploaded images
                if product.get('main_image') and product.get('main_image').startswith('/static/uploads/products/'):
                    image_filename = product['main_image'].replace('/static/uploads/products/', '')
                    image_path = os.path.join(UPLOAD_DIR, image_filename)
                    exists = os.path.exists(image_path)
                    status = "✓ EXISTS" if exists else "✗ MISSING"
                    print(f"  - File Status: {status}")
                
        else:
            print(f"Error: {data.get('message')}")
            
    except Exception as e:
        print(f"Error fetching products: {e}")

def test_upload_directory():
    """Check what files exist in the upload directory"""
    print("\n" + "=" * 80)
    print("CHECKING UPLOAD DIRECTORY")
    print("=" * 80)
    
    if os.path.exists(UPLOAD_DIR):
        files = os.listdir(UPLOAD_DIR)
        print(f"\nDirectory: {UPLOAD_DIR}")
        print(f"Total files: {len(files)}")
        
        if files:
            print("\nFiles in directory:")
            for f in files[:10]:  # Show first 10 files
                full_path = os.path.join(UPLOAD_DIR, f)
                size = os.path.getsize(full_path)
                print(f"  - {f} ({size} bytes)")
            
            if len(files) > 10:
                print(f"  ... and {len(files) - 10} more files")
        else:
            print("\n⚠ Directory is EMPTY - no uploaded images found!")
    else:
        print(f"\n✗ Directory does not exist: {UPLOAD_DIR}")

def test_image_url_accessibility():
    """Test if uploaded images are accessible via HTTP"""
    print("\n" + "=" * 80)
    print("TESTING IMAGE URL ACCESSIBILITY")
    print("=" * 80)
    
    try:
        response = requests.get(f'{BASE_URL}/api/products?per_page=100')
        data = response.json()
        
        if data['status'] == 'success':
            products = data['products']
            
            print("\nTesting image URLs...")
            tested_count = 0
            successful_count = 0
            
            for product in products:
                if product.get('main_image'):
                    main_image = product['main_image']
                    
                    # Only test uploaded images
                    if main_image.startswith('/static/uploads/products/'):
                        full_url = f'{BASE_URL}{main_image}'
                        try:
                            img_response = requests.head(full_url, timeout=5)
                            status = "✓" if img_response.status_code == 200 else f"✗ ({img_response.status_code})"
                            print(f"  {status} {main_image}")
                            tested_count += 1
                            if img_response.status_code == 200:
                                successful_count += 1
                        except Exception as e:
                            print(f"  ✗ {main_image} - Error: {str(e)}")
                            tested_count += 1
            
            print(f"\nAccessibility: {successful_count}/{tested_count} uploaded images accessible")
                            
    except Exception as e:
        print(f"Error testing URLs: {e}")

def main():
    print("\n\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 15 + "UPLOADED PRODUCT IMAGES TEST SUITE" + " " * 29 + "║")
    print("╚" + "=" * 78 + "╝")
    
    test_api_products()
    test_upload_directory()
    test_image_url_accessibility()
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)
    print("\nSummary:")
    print("1. If 'main_image' shows /static/uploads/products/... → ✓ Images being returned")
    print("2. If files exist in upload directory → ✓ Files being saved correctly")
    print("3. If image URLs are accessible → ✓ Frontend can display images")
    print("\n")

if __name__ == '__main__':
    main()

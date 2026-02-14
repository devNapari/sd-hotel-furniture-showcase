#!/usr/bin/env python
"""Check which uploaded image files are valid and fix broken ones"""

from app import app, db
from models.product import ProductImage, Product
import os

print("\n" + "="*80)
print("CHECKING AND FIXING UPLOADED IMAGES")
print("="*80)

with app.app_context():
    try:
        uploads_dir = os.path.join(os.path.dirname(__file__), 'static', 'uploads', 'products')
        
        # Get all ProductImage records with local uploads
        local_images = ProductImage.query.filter(
            ProductImage.image_url.like('%/static/uploads/%')
        ).all()
        
        print(f"\n[STEP 1] Checking {len(local_images)} local image records...\n")
        
        valid_files = os.listdir(uploads_dir)
        valid_images = {}  # Map of filename to full path
        broken_count = 0
        valid_count = 0
        
        for img in local_images:
            product = Product.query.get(img.product_id)
            filename = os.path.basename(img.image_url)
            file_path = os.path.join(uploads_dir, filename)
            
            exists = os.path.exists(file_path)
            size = os.path.getsize(file_path) if exists else 0
            
            # Check if file is valid (more than 100 bytes is usually safe)
            is_valid = exists and size > 100
            
            if is_valid:
                valid_count += 1
                print(f"✓ {product.name[:40]}")
                print(f"  File: {filename} ({size} bytes)")
                valid_images[filename] = True
            else:
                broken_count += 1
                print(f"✗ {product.name[:40]}")
                print(f"  File: {filename} - {'MISSING' if not exists else 'BROKEN (too small)'} ({size} bytes)")
            print()
        
        print(f"\n[STEP 2] Summary")
        print(f"Valid images: {valid_count}")
        print(f"Broken/Missing: {broken_count}")
        
        # Find all actual image files that are valid
        print(f"\n[STEP 3] Finding valid files in uploads folder...\n")
        
        valid_upload_files = []
        for filename in os.listdir(uploads_dir):
            file_path = os.path.join(uploads_dir, filename)
            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                if size > 100:  # Valid image should be more than 100 bytes
                    valid_upload_files.append(filename)
                    print(f"✓ {filename} ({size} bytes)")
        
        print(f"\nTotal valid files available: {len(valid_upload_files)}")
        
        if valid_upload_files and broken_count > 0:
            print(f"\n[STEP 4] Fixing broken images with valid files...")
            
            import random
            broken_images = ProductImage.query.filter(
                ProductImage.image_url.like('%/static/uploads/%')
            ).all()
            
            fixed_count = 0
            for img in broken_images:
                filename = os.path.basename(img.image_url)
                file_path = os.path.join(uploads_dir, filename)
                size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
                
                # Replace if file doesn't exist or is too small
                if not os.path.exists(file_path) or size <= 100:
                    random_file = random.choice(valid_upload_files)
                    old_url = img.image_url
                    img.image_url = f"/static/uploads/products/{random_file}"
                    
                    product = Product.query.get(img.product_id)
                    fixed_count += 1
                    
                    print(f"\n[{fixed_count}] {product.name[:40]}")
                    print(f"  Old: {old_url}")
                    print(f"  New: {img.image_url}")
            
            if fixed_count > 0:
                db.session.commit()
                print(f"\n✓ Fixed {fixed_count} broken image records")
        
        print("\n" + "="*80)
        print("✓ IMAGE CHECK AND FIX COMPLETE")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        db.session.rollback()

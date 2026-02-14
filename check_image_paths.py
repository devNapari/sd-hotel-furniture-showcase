#!/usr/bin/env python
"""Check what image paths are in database vs what files exist on disk"""

from app import app, db
from models.product import Product, ProductImage
import os

print("\n" + "="*80)
print("CHECKING IMAGE PATHS: DATABASE vs DISK")
print("="*80)

with app.app_context():
    try:
        # Get all ProductImage records
        all_images = ProductImage.query.all()
        print(f"\n[STEP 1] ProductImage records in database: {len(all_images)}")
        
        # Check uploaded images specifically
        uploaded_images = ProductImage.query.filter(ProductImage.image_url.like('%/static/uploads/%')).all()
        print(f"[STEP 2] Uploaded images (in /static/uploads/): {len(uploaded_images)}")
        
        if uploaded_images:
            print("\n[STEP 3] Checking if uploaded image files exist on disk:\n")
            
            for img in uploaded_images[:5]:  # Check first 5
                product = Product.query.get(img.product_id)
                image_url = img.image_url
                
                # Convert URL to file path
                # URL is like: /static/uploads/products/filename.png
                # We need to convert to: {project_root}/static/uploads/products/filename.png
                
                file_path = image_url.replace('/static/', '')  # Remove /static/
                full_path = os.path.join(os.path.dirname(__file__), 'static', file_path)
                
                file_exists = os.path.exists(full_path)
                file_size = os.path.getsize(full_path) if file_exists else 0
                
                print(f"Product: {product.name}")
                print(f"  URL in DB:    {image_url}")
                print(f"  File path:    {full_path}")
                print(f"  File exists:  {'YES' if file_exists else 'NO'}")
                if file_exists:
                    print(f"  File size:    {file_size} bytes")
                print()
        
        # List what's actually in the uploads directory
        print("[STEP 4] Files actually in /static/uploads/products/:\n")
        upload_dir = os.path.join(os.path.dirname(__file__), 'static', 'uploads', 'products')
        
        if os.path.exists(upload_dir):
            files = os.listdir(upload_dir)
            print(f"Total files: {len(files)}")
            for f in files[:10]:
                file_path = os.path.join(upload_dir, f)
                size = os.path.getsize(file_path)
                print(f"  {f} ({size} bytes)")
        else:
            print(f"  ERROR: Directory doesn't exist: {upload_dir}")
        
        # Check a product's main_image
        print("\n[STEP 5] Checking Product.main_image property:\n")
        products_with_uploads = db.session.query(Product).join(ProductImage).filter(
            ProductImage.image_url.like('%/static/uploads/%')
        ).all()
        
        for p in products_with_uploads[:3]:
            print(f"Product: {p.name}")
            print(f"  main_image: {p.main_image}")
            images = ProductImage.query.filter_by(product_id=p.id).all()
            for img in images:
                print(f"  ProductImage: {img.image_url} (primary: {img.is_primary})")
            print()
        
        print("="*80)
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()

#!/usr/bin/env python
"""Debug why uploaded images aren't displaying"""

from app import app, db
from models.product import Product, ProductImage
import os

print("\n" + "="*70)
print("DEBUGGING UPLOADED IMAGE DISPLAY ISSUE")
print("="*70)

with app.app_context():
    try:
        # Get all products
        products = Product.query.all()
        print(f"\n[STEP 1] Total Products in Database: {len(products)}")
        
        # Check each product
        print("\n[STEP 2] Checking products and their images...\n")
        
        for p in products[:10]:  # Check first 10
            print(f"Product: {p.name} (ID: {p.id})")
            print(f"  main_image property: {p.main_image}")

            # Check ProductImage table directly
            images = ProductImage.query.filter_by(product_id=p.id).all()
            print(f"  ProductImages in DB: {len(images)}")

            if images:
                for idx, img in enumerate(images):
                    print(f"    [{idx}] URL: {img.image_url}")
                    print(f"        is_primary: {img.is_primary}")
                    print(f"        display_order: {img.display_order}")

                    # Check if file exists
                    if '/static/uploads/' in img.image_url:
                        file_path = img.image_url.replace('/static/', '')
                        full_path = os.path.join(os.path.dirname(__file__), 'static', file_path.replace('uploads/', 'uploads/'))
                        exists = os.path.exists(full_path)
                        print(f"        file exists: {exists}")
            else:
                print(f"    NO ProductImage records found")
            
            print()
        
        # Count summary
        print("\n[STEP 3] Summary Statistics")
        total_images = ProductImage.query.count()
        print(f"Total ProductImage records: {total_images}")

        products_with_images = db.session.query(ProductImage.product_id).distinct().count()
        print(f"Products with images: {products_with_images}")

        uploaded_images = ProductImage.query.filter(ProductImage.image_url.like('%/static/uploads/%')).count()
        print(f"Uploaded images (in /static/uploads/): {uploaded_images}")

        external_images = ProductImage.query.filter(ProductImage.image_url.like('http%')).count()
        print(f"External images (http): {external_images}")

        # Check primary images
        print("\n[STEP 4] Primary Image Status")
        primary_images = ProductImage.query.filter_by(is_primary=True).count()
        print(f"Images marked as primary: {primary_images}")

        non_primary = ProductImage.query.filter_by(is_primary=False).count()
        print(f"Images NOT marked as primary: {non_primary}")

        # Find products with images but no primary
        print("\n[STEP 5] Products with images but no primary")
        all_product_ids = db.session.query(ProductImage.product_id).distinct().all()
        for product_id_tuple in all_product_ids[:5]:
            product_id = product_id_tuple[0]
            product = Product.query.get(product_id)
            primary = ProductImage.query.filter_by(product_id=product_id, is_primary=True).first()

            if not primary:
                images = ProductImage.query.filter_by(product_id=product_id).all()
                print(f"  {product.name}: {len(images)} images, NO PRIMARY")
                print(f"    main_image returns: {product.main_image}")
        
        print("\n" + "="*70)
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()

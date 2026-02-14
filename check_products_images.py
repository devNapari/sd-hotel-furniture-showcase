"""Check products and their images"""
import sys
sys.path.insert(0, r'c:\Users\zoe\Downloads\New folder\New folder\sd-hotel-furniture-showcase')

from app import app, db
from models.product import Product, ProductImage

with app.app_context():
    # Get all products
    products = Product.query.filter_by(is_active=True).all()
    
    print(f"\nTotal active products: {len(products)}")
    print("=" * 80)
    
    for i, product in enumerate(products[:10], 1):  # Show first 10
        print(f"\n{i}. {product.name} (ID: {product.id})")
        print(f"   - Price: ${product.price}")
        print(f"   - Main Image: {product.main_image}")
        print(f"   - Uploaded Images: {product.images.count()}")
        
        if product.images.count() > 0:
            for img in product.images.all():
                print(f"     • {img.image_url} (Primary: {img.is_primary})")
        else:
            print(f"     • No images uploaded")
    
    print("\n" + "=" * 80)
    print("\nProducts with NO images:")
    no_image_products = [p for p in products if not p.main_image]
    print(f"Count: {len(no_image_products)}")
    for p in no_image_products[:5]:
        print(f"  - {p.name} (ID: {p.id})")

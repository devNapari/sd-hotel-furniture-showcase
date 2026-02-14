from models.product import Product, ProductImage
products = Product.query.all()
for p in products:
    print(f"Product: {p.name}")
    for img in p.images:
        print(f"  - Image URL: {img.image_url}")
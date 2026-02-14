#!/usr/bin/env python
"""Debug script to check product status in database"""
from app import create_app
from models import db
from models.product import Product

app = create_app()
with app.app_context():
    # Get ALL products (including inactive)
    products = Product.query.all()
    print(f"Total products in DB: {len(products)}")
    print("\nLast 10 products:")
    for p in products[-10:]:
        print(f"  ID: {p.id}, Name: {p.name}, Slug: {p.slug}, is_active: {p.is_active}, category_id: {p.category_id}")
    
    # Check specifically for recently added ones
    print("\nProducts with 'Adams' or 'amina' in name:")
    adams = Product.query.filter(Product.name.ilike('%amina%')).all()
    for p in adams:
        print(f"  ID: {p.id}, Name: {p.name}, Slug: {p.slug}, is_active: {p.is_active}, category_id: {p.category_id}")
    
    # Check active products count
    active = Product.query.filter_by(is_active=True).all()
    print(f"\nTotal ACTIVE products: {len(active)}")
    
    # Test API query
    print("\nSimulating API query (is_active=True filter):")
    api_products = Product.query.filter_by(is_active=True).all()
    print(f"API would return {len(api_products)} products")

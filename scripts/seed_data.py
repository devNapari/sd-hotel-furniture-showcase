"""
Database seeding script to populate with sample data
"""
from models import db
from models.user import User
from models.product import Product, Category, ProductImage
from models.order import Order, OrderItem
from models.review import Review
import re


def _generate_unique_slug(session, Model, base_slug, current_id=None):
    """Generate a unique slug by appending -1, -2, ... if needed."""
    slug = base_slug
    i = 1
    query = session.query(Model).filter_by(slug=slug)
    if current_id:
        query = query.filter(Model.id != current_id)
    while query.first() is not None:
        slug = f"{base_slug}-{i}"
        i += 1
        query = session.query(Model).filter_by(slug=slug)
        if current_id:
            query = query.filter(Model.id != current_id)
    return slug


def seed_database():
    """Seed the database with sample data"""
    print("Starting database seeding...")
    
    # Create categories
    print("Creating categories...")
    categories = [
        Category(
            name='Guest Room',
            slug='guest-room',
            description='Furniture for hotel guest rooms',
            image_url='https://picsum.photos/seed/guestroom/600/400',
            is_active=True,
            display_order=1
        ),
        Category(
            name='Lobby & Public Area',
            slug='lobby',
            description='Furniture for hotel lobbies and public spaces',
            image_url='https://picsum.photos/seed/lobby/600/400',
            is_active=True,
            display_order=2
        ),
        Category(
            name='Restaurant & Bar',
            slug='restaurant',
            description='Furniture for hotel restaurants and bars',
            image_url='https://picsum.photos/seed/restaurant/600/400',
            is_active=True,
            display_order=3
        ),
        Category(
            name='Outdoor',
            slug='outdoor',
            description='Outdoor furniture for hotels',
            image_url='https://picsum.photos/seed/outdoor/600/400',
            is_active=True,
            display_order=4
        )
    ]
    
    for category in categories:
        db.session.add(category)
    
    db.session.commit()
    print(f"Created {len(categories)} categories")
    
    # Create products
    print("Creating products...")
    products_data = [
        {
            'name': 'Luxury King Bed Frame',
            'slug': 'luxury-king-bed-frame',
            'sku': 'BED-001',
            'description': 'Premium solid wood king bed frame with elegant upholstered headboard. Perfect for luxury hotel rooms.',
            'short_description': 'Premium solid wood king bed frame',
            'price': 2499.99,
            'category': 'guest-room',
            'features': ['Solid wood construction', 'Upholstered headboard', 'Easy assembly', 'Weight capacity: 800 lbs'],
            'stock_quantity': 50,
            'is_featured': True
        },
        {
            'name': 'Modern Nightstand Set',
            'slug': 'modern-nightstand-set',
            'sku': 'NS-001',
            'description': 'Contemporary nightstand with soft-close drawers and USB charging ports.',
            'short_description': 'Contemporary nightstand with USB ports',
            'price': 599.99,
            'category': 'guest-room',
            'features': ['2 soft-close drawers', 'Built-in USB ports', 'Scratch-resistant surface', 'Set of 2'],
            'stock_quantity': 100
        },
        {
            'name': 'Executive Desk Chair',
            'slug': 'executive-desk-chair',
            'sku': 'CHAIR-001',
            'description': 'Ergonomic office chair with premium leather upholstery and adjustable features.',
            'short_description': 'Ergonomic office chair',
            'price': 449.99,
            'category': 'guest-room',
            'features': ['Genuine leather', 'Adjustable height', 'Lumbar support', '360° swivel'],
            'stock_quantity': 75
        },
        {
            'name': 'Grand Lobby Sofa',
            'slug': 'grand-lobby-sofa',
            'sku': 'SOFA-001',
            'description': 'Luxurious 3-seater sofa with premium fabric and solid hardwood frame.',
            'short_description': 'Luxurious 3-seater sofa',
            'price': 3999.99,
            'category': 'lobby',
            'features': ['Premium fabric upholstery', 'Hardwood frame', 'High-density foam', 'Seats 3 people'],
            'stock_quantity': 30,
            'is_featured': True
        },
        {
            'name': 'Reception Desk',
            'slug': 'reception-desk',
            'sku': 'DESK-001',
            'description': 'Modern reception desk with integrated lighting and cable management.',
            'short_description': 'Modern reception desk',
            'price': 5499.99,
            'category': 'lobby',
            'features': ['LED lighting', 'Cable management', 'Durable laminate', 'Custom branding available'],
            'stock_quantity': 20
        },
        {
            'name': 'Restaurant Dining Table',
            'slug': 'restaurant-dining-table',
            'sku': 'TABLE-001',
            'description': 'Solid wood dining table for 4-6 people with scratch-resistant finish.',
            'short_description': 'Solid wood dining table',
            'price': 1299.99,
            'category': 'restaurant',
            'features': ['Solid wood', 'Seats 4-6', 'Scratch-resistant', 'Commercial grade'],
            'stock_quantity': 60
        },
        {
            'name': 'Bar Stool Set',
            'slug': 'bar-stool-set',
            'sku': 'STOOL-001',
            'description': 'Modern bar stools with adjustable height and footrest.',
            'short_description': 'Modern adjustable bar stools',
            'price': 799.99,
            'category': 'restaurant',
            'features': ['Adjustable height', 'Swivel seat', 'Footrest', 'Set of 4'],
            'stock_quantity': 80
        },
        {
            'name': 'Patio Lounge Set',
            'slug': 'patio-lounge-set',
            'sku': 'PATIO-001',
            'description': 'Weather-resistant outdoor lounge set with cushions.',
            'short_description': 'Weather-resistant lounge set',
            'price': 2799.99,
            'category': 'outdoor',
            'features': ['Weather-resistant', 'UV-protected cushions', 'Aluminum frame', 'Includes 2 chairs and table'],
            'stock_quantity': 40,
            'is_featured': True
        }
    ]
    
    for product_data in products_data:
        category = Category.query.filter_by(slug=product_data['category']).first()
        
        # Ensure unique slug
        base_slug = product_data['slug'] or re.sub(r'[^\w\s-]', '', product_data['name'].lower())
        base_slug = re.sub(r'[-\s]+', '-', base_slug).strip('-')
        unique_slug = _generate_unique_slug(db.session, Product, base_slug, current_id=None)
        
        product = Product(
            name=product_data['name'],
            slug=unique_slug,
            sku=product_data['sku'],
            description=product_data['description'],
            short_description=product_data['short_description'],
            price=product_data['price'],
            category_id=category.id,
            features=product_data['features'],
            stock_quantity=product_data.get('stock_quantity', 0),
            is_active=True,
            is_featured=product_data.get('is_featured', False),
            average_rating=4.5,
            review_count=0
        )
        
        db.session.add(product)
        db.session.flush()
        
        # Add product image
        image = ProductImage(
            product_id=product.id,
            image_url=f'https://picsum.photos/seed/{unique_slug}/400/400',
            alt_text=product.name,
            is_primary=True,
            display_order=1
        )
        db.session.add(image)
    
    db.session.commit()
    print(f"Created {len(products_data)} products")
    
    # Create sample users
    print("Creating sample users...")
    users_data = [
        {
            'email': 'admin@sdhotelfurniture.com',
            'username': 'admin',
            'password': 'admin123',
            'first_name': 'Admin',
            'last_name': 'User',
            'role': 'admin',
            'is_verified': True
        },
        {
            'email': 'customer@example.com',
            'username': 'customer',
            'password': 'customer123',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'customer',
            'is_verified': True
        }
    ]
    
    for user_data in users_data:
        user = User.create_user(**user_data)
        db.session.add(user)
    
    db.session.commit()
    print(f"Created {len(users_data)} users")
    
    print("Database seeding completed successfully!")
    print("\nSample credentials:")
    print("Admin - Email: admin@sdhotelfurniture.com, Password: admin123")
    print("Customer - Email: customer@example.com, Password: customer123")


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Seed data
        seed_database()
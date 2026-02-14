"""
Script to create blog tables in the database
Run this after adding the blog models to create the necessary tables
"""
from app import app, db
from models.blog import BlogPost, BlogCategory, BlogComment

def create_blog_tables():
    """Create blog tables in the database"""
    with app.app_context():
        # Create all tables (will only create missing ones)
        db.create_all()
        print("✓ Blog tables created successfully!")
        
        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        blog_tables = ['blog_posts', 'blog_categories', 'blog_comments']
        created_tables = [t for t in blog_tables if t in tables]
        
        print(f"\nCreated tables: {', '.join(created_tables)}")
        
        if len(created_tables) == len(blog_tables):
            print("\n✓ All blog tables created successfully!")
            print("\nNext steps:")
            print("1. Create an admin user if you haven't: flask create-admin")
            print("2. Log into the admin panel at /admin")
            print("3. Create your first blog post")
            print("4. Visit /blog to see your blog!")
        else:
            missing = [t for t in blog_tables if t not in created_tables]
            print(f"\n⚠ Warning: Some tables may not have been created: {', '.join(missing)}")

if __name__ == '__main__':
    create_blog_tables()
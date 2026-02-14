# Blog System Setup Guide

## Database Migration Required

The blog system has been successfully added to the application, but the database tables need to be created.

## Quick Setup Steps

### Option 1: Using Flask-Migrate (Recommended)

1. **Create a new migration**:
   ```bash
   flask db migrate -m "Add blog models"
   ```

2. **Apply the migration**:
   ```bash
   flask db upgrade
   ```

### Option 2: Recreate Database (Development Only)

If you're in development and don't mind losing existing data:

1. **Delete the existing database**:
   ```bash
   # On Windows
   del instance\app.db
   
   # On Linux/Mac
   rm instance/app.db
   ```

2. **Initialize the database**:
   ```bash
   flask db init
   flask db migrate -m "Initial migration with blog"
   flask db upgrade
   ```

### Option 3: Direct Table Creation

Run this Python script to create just the blog tables:

```python
from app import app, db
from models.blog import BlogPost, BlogCategory, BlogComment

with app.app_context():
    # Create only blog tables
    db.create_all()
    print("Blog tables created successfully!")
```

Save this as `create_blog_tables.py` and run:
```bash
python create_blog_tables.py
```

## Verify Installation

After running migrations, verify the tables were created:

```python
from app import app, db
from models.blog import BlogPost

with app.app_context():
    count = BlogPost.query.count()
    print(f"Blog posts table exists! Current count: {count}")
```

## Create Sample Blog Posts

You can create sample blog posts through the admin panel at `/admin` or using this script:

```python
from app import app, db
from models.blog import BlogPost, BlogCategory
from models.user import User
from datetime import datetime

with app.app_context():
    # Get or create an admin user
    admin = User.query.filter_by(role='admin').first()
    
    if not admin:
        print("Please create an admin user first using: flask create-admin")
    else:
        # Create a sample blog post
        post = BlogPost(
            title="Welcome to Our Blog",
            slug="welcome-to-our-blog",
            content="""
            <h2>Welcome to SD Hotel Furniture Blog</h2>
            <p>We're excited to launch our new blog where we'll share insights about hotel furniture design, industry trends, and tips for creating beautiful hospitality spaces.</p>
            <h3>What to Expect</h3>
            <ul>
                <li>Design inspiration and trends</li>
                <li>Product spotlights and reviews</li>
                <li>Industry news and updates</li>
                <li>Tips for hotel owners and designers</li>
            </ul>
            <p>Stay tuned for regular updates!</p>
            """,
            excerpt="Welcome to our new blog! Learn about hotel furniture design, trends, and industry insights.",
            category="news",
            tags="welcome, announcement, blog",
            author_id=admin.id,
            status="published",
            is_featured=True,
            published_at=datetime.utcnow()
        )
        
        db.session.add(post)
        db.session.commit()
        
        print(f"Sample blog post created! View it at: /blog/{post.slug}")
```

Save as `create_sample_post.py` and run:
```bash
python create_sample_post.py
```

## Blog Features

Once set up, you can:

1. **Admin Panel** (`/admin`):
   - Create/edit/delete blog posts
   - Manage categories
   - Moderate comments
   - Set featured posts

2. **Public Blog** (`/blog`):
   - Browse all published posts
   - Search articles
   - Filter by category
   - Read and comment (login required)

3. **Individual Posts** (`/blog/<slug>`):
   - Full article view
   - Related posts
   - Comment system
   - Social sharing

## Troubleshooting

### "no such table: blog_posts" Error

This means migrations haven't been run. Follow Option 1 or 2 above.

### "no such column" Error

The database schema is out of sync. Run:
```bash
flask db migrate -m "Update blog schema"
flask db upgrade
```

### Can't Create Posts in Admin

Make sure you're logged in as an admin user. Create one with:
```bash
flask create-admin
```

## Next Steps

1. Run the database migration
2. Create an admin user (if you haven't already)
3. Log into `/admin`
4. Create your first blog post
5. Visit `/blog` to see it live!

## Support

If you encounter any issues, check:
- Database file exists in `instance/app.db`
- Flask-Migrate is installed: `pip install Flask-Migrate`
- All blog models are imported in `app.py`
- Admin user exists and has proper permissions
"""
Blog/News model for articles and updates
"""
from datetime import datetime
from models import db


class BlogPost(db.Model):
    """Blog post model for news and articles"""
    __tablename__ = 'blog_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(500))
    featured_image = db.Column(db.String(500))
    category = db.Column(db.String(50), default='general')
    tags = db.Column(db.String(200))  # Comma-separated tags
    
    # Author information
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('User', backref='blog_posts')
    
    # Status and visibility
    status = db.Column(db.String(20), default='draft')  # draft, published, archived
    is_featured = db.Column(db.Boolean, default=False)
    
    # SEO fields
    meta_title = db.Column(db.String(200))
    meta_description = db.Column(db.String(300))
    
    # Engagement metrics
    views = db.Column(db.Integer, default=0)
    
    # Timestamps
    published_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<BlogPost {self.title}>'
    
    @property
    def reading_time(self):
        """Calculate estimated reading time in minutes"""
        words = len(self.content.split())
        minutes = max(1, round(words / 200))  # Average reading speed: 200 words/min
        return minutes
    
    @property
    def tag_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
    
    def increment_views(self):
        """Increment view count"""
        self.views += 1
        db.session.commit()


class BlogCategory(db.Model):
    """Blog categories for organizing posts"""
    __tablename__ = 'blog_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<BlogCategory {self.name}>'


class BlogComment(db.Model):
    """Comments on blog posts"""
    __tablename__ = 'blog_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'), nullable=False)
    post = db.relationship('BlogPost', backref=db.backref('comments', lazy='dynamic'))
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='blog_comments')
    
    content = db.Column(db.Text, nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<BlogComment by {self.user.username} on {self.post.title}>'
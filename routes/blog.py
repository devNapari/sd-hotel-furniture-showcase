"""
Blog routes for viewing articles and news
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from datetime import datetime
from sqlalchemy import or_

from models import db
from models.blog import BlogPost, BlogCategory, BlogComment

blog_bp = Blueprint('blog', __name__, url_prefix='/blog')


@blog_bp.route('/')
def index():
    """Blog listing page with pagination and filtering"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', None)
    search = request.args.get('search', None)
    
    # Base query for published posts
    query = BlogPost.query.filter_by(status='published').order_by(BlogPost.published_at.desc())
    
    # Apply filters
    if category:
        query = query.filter_by(category=category)
    
    if search:
        search_term = f'%{search}%'
        query = query.filter(
            or_(
                BlogPost.title.ilike(search_term),
                BlogPost.content.ilike(search_term),
                BlogPost.excerpt.ilike(search_term)
            )
        )
    
    # Paginate results
    per_page = 9
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    posts = pagination.items
    
    # Get featured posts for sidebar
    featured_posts = BlogPost.query.filter_by(
        status='published',
        is_featured=True
    ).order_by(BlogPost.published_at.desc()).limit(3).all()
    
    # Get categories
    categories = db.session.query(
        BlogPost.category,
        db.func.count(BlogPost.id).label('count')
    ).filter_by(status='published').group_by(BlogPost.category).all()
    
    # Get recent posts for sidebar
    recent_posts = BlogPost.query.filter_by(
        status='published'
    ).order_by(BlogPost.published_at.desc()).limit(5).all()
    
    return render_template(
        'blog/index.html',
        posts=posts,
        pagination=pagination,
        featured_posts=featured_posts,
        categories=categories,
        recent_posts=recent_posts,
        current_category=category,
        search_query=search
    )


@blog_bp.route('/<slug>')
def detail(slug):
    """Blog post detail page"""
    post = BlogPost.query.filter_by(slug=slug, status='published').first_or_404()
    
    # Increment view count
    post.increment_views()
    
    # Get approved comments
    comments = BlogComment.query.filter_by(
        post_id=post.id,
        is_approved=True
    ).order_by(BlogComment.created_at.desc()).all()
    
    # Get related posts (same category, excluding current)
    related_posts = BlogPost.query.filter(
        BlogPost.category == post.category,
        BlogPost.id != post.id,
        BlogPost.status == 'published'
    ).order_by(BlogPost.published_at.desc()).limit(3).all()
    
    return render_template(
        'blog/detail.html',
        post=post,
        comments=comments,
        related_posts=related_posts
    )


@blog_bp.route('/<slug>/comment', methods=['POST'])
@login_required
def add_comment(slug):
    """Add a comment to a blog post"""
    post = BlogPost.query.filter_by(slug=slug, status='published').first_or_404()
    
    content = request.form.get('content', '').strip()
    
    if not content:
        flash('Comment cannot be empty.', 'danger')
        return redirect(url_for('blog.detail', slug=slug))
    
    if len(content) < 10:
        flash('Comment must be at least 10 characters long.', 'danger')
        return redirect(url_for('blog.detail', slug=slug))
    
    comment = BlogComment(
        post_id=post.id,
        user_id=current_user.id,
        content=content,
        is_approved=False  # Requires admin approval
    )
    
    db.session.add(comment)
    db.session.commit()
    
    flash('Your comment has been submitted and is awaiting approval.', 'success')
    return redirect(url_for('blog.detail', slug=slug))


@blog_bp.route('/category/<category>')
def category(category):
    """View posts by category"""
    return redirect(url_for('blog.index', category=category))


@blog_bp.route('/search')
def search():
    """Search blog posts"""
    search_query = request.args.get('q', '')
    return redirect(url_for('blog.index', search=search_query))
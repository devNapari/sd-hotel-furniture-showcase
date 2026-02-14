# SD Hotel Furniture - Database Setup Guide

This guide will help you set up the database and authentication system for the SD Hotel Furniture project.

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- PostgreSQL (for production) or SQLite (for development)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the example environment file and update it with your settings:

```bash
cp .env.example .env
```

Edit `.env` and update the following:
- `SECRET_KEY`: Generate a random secret key
- `DATABASE_URL`: Your database connection string
- Email settings (optional, for password reset)
- OAuth credentials (optional, for social login)

### 3. Initialize the Database

```bash
# Initialize Flask-Migrate
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migrations to database
flask db upgrade
```

### 4. Seed the Database (Optional)

Populate the database with sample data:

```bash
flask seed-db
```

This will create:
- 4 product categories
- 8 sample products
- 2 users (admin and customer)

**Sample Credentials:**
- **Admin**: Email: `admin@sdhotelfurniture.com`, Password: `admin123`
- **Customer**: Email: `customer@example.com`, Password: `customer123`

### 5. Create Admin User (Alternative)

If you prefer to create your own admin user:

```bash
flask create-admin
```

Follow the prompts to enter admin credentials.

### 6. Run the Application

```bash
python app.py
```

Or using Flask CLI:

```bash
flask run
```

The application will be available at `http://localhost:5000`

## 📁 Project Structure

```
sd-hotel-furniture-showcase/
├── app.py                      # Main application file
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create from .env.example)
├── .env.example               # Environment variables template
├── models/                     # Database models
│   ├── __init__.py
│   ├── user.py                # User model
│   ├── product.py             # Product and Category models
│   ├── order.py               # Order and OrderItem models
│   ├── review.py              # Review model
│   └── wishlist.py            # Wishlist model
├── routes/                     # Application routes
│   ├── __init__.py
│   ├── auth.py                # Authentication routes
│   └── api.py                 # API endpoints
├── scripts/                    # Utility scripts
│   └── seed_data.py           # Database seeding script
├── templates/                  # HTML templates
│   ├── index.html
│   ├── products.html
│   ├── shop.html
│   ├── projects.html
│   ├── about.html
│   ├── contact.html
│   └── auth/                  # Authentication templates (to be created)
│       ├── login.html
│       ├── register.html
│       ├── profile.html
│       ├── edit_profile.html
│       └── change_password.html
└── static/                     # Static files
    ├── css/
    ├── js/
    └── images/
```

## 🗄️ Database Models

### User Model
- Authentication (email, password)
- Profile information
- Role-based access (admin, staff, customer)
- OAuth integration support

### Product Model
- Product details (name, description, price)
- Inventory management
- Categories
- Multiple images
- Features and specifications

### Order Model
- Order management
- Shipping and billing information
- Order status tracking
- Payment information

### Review Model
- Product reviews and ratings
- Admin approval system

### Wishlist Model
- Save products for later

## 🔐 Authentication Features

### Implemented:
- ✅ User registration
- ✅ User login/logout
- ✅ Password hashing (bcrypt)
- ✅ Session management
- ✅ Role-based access control
- ✅ User profile management
- ✅ Password change

### To Be Implemented:
- ⏳ Email verification
- ⏳ Password reset via email
- ⏳ OAuth (Google, Facebook, LinkedIn)
- ⏳ Two-factor authentication

## 🔌 API Endpoints

### Products
- `GET /api/products` - Get all products (with filtering)
- `GET /api/products/<id>` - Get single product
- `GET /api/categories` - Get all categories

### Wishlist
- `GET /api/wishlist` - Get user's wishlist
- `POST /api/wishlist/<product_id>` - Add to wishlist
- `DELETE /api/wishlist/<product_id>` - Remove from wishlist

### Reviews
- `GET /api/products/<id>/reviews` - Get product reviews
- `POST /api/products/<id>/reviews` - Create review

### Orders
- `GET /api/orders` - Get user's orders
- `GET /api/orders/<id>` - Get single order

## 🛠️ CLI Commands

```bash
# Initialize database
flask init-db

# Seed database with sample data
flask seed-db

# Create admin user
flask create-admin

# Database migrations
flask db init          # Initialize migrations
flask db migrate       # Create migration
flask db upgrade       # Apply migrations
flask db downgrade     # Rollback migrations
```

## 🔧 Configuration

### Development
Uses SQLite database by default. Configuration in `config.py`:
```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///hotel_furniture.db'
```

### Production
Use PostgreSQL for production. Set in `.env`:
```
DATABASE_URL=postgresql://username:password@localhost/hotel_furniture_prod
```

## 🐛 Troubleshooting

### Database Connection Error
- Check your `DATABASE_URL` in `.env`
- Ensure PostgreSQL is running (if using PostgreSQL)
- Verify database credentials

### Migration Errors
```bash
# Reset migrations
rm -rf migrations/
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 📚 Next Steps

1. **Create Authentication Templates**
   - Login page
   - Registration page
   - User profile pages

2. **Implement Admin Panel**
   - Use Flask-Admin
   - Manage products, orders, users

3. **Add Email Functionality**
   - Email verification
   - Password reset
   - Order confirmations

4. **Implement OAuth**
   - Google login
   - Facebook login
   - LinkedIn login

5. **Add Payment Integration**
   - Stripe or PayPal
   - Order processing
   - Invoice generation

## 🔒 Security Notes

- Change `SECRET_KEY` in production
- Use HTTPS in production
- Enable CSRF protection
- Implement rate limiting
- Regular security audits
- Keep dependencies updated

## 📞 Support

For issues or questions:
1. Check this guide
2. Review error logs
3. Check Flask documentation
4. Check SQLAlchemy documentation

---

**Important**: Never commit `.env` file to version control. It contains sensitive information.
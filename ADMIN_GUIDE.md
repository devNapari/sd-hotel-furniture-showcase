# 🔐 Admin Panel Guide - SD Hotel Furniture

Complete guide for using the Flask-Admin panel to manage your e-commerce platform.

## 📋 Table of Contents

1. [Installation](#installation)
2. [Accessing the Admin Panel](#accessing-the-admin-panel)
3. [Dashboard Overview](#dashboard-overview)
4. [Managing Users](#managing-users)
5. [Managing Products](#managing-products)
6. [Managing Orders](#managing-orders)
7. [Managing Reviews](#managing-reviews)
8. [Security Features](#security-features)
9. [Troubleshooting](#troubleshooting)

---

## 🚀 Installation

### Step 1: Install Flask-Admin

```bash
pip install -r requirements.txt
```

This will install Flask-Admin==1.6.1 along with all other dependencies.

### Step 2: Initialize Database

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Step 3: Seed Database

```bash
flask seed-db
```

This creates:
- Admin user: `admin@sdhotelfurniture.com` / `admin123`
- Customer user: `customer@example.com` / `customer123`
- 4 product categories
- 8 sample products

### Step 4: Run Application

```bash
python app.py
```

---

## 🔑 Accessing the Admin Panel

### Admin URL

**http://localhost:5000/admin**

### Login Credentials

**Admin Account:**
- Email: `admin@sdhotelfurniture.com`
- Password: `admin123`

**Important:** Change the default password immediately after first login!

### Access Requirements

- Must be logged in
- Must have `admin` role
- Non-admin users will be redirected to login page

---

## 📊 Dashboard Overview

The admin dashboard provides:

### Statistics Cards

1. **Total Users** - Count of all registered users
2. **Total Products** - Count of all products (with active count)
3. **Total Orders** - Count of all orders (with pending count)
4. **Total Reviews** - Count of all reviews (with pending approval count)

### Recent Activity

- **Recent Orders** - Last 5 orders with status and totals
- **Recent Users** - Last 5 registered users with roles

### Quick Actions

- Add New Product
- Add New Category
- Add New User
- Approve Reviews

---

## 👥 Managing Users

### Access: Admin → User Management → Users

### Features

**View Users:**
- List all users with pagination
- Search by username, email, name
- Filter by role, active status, verified status
- Sort by registration date

**Edit Users:**
- Click on any user to edit
- Update profile information
- Change role (customer, staff, admin)
- Toggle active/verified status
- View user's orders and reviews

**Quick Edit:**
- Toggle `Active` status directly in list
- Toggle `Verified` status directly in list
- Change `Role` directly in list

**Create New User:**
- Click "Create" button
- Fill in required fields:
  - Email (unique)
  - Username (unique)
  - Password
  - Role
- Optional fields:
  - First/Last name
  - Phone, Company
  - Address information

**Delete User:**
- Click on user → Delete
- Confirmation required
- **Warning:** This will also delete user's orders and reviews

### User Roles

- **Customer** - Regular user, can shop and review
- **Staff** - Employee access (future feature)
- **Admin** - Full access to admin panel

---

## 🛍️ Managing Products

### Access: Admin → Catalog → Products

### Features

**View Products:**
- List all products with images
- Search by name, SKU, description
- Filter by:
  - Category
  - Active status
  - Featured status
  - New/On Sale status
  - Creation date
- Sort by any column

**Quick Edit:**
- Edit `Price` directly in list
- Edit `Stock Quantity` directly in list
- Toggle `Active` status
- Toggle `Featured` status

**Create New Product:**

Required Fields:
- **Name** - Product name
- **SKU** - Stock Keeping Unit (unique)
- **Price** - Product price
- **Category** - Select from dropdown

Optional Fields:
- **Short Description** - Brief description
- **Description** - Full product description
- **Compare At Price** - Original price (for sales)
- **Stock Quantity** - Available stock
- **Low Stock Threshold** - Alert level
- **Features** - JSON array of features
- **Specifications** - JSON object of specs
- **Dimensions** - Product dimensions
- **Weight** - Product weight
- **Material** - Product material
- **Color Options** - Available colors
- **Tags** - Comma-separated tags

Flags:
- ☑️ **Is Active** - Show on website
- ☑️ **Is Featured** - Show in featured section
- ☑️ **Is New** - Mark as new arrival
- ☑️ **Is On Sale** - Mark as on sale

**Edit Product:**
- Click on product name
- Update any field
- Save changes

**Delete Product:**
- Click on product → Delete
- Confirmation required
- **Warning:** This will affect orders containing this product

### Product Images

**Access: Admin → Catalog → Product Images**

- Add multiple images per product
- Set primary image
- Set display order
- Add alt text for SEO

---

## 📦 Managing Orders

### Access: Admin → Sales → Orders

### Features

**View Orders:**
- List all orders
- Search by order number, tracking number
- Filter by:
  - Status (pending, processing, shipped, delivered, cancelled)
  - Payment status (pending, paid, failed, refunded)
  - Payment method
  - Date range
- Sort by date

**Order Statuses:**
- **Pending** - New order, awaiting processing
- **Processing** - Order being prepared
- **Shipped** - Order dispatched
- **Delivered** - Order received by customer
- **Cancelled** - Order cancelled

**Payment Statuses:**
- **Pending** - Payment not received
- **Paid** - Payment successful
- **Failed** - Payment failed
- **Refunded** - Payment refunded

**Quick Edit:**
- Change `Status` directly in list
- Change `Payment Status` directly in list

**View Order Details:**
- Click on order number
- See customer information
- View order items
- Check shipping/billing addresses
- View payment details
- Update order status
- Add tracking number

**Order Items:**

**Access: Admin → Sales → Order Items**

- View all order items across all orders
- See product details
- Check quantities and prices
- Filter by order

---

## ⭐ Managing Reviews

### Access: Admin → Content → Reviews

### Features

**View Reviews:**
- List all product reviews
- Search by title, comment
- Filter by:
  - Rating (1-5 stars)
  - Approval status
  - Verified purchase
  - Date
- Sort by date

**Quick Edit:**
- Toggle `Approved` status directly in list

**Approve/Reject Reviews:**
- Click on review
- Toggle "Is Approved" checkbox
- Save changes

**Review Details:**
- Product name
- Customer name
- Rating (1-5 stars)
- Title and comment
- Verified purchase badge
- Creation date

**Delete Review:**
- Click on review → Delete
- Confirmation required

---

## 📂 Managing Categories

### Access: Admin → Catalog → Categories

### Features

**View Categories:**
- List all product categories
- See product count per category
- View parent-child relationships

**Create Category:**
- Name (required)
- Description
- Parent category (for subcategories)
- SEO fields

**Edit Category:**
- Update name and description
- Change parent category
- Slug is auto-generated

**Delete Category:**
- Only if no products assigned
- Confirmation required

---

## 💝 Managing Wishlists

### Access: Admin → Content → Wishlists

### Features

- View all wishlist items
- See which users saved which products
- Filter by user or product
- View customer notes
- Sort by date added

---

## 🔒 Security Features

### Authentication

- **Login Required** - All admin pages require authentication
- **Role-Based Access** - Only admin users can access
- **Session Management** - Secure session handling
- **Auto-Redirect** - Non-admins redirected to login

### Authorization

```python
def is_accessible(self):
    return current_user.is_authenticated and current_user.is_admin
```

### Password Security

- Passwords hashed with bcrypt
- Never stored in plain text
- Strong password requirements recommended

### Best Practices

1. **Change Default Password** - Immediately after first login
2. **Use Strong Passwords** - Minimum 8 characters, mixed case, numbers, symbols
3. **Limit Admin Accounts** - Only create admin accounts when necessary
4. **Regular Audits** - Review user accounts regularly
5. **Monitor Activity** - Check recent orders and users
6. **Backup Database** - Regular backups recommended

---

## 🎨 Customization

### Custom Admin Views

Located in: `admin/__init__.py`

**Customize Columns:**
```python
column_list = ['id', 'name', 'email', 'created_at']
```

**Add Filters:**
```python
column_filters = ['status', 'is_active', 'created_at']
```

**Enable Search:**
```python
column_searchable_list = ['name', 'email', 'description']
```

**Quick Edit:**
```python
column_editable_list = ['is_active', 'price', 'stock']
```

### Custom Dashboard

Located in: `templates/admin/dashboard.html`

Customize:
- Statistics cards
- Recent activity sections
- Quick action buttons
- Styling and layout

---

## 🐛 Troubleshooting

### Cannot Access Admin Panel

**Problem:** Redirected to login page

**Solutions:**
1. Ensure you're logged in
2. Check user has `admin` role
3. Verify `is_active` is True
4. Clear browser cache/cookies

### Database Errors

**Problem:** "Table doesn't exist"

**Solution:**
```bash
flask db upgrade
```

**Problem:** "Column doesn't exist"

**Solution:**
```bash
flask db migrate -m "Add missing columns"
flask db upgrade
```

### Permission Errors

**Problem:** "Access denied"

**Solution:**
```python
# Check user role in database
user = User.query.filter_by(email='admin@sdhotelfurniture.com').first()
print(user.role)  # Should be 'admin'
print(user.is_admin)  # Should be True
```

### Flask-Admin Not Loading

**Problem:** Admin routes not found

**Solution:**
1. Check Flask-Admin is installed:
```bash
pip list | findstr Flask-Admin
```

2. Verify admin initialization in app.py:
```python
from admin import init_admin
init_admin(app)
```

3. Restart application

---

## 📱 Mobile Access

The admin panel is responsive and works on mobile devices:

- Collapsible sidebar
- Touch-friendly buttons
- Responsive tables
- Mobile-optimized forms

---

## 🔄 Bulk Operations

### Bulk Delete

1. Select multiple items using checkboxes
2. Choose "Delete" from actions dropdown
3. Confirm deletion

### Bulk Edit (Future Feature)

- Bulk price updates
- Bulk status changes
- Bulk category assignments

---

## 📈 Analytics (Future Feature)

Planned features:
- Sales reports
- Revenue charts
- Popular products
- Customer analytics
- Inventory alerts

---

## 🆘 Support

### Documentation

- Flask-Admin: https://flask-admin.readthedocs.io/
- Flask: https://flask.palletsprojects.com/
- SQLAlchemy: https://docs.sqlalchemy.org/

### Common Tasks

**Reset Admin Password:**
```bash
flask shell
>>> from models.user import User
>>> admin = User.query.filter_by(email='admin@sdhotelfurniture.com').first()
>>> admin.set_password('new_password')
>>> db.session.commit()
```

**Create New Admin:**
```bash
flask create-admin
```

**Check Database:**
```bash
flask shell
>>> from models import db
>>> db.engine.table_names()
```

---

## ✅ Quick Reference

### URLs

- **Admin Panel:** http://localhost:5000/admin
- **Dashboard:** http://localhost:5000/admin/
- **Users:** http://localhost:5000/admin/user/
- **Products:** http://localhost:5000/admin/product/
- **Orders:** http://localhost:5000/admin/order/
- **Reviews:** http://localhost:5000/admin/review/

### Keyboard Shortcuts

- **Ctrl + S** - Save form
- **Esc** - Cancel/Close
- **Ctrl + F** - Search

### Default Credentials

```
Email: admin@sdhotelfurniture.com
Password: admin123
```

**⚠️ IMPORTANT: Change password after first login!**

---

## 🎓 Training Checklist

- [ ] Access admin panel
- [ ] Change default password
- [ ] View dashboard statistics
- [ ] Create a new product
- [ ] Edit product details
- [ ] Upload product images
- [ ] Create a category
- [ ] View and manage orders
- [ ] Approve/reject reviews
- [ ] Create a new user
- [ ] Change user roles
- [ ] Use search and filters
- [ ] Export data (if enabled)

---

**Last Updated:** 2025-11-13
**Version:** 1.0.0
**Admin Panel:** Flask-Admin 1.6.1
#!/usr/bin/env python
"""Check existing admin users and optionally create one"""

from app import app, db
from models.user import User
import getpass

print("\n" + "="*80)
print("ADMIN USER MANAGEMENT")
print("="*80)

with app.app_context():
    try:
        # Check for existing admin users
        print("\n[STEP 1] Checking for existing admin users...\n")
        
        admin_users = User.query.filter_by(role='admin').all()
        
        if admin_users:
            print(f"Found {len(admin_users)} admin user(s):\n")
            for admin in admin_users:
                print(f"  Email: {admin.email}")
                print(f"  Name: {admin.full_name}")
                print(f"  Active: {'Yes' if admin.is_active else 'No'}")
                print()
        else:
            print("No admin users found in database.\n")
        
        # Option to create new admin
        print("[STEP 2] Create new admin user?\n")
        create_admin = input("Create a new admin account? (y/n): ").lower().strip()
        
        if create_admin == 'y':
            print("\nEnter admin details:")
            email = input("Email: ").strip().lower()
            first_name = input("First name: ").strip()
            last_name = input("Last name: ").strip()
            password = getpass.getpass("Password: ")
            confirm_password = getpass.getpass("Confirm password: ")
            
            if password != confirm_password:
                print("\nError: Passwords do not match!")
                exit(1)
            
            # Check if email already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                print(f"\nError: User with email {email} already exists!")
                exit(1)
            
            # Create admin user
            print("\nCreating admin user...")
            admin_user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                role='admin',
                is_active=True,
                is_verified=True
            )
            admin_user.set_password(password)
            
            db.session.add(admin_user)
            db.session.commit()
            
            print(f"\n✓ Admin user created successfully!")
            print(f"\nLogin Details:")
            print(f"  Email: {email}")
            print(f"  Password: (as you entered)")
        
        # Show how to access admin
        print("\n" + "="*80)
        print("ADMIN PANEL ACCESS")
        print("="*80)
        print("\nTo access the admin panel:")
        print("1. Go to: http://localhost:5000/admin")
        print("2. Login with your admin email and password")
        print("3. Manage products, categories, users, orders, etc.")
        print("\n" + "="*80 + "\n")
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()

#!/usr/bin/env python
"""Show admin login details and password reset options"""

from app import app, db
from models.user import User
import getpass

print("\n" + "="*80)
print("ADMIN LOGIN DETAILS")
print("="*80)

with app.app_context():
    try:
        # Get all admin users
        admin_users = User.query.filter_by(role='admin').all()
        
        print("\n[ADMIN ACCOUNTS]\n")
        
        for idx, admin in enumerate(admin_users, 1):
            print(f"Admin #{idx}")
            print(f"  Email: {admin.email}")
            print(f"  Name: {admin.first_name} {admin.last_name}")
            print(f"  Status: {'Active' if admin.is_active else 'Inactive'}")
            print(f"  Verified: {'Yes' if admin.is_verified else 'No'}")
            print(f"  User ID: {admin.id}")
            print()
        
        print("="*80)
        print("NOTE: Passwords are securely hashed and cannot be displayed.")
        print("="*80)
        
        # Offer password reset
        print("\n[PASSWORD RESET OPTION]\n")
        reset = input("Would you like to reset an admin password? (y/n): ").lower().strip()
        
        if reset == 'y':
            print("\nSelect admin account to reset password:\n")
            admin_users = User.query.filter_by(role='admin').all()
            
            for idx, admin in enumerate(admin_users, 1):
                print(f"{idx}. {admin.email} ({admin.full_name})")
            
            choice = input("\nEnter number (1-{}): ".format(len(admin_users)))
            
            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(admin_users):
                    selected_admin = admin_users[choice_idx]
                    
                    print(f"\nResetting password for: {selected_admin.email}")
                    new_password = getpass.getpass("Enter new password: ")
                    confirm_password = getpass.getpass("Confirm password: ")
                    
                    if new_password != confirm_password:
                        print("Error: Passwords do not match!")
                        exit(1)
                    
                    if len(new_password) < 6:
                        print("Error: Password must be at least 6 characters!")
                        exit(1)
                    
                    selected_admin.set_password(new_password)
                    db.session.commit()
                    
                    print(f"\n✓ Password reset successfully for {selected_admin.email}")
                else:
                    print("Invalid selection!")
            except ValueError:
                print("Invalid input!")
        
        print("\n" + "="*80)
        print("ADMIN PANEL ACCESS")
        print("="*80)
        print("\nURL: http://localhost:5000/admin")
        print("\nLogin Steps:")
        print("1. Go to http://localhost:5000/admin")
        print("2. Enter email (from above)")
        print("3. Enter password")
        print("4. Click Login")
        print("\n" + "="*80 + "\n")
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()

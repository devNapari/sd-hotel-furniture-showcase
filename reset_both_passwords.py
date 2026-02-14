#!/usr/bin/env python
"""Reset passwords for both admin accounts"""

from app import app, db
from models.user import User
import secrets
import string

def generate_password(length=12):
    """Generate a secure random password"""
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(characters) for _ in range(length))

print("\n" + "="*80)
print("ADMIN PASSWORD RESET")
print("="*80 + "\n")

with app.app_context():
    try:
        # Get all admin users
        admin_users = User.query.filter_by(role='admin').all()
        
        passwords = {}
        
        for admin in admin_users:
            # Generate new secure password
            new_password = generate_password()
            
            # Update password
            admin.set_password(new_password)
            passwords[admin.email] = new_password
            
            print(f"✓ Reset password for: {admin.email}")
        
        # Commit all changes
        db.session.commit()
        
        print("\n" + "="*80)
        print("NEW ADMIN PASSWORDS")
        print("="*80 + "\n")
        
        for email, password in passwords.items():
            print(f"Email: {email}")
            print(f"Password: {password}")
            print()
        
        print("="*80)
        print("ADMIN PANEL ACCESS")
        print("="*80)
        print("\nURL: http://localhost:5000/admin")
        print("\nUse the email and password above to login.")
        print("\n" + "="*80 + "\n")
        
        # Save to file
        with open('admin_passwords.txt', 'w') as f:
            f.write("ADMIN PASSWORDS - SECURE THIS FILE\n")
            f.write("="*80 + "\n\n")
            for email, password in passwords.items():
                f.write(f"Email: {email}\n")
                f.write(f"Password: {password}\n")
                f.write(f"Admin Panel: http://localhost:5000/admin\n\n")
        
        print("✓ Passwords also saved to 'admin_passwords.txt'")
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()

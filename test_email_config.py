#!/usr/bin/env python3
"""
Test script to verify email configuration
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_email_config():
    """Test email configuration"""
    print("Testing Email Configuration...")
    print("=" * 50)
    
    # Check required environment variables
    required_vars = [
        'MAIL_SERVER',
        'MAIL_PORT', 
        'MAIL_USE_TLS',
        'MAIL_USERNAME',
        'MAIL_PASSWORD',
        'MAIL_DEFAULT_SENDER'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            # Hide password in output
            if var == 'MAIL_PASSWORD':
                print(f"{var}: {'*' * len(value)}")
            else:
                print(f"{var}: {value}")
        else:
            print(f"{var}: NOT SET")
            missing_vars.append(var)
    
    print("\n" + "=" * 50)
    
    if missing_vars:
        print(f"Missing environment variables: {', '.join(missing_vars)}")
        return False
    else:
        print("All required environment variables are set")
    
    # Test email connectivity
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        # Get email settings
        mail_server = os.environ.get('MAIL_SERVER')
        mail_port = int(os.environ.get('MAIL_PORT'))
        mail_username = os.environ.get('MAIL_USERNAME')
        mail_password = os.environ.get('MAIL_PASSWORD')
        
        print(f"\nTesting connection to {mail_server}:{mail_port}...")
        
        # Test connection
        server = smtplib.SMTP(mail_server, mail_port)
        server.starttls()
        server.login(mail_username, mail_password)
        
        server.quit()
        
        print("Email server connection successful!")
        print("Authentication successful!")
        print("\nNote: Test email not actually sent (this is just a configuration test)")
        
        return True
        
    except Exception as e:
        print(f"Email configuration test failed: {str(e)}")
        print("\nTroubleshooting Tips:")
        print("1. Make sure you're using an App Password for Gmail (not your regular password)")
        print("2. Enable 'Less secure app access' in your Google Account settings")
        print("3. Or use 2-Step Verification and create an App Password")
        print("4. Check if your firewall allows outbound SMTP connections")
        return False

def test_flask_mail():
    """Test Flask-Mail integration"""
    print("\n" + "=" * 50)
    print("Testing Flask-Mail Integration...")
    print("=" * 50)
    
    try:
        from flask import Flask
        from flask_mail import Mail, Message
        
        # Create test app
        app = Flask(__name__)
        app.config['TESTING'] = True
        
        # Configure mail
        app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
        app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT'))
        app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
        app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
        app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
        app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
        
        # Initialize mail
        mail = Mail(app)
        
        print("Flask-Mail initialized successfully")
        print(f"Mail server: {app.config['MAIL_SERVER']}")
        print(f"Mail port: {app.config['MAIL_PORT']}")
        print(f"TLS enabled: {app.config['MAIL_USE_TLS']}")
        print(f"Default sender: {app.config['MAIL_DEFAULT_SENDER']}")
        
        return True
        
    except Exception as e:
        print(f"Flask-Mail integration test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("SD Hotel Furniture - Email Configuration Test")
    print("=" * 60)
    
    # Test basic configuration
    config_ok = test_email_config()
    
    # Test Flask-Mail integration
    flask_ok = test_flask_mail()
    
    print("\n" + "=" * 60)
    if config_ok and flask_ok:
        print("SUCCESS: All email configuration tests passed!")
        print("\nYour email setup is ready to use. Contact forms and consultation")
        print("requests will now be able to send emails automatically.")
        sys.exit(0)
    else:
        print("WARNING: Some email configuration tests failed.")
        print("Please check the error messages above and fix the issues.")
        sys.exit(1)
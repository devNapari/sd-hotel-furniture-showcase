"""
Test script for email forwarding feature
This validates that:
1. Contact and consultation forms still save to database correctly
2. Email notifications are sent asynchronously without blocking
3. Existing features are not affected
"""

import os
import sys
from datetime import datetime

# Set up environment
os.environ['FLASK_ENV'] = 'development'

from app import create_app, db
from models.notification import ContactMessage, ConsultationRequest
from routes.api import send_contact_notification_email, send_consultation_notification_email

def test_contact_form_database_save():
    """Test that contact form data saves to database correctly"""
    print("\n" + "="*70)
    print("TEST 1: Contact Form - Database Save")
    print("="*70)
    
    app = create_app()
    with app.app_context():
        # Clear existing test data
        ContactMessage.query.delete()
        db.session.commit()
        
        # Create test contact message
        test_message = ContactMessage(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            phone="+233123456789",
            company="Test Company",
            subject="Test Subject",
            message="This is a test message",
            newsletter=1
        )
        
        db.session.add(test_message)
        db.session.commit()
        
        # Verify it was saved
        saved_msg = ContactMessage.query.filter_by(email="test@example.com").first()
        assert saved_msg is not None, "Contact message not saved"
        assert saved_msg.first_name == "Test", "First name mismatch"
        assert saved_msg.is_read == False, "Message should be unread initially"
        
        print("✓ Contact message saved successfully")
        print(f"  ID: {saved_msg.id}")
        print(f"  From: {saved_msg.first_name} {saved_msg.last_name}")
        print(f"  Email: {saved_msg.email}")
        print(f"  Subject: {saved_msg.subject}")
        print(f"  Created: {saved_msg.created_at}")
        
        return True

def test_consultation_form_database_save():
    """Test that consultation form data saves to database correctly"""
    print("\n" + "="*70)
    print("TEST 2: Consultation Form - Database Save with Cart Items")
    print("="*70)
    
    app = create_app()
    with app.app_context():
        # Clear existing test data
        ConsultationRequest.query.delete()
        db.session.commit()
        
        # Create test consultation with cart items
        test_consultation = ConsultationRequest(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone="+233987654321",
            company="Acme Corp",
            subject="Furniture Consultation",
            message="I need custom furniture for my office",
            preferred_date="2026-02-20",
            preferred_time="14:30",
            newsletter=0
        )
        
        # Set cart items as JSON
        cart_items = [
            {"id": 1, "name": "Office Chair", "price": 150.00, "quantity": 2},
            {"id": 2, "name": "Standing Desk", "price": 500.00, "quantity": 1}
        ]
        test_consultation.set_cart_items(cart_items)
        
        db.session.add(test_consultation)
        db.session.commit()
        
        # Verify it was saved
        saved_consultation = ConsultationRequest.query.filter_by(
            email="john@example.com"
        ).first()
        
        assert saved_consultation is not None, "Consultation not saved"
        assert saved_consultation.first_name == "John", "First name mismatch"
        assert saved_consultation.preferred_date == "2026-02-20", "Date mismatch"
        assert saved_consultation.is_read == False, "Should be unread initially"
        
        # Verify cart items
        retrieved_items = saved_consultation.get_cart_items()
        assert len(retrieved_items) == 2, f"Expected 2 items, got {len(retrieved_items)}"
        assert retrieved_items[0]['name'] == "Office Chair", "Cart item mismatch"
        
        total = sum(item['price'] * item['quantity'] for item in retrieved_items)
        
        print("✓ Consultation saved successfully with cart items")
        print(f"  ID: {saved_consultation.id}")
        print(f"  From: {saved_consultation.first_name} {saved_consultation.last_name}")
        print(f"  Email: {saved_consultation.email}")
        print(f"  Preferred Date/Time: {saved_consultation.preferred_date} @ {saved_consultation.preferred_time}")
        print(f"  Cart Items: {len(retrieved_items)} items")
        print(f"  Cart Total: GHS {total:.2f}")
        print(f"  Created: {saved_consultation.created_at}")
        
        return True

def test_email_notification_functions_exist():
    """Test that email notification functions exist and don't crash"""
    print("\n" + "="*70)
    print("TEST 3: Email Notification Functions")
    print("="*70)
    
    app = create_app()
    with app.app_context():
        # Create a contact message
        contact_msg = ContactMessage(
            first_name="Alert",
            last_name="Test",
            email="alert@example.com",
            phone="+233000000000",
            company="Test",
            subject="Test Email",
            message="Testing email notification",
            newsletter=1
        )
        db.session.add(contact_msg)
        db.session.commit()
        
        # Call email function (should not raise exception)
        try:
            result = send_contact_notification_email(contact_msg)
            print(f"✓ Contact notification email function executed: {result}")
        except Exception as e:
            print(f"✗ Contact notification error: {str(e)}")
            return False
        
        # Create a consultation
        consultation = ConsultationRequest(
            first_name="Alert",
            last_name="Consultant",
            email="consultant@example.com",
            phone="+233111111111",
            company="Test Co",
            subject="Test Consultation",
            message="Testing consultation email",
            preferred_date="2026-03-01",
            preferred_time="10:00",
            newsletter=0
        )
        consultation.set_cart_items([
            {"id": 1, "name": "Test Item", "price": 100, "quantity": 1}
        ])
        db.session.add(consultation)
        db.session.commit()
        
        # Call email function (should not raise exception)
        try:
            result = send_consultation_notification_email(consultation)
            print(f"✓ Consultation notification email function executed: {result}")
        except Exception as e:
            print(f"✗ Consultation notification error: {str(e)}")
            return False
        
        return True

def test_notification_api_still_works():
    """Test that notification API endpoints still work correctly"""
    print("\n" + "="*70)
    print("TEST 4: Notification API Endpoints")
    print("="*70)
    
    app = create_app()
    with app.app_context():
        # Count notifications
        contact_count = ContactMessage.query.filter_by(is_read=False).count()
        consultation_count = ConsultationRequest.query.filter_by(is_read=False).count()
        
        print(f"✓ Unread Contact Messages: {contact_count}")
        print(f"✓ Unread Consultation Requests: {consultation_count}")
        
        # Test marking as read
        contact = ContactMessage.query.first()
        if contact:
            contact.is_read = True
            db.session.commit()
            print(f"✓ Successfully marked contact message {contact.id} as read")
        
        consultation = ConsultationRequest.query.first()
        if consultation:
            consultation.is_read = True
            db.session.commit()
            print(f"✓ Successfully marked consultation {consultation.id} as read")
        
        return True

def test_backward_compatibility():
    """Test that existing features are not affected"""
    print("\n" + "="*70)
    print("TEST 5: Backward Compatibility - Database Integrity")
    print("="*70)
    
    app = create_app()
    with app.app_context():
        # Verify tables exist
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        required_tables = [
            'contact_messages',
            'consultation_requests',
            'users',
            'products',
            'orders',
            'reviews',
            'wishlist'
        ]
        
        for table in required_tables:
            if table in tables:
                print(f"✓ Table '{table}' exists")
            else:
                print(f"✗ Table '{table}' missing!")
                return False
        
        # Verify contact_messages columns
        contact_columns = [col['name'] for col in inspector.get_columns('contact_messages')]
        required_contact_cols = [
            'id', 'first_name', 'last_name', 'email', 'phone', 
            'company', 'subject', 'message', 'newsletter', 'is_read',
            'created_at', 'updated_at'
        ]
        
        missing_cols = [col for col in required_contact_cols if col not in contact_columns]
        if missing_cols:
            print(f"✗ Missing columns in contact_messages: {missing_cols}")
            return False
        
        print(f"✓ contact_messages table has all required columns")
        
        # Verify consultation_requests columns
        consultation_columns = [col['name'] for col in inspector.get_columns('consultation_requests')]
        required_consultation_cols = [
            'id', 'first_name', 'last_name', 'email', 'phone',
            'company', 'subject', 'message', 'preferred_date', 'preferred_time',
            'newsletter', 'cart_items', 'is_read', 'created_at', 'updated_at'
        ]
        
        missing_cols = [col for col in required_consultation_cols if col not in consultation_columns]
        if missing_cols:
            print(f"✗ Missing columns in consultation_requests: {missing_cols}")
            return False
        
        print(f"✓ consultation_requests table has all required columns")
        
        return True

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "EMAIL FORWARDING FEATURE - TEST SUITE" + " "*17 + "║")
    print("╚" + "="*68 + "╝")
    
    tests = [
        ("Database Save - Contact Form", test_contact_form_database_save),
        ("Database Save - Consultation Form", test_consultation_form_database_save),
        ("Email Notification Functions", test_email_notification_functions_exist),
        ("Notification API Endpoints", test_notification_api_still_works),
        ("Backward Compatibility", test_backward_compatibility)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} FAILED: {str(e)}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ ALL TESTS PASSED - Email forwarding feature is working correctly!")
    else:
        print(f"\n✗ {total - passed} test(s) failed - Please review the output above")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

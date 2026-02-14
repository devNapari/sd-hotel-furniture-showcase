# Email Forwarding - Technical API Reference

## Overview

This document provides technical details for developers integrating with the email forwarding system.

---

## API Functions

### `send_email_async(msg)`

**Location:** `routes/api.py`

**Purpose:** Send Flask-Mail Message object asynchronously in a background thread

**Parameters:**
- `msg` (Message): Flask-Mail Message object with recipients, subject, and html body

**Returns:** None (fires and forgets)

**Implementation:**
```python
def send_email_async(msg):
    """Send email asynchronously without blocking the request"""
    try:
        with current_app.app_context():
            mail.send(msg)
            print(f"[EMAIL] Successfully sent to {msg.recipients}")
    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send email: {str(e)}")
```

**Usage:**
```python
from routes.api import send_email_async
from flask_mail import Message

msg = Message(
    subject="Test Email",
    recipients=["admin@example.com"],
    html="<h1>Test</h1>"
)

thread = threading.Thread(target=send_email_async, args=(msg,))
thread.daemon = True
thread.start()
```

---

### `send_contact_notification_email(contact_message)`

**Location:** `routes/api.py`

**Purpose:** Send professional HTML email notification for new contact form submission

**Parameters:**
- `contact_message` (ContactMessage): Database model instance

**Returns:** Boolean
- `True` if email was queued for sending
- `False` if email could not be prepared

**HTML Template Elements:**
- Contact information (name, email, phone, company)
- Message subject and content
- Newsletter signup status
- Timestamp and message ID
- Admin call-to-action box

**Example:**
```python
from models.notification import ContactMessage
from routes.api import send_contact_notification_email

# After creating and saving contact message
contact_msg = ContactMessage(
    first_name="John",
    last_name="Doe",
    email="john@example.com",
    phone="+233123456789",
    company="ACME Corp",
    subject="Product Inquiry",
    message="Tell me about your furniture",
    newsletter=1
)
db.session.add(contact_msg)
db.session.commit()

# Send email notification
success = send_contact_notification_email(contact_msg)
```

**Email Subject:** `New Contact Message: [subject]`

**Email Recipients:** Taken from `current_app.config.get('ADMIN_EMAIL')`

---

### `send_consultation_notification_email(consultation_request)`

**Location:** `routes/api.py`

**Purpose:** Send professional HTML email with consultation details and cart items

**Parameters:**
- `consultation_request` (ConsultationRequest): Database model instance

**Returns:** Boolean
- `True` if email was queued for sending
- `False` if email could not be prepared

**HTML Template Elements:**
- Consultation information (name, email, phone, company)
- Message subject and content
- Preferred date and time
- Newsletter signup status
- **Cart items table:**
  - Product name, quantity, price, item total
  - Grand total in GHS
- Timestamp and request ID
- Admin call-to-action box

**Example:**
```python
from models.notification import ConsultationRequest
from routes.api import send_consultation_notification_email

# After creating and saving consultation
consultation = ConsultationRequest(
    first_name="Jane",
    last_name="Smith",
    email="jane@example.com",
    phone="+233987654321",
    company="XYZ Ltd",
    subject="Custom Furniture Design",
    message="Need office furniture",
    preferred_date="2026-02-20",
    preferred_time="14:30",
    newsletter=0
)

# Add cart items
cart_items = [
    {"id": 1, "name": "Executive Desk", "price": 500.00, "quantity": 1},
    {"id": 2, "name": "Office Chair", "price": 150.00, "quantity": 2}
]
consultation.set_cart_items(cart_items)

db.session.add(consultation)
db.session.commit()

# Send email with cart table
success = send_consultation_notification_email(consultation)
```

**Email Subject:** `New Consultation Request: [subject]`

**Email Recipients:** Taken from `current_app.config.get('ADMIN_EMAIL')`

**Cart Items Handling:**
```python
# Retrieve cart items
cart_items = consultation.get_cart_items()  # Returns list of dicts

# Calculate totals
total = sum(item['price'] * item['quantity'] for item in cart_items)
```

---

## REST API Endpoints

### POST /api/contact

**Description:** Submit contact form and trigger email notification

**Request:**
```json
{
  "firstName": "John",
  "lastName": "Doe",
  "email": "john@example.com",
  "phone": "+233123456789",
  "company": "ACME Corp",
  "subject": "Product Inquiry",
  "message": "I'm interested in your furniture",
  "newsletter": true
}
```

**Response (Success):**
```json
{
  "status": "success",
  "message": "Your message has been received! We will get back to you soon.",
  "id": 1
}
```

**Response (Validation Error):**
```json
{
  "status": "error",
  "message": "firstName is required"
}
```

**Flow:**
1. Validate required fields: firstName, lastName, email, subject, message
2. Convert newsletter checkbox value to boolean (0 or 1)
3. Save to `contact_messages` table
4. Call `send_contact_notification_email()` in background thread
5. Return success immediately (don't wait for email)
6. Email is sent asynchronously

**Side Effects:**
- Creates record in `contact_messages` table
- Queues email notification (might fail silently if SMTP down)
- Logs email delivery status

---

### POST /api/consultation

**Description:** Submit consultation form with cart items and trigger email notification

**Request:**
```json
{
  "firstName": "Jane",
  "lastName": "Smith",
  "email": "jane@example.com",
  "phone": "+233987654321",
  "company": "XYZ Ltd",
  "subject": "Custom Furniture Design",
  "message": "Need office furniture for new location",
  "preferredDate": "2026-02-20",
  "preferredTime": "14:30",
  "newsletter": false,
  "cartItems": [
    {
      "id": 1,
      "name": "Executive Desk",
      "price": 500.00,
      "quantity": 1
    },
    {
      "id": 2,
      "name": "Conference Table",
      "price": 1500.00,
      "quantity": 1
    }
  ]
}
```

**Response (Success):**
```json
{
  "status": "success",
  "message": "Your consultation request has been received! We will contact you within 24 hours.",
  "id": 2
}
```

**Response (Validation Error):**
```json
{
  "status": "error",
  "message": "preferredDate is required"
}
```

**Flow:**
1. Validate required fields: firstName, lastName, email, phone, subject, message, preferredDate, preferredTime
2. Convert newsletter checkbox value to boolean (0 or 1)
3. Save to `consultation_requests` table
4. Serialize cart items to JSON and store in database
5. Call `send_consultation_notification_email()` in background thread
6. Return success immediately (don't wait for email)
7. Email with cart table is sent asynchronously

**Side Effects:**
- Creates record in `consultation_requests` table with cart_items as JSON
- Queues email notification with cart items table
- Logs email delivery status
- Logs cart total for debugging

---

## Database Models

### ContactMessage

**File:** `models/notification.py`

**Table:** `contact_messages`

**Fields:**
```python
id: Integer (Primary Key)
first_name: String(100)
last_name: String(100)
email: String(120)
phone: String(20)
company: String(100)
subject: String(255)
message: Text
newsletter: Integer (0 or 1, Boolean representation)
is_read: Integer (0 or 1, Boolean representation)
created_at: DateTime
updated_at: DateTime
```

**Methods:**
```python
to_dict() -> dict
    Returns JSON-serializable representation of the contact message
```

---

### ConsultationRequest

**File:** `models/notification.py`

**Table:** `consultation_requests`

**Fields:**
```python
id: Integer (Primary Key)
first_name: String(100)
last_name: String(100)
email: String(120)
phone: String(20)
company: String(100)
subject: String(255)
message: Text
preferred_date: String(10)  # YYYY-MM-DD format
preferred_time: String(5)   # HH:MM format
newsletter: Integer (0 or 1, Boolean representation)
cart_items: Text (JSON string)
is_read: Integer (0 or 1, Boolean representation)
created_at: DateTime
updated_at: DateTime
```

**Methods:**
```python
set_cart_items(items: list) -> None
    Serialize cart items list to JSON string and store in database

get_cart_items() -> list
    Retrieve and deserialize cart items from JSON string
    Returns list of dicts with format:
    [
        {"id": 1, "name": "Product", "price": 100, "quantity": 1},
        ...
    ]

to_dict() -> dict
    Returns JSON-serializable representation including deserialized cart items
```

---

## Configuration

### Environment Variables (.env)

```dotenv
# Email Server Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Admin Email (notification recipient)
ADMIN_EMAIL=admin@yourdomain.com

# Default Sender (optional, defaults to MAIL_USERNAME)
MAIL_DEFAULT_SENDER=noreply@yourdomain.com
```

### Config Class (config.py)

```python
class Config:
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@sdhotelfurniture.com'
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'admin@sdhotelfurniture.com'
```

---

## Error Handling

### Email Sending Failures

Email failures are logged but never crash the application:

```
[EMAIL ERROR] Failed to send email: SMTPAuthenticationError('Invalid credentials')
[EMAIL ERROR] Failed to send email: SMTPServerDisconnected('Connection refused')
[EMAIL ERROR] Failed to send email: Connection timeout
```

### Database Errors

Database errors in form submission are caught and returned to client:

```json
{
  "status": "error",
  "message": "Error saving your message. Please try again."
}
```

### Configuration Errors

If admin email or mail instance is not configured:

```
[EMAIL] Skipping email - Admin email: None, Mail: None
```

---

## Performance Considerations

### Request Blocking

✅ **Form submission is NOT blocked by email sending**

```
Request arrives
    ↓
Process form (save to DB) ~50ms
    ↓
Return 200 response (instantly) ← User sees success
    ↓
[Background] Email sent asynchronously ~1-5 seconds
```

### Database Load

- Two additional tables: `contact_messages`, `consultation_requests`
- Indexes on: `email`, `is_read`, `created_at`
- Query performance: O(1) for inserts, O(log n) for reads

### Memory Usage

- One thread created per email sent
- Threads are daemon threads (don't prevent shutdown)
- Minimal memory overhead (~1MB per thread)

### Network Usage

- SMTP connection pool managed by Flask-Mail
- One connection per email (reused if available)
- Typical email size: 2-5KB

---

## Testing

### Unit Test Example

```python
from app import create_app, db
from models.notification import ContactMessage
from routes.api import send_contact_notification_email

def test_contact_email():
    app = create_app()
    with app.app_context():
        # Create message
        msg = ContactMessage(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            phone="+233123456789",
            company="Test",
            subject="Test",
            message="Test message",
            newsletter=1
        )
        db.session.add(msg)
        db.session.commit()
        
        # Send email
        result = send_contact_notification_email(msg)
        assert result == True
```

### Integration Test Example

```python
from flask import json

def test_contact_form_submission(client):
    """Test POST /api/contact endpoint"""
    response = client.post('/api/contact', 
        json={
            'firstName': 'Test',
            'lastName': 'User',
            'email': 'test@example.com',
            'subject': 'Test',
            'message': 'Test message'
        }
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['id'] > 0
```

---

## Logging

### Email Delivery Logs

```
[EMAIL] Successfully sent to ['admin@example.com']
[EMAIL ERROR] Failed to send email: Connection refused
[EMAIL] Skipping email - Admin email: None, Mail: None
```

### Form Submission Logs

```
[CONTACT FORM] New message from John Doe (john@example.com)
  Subject: Product Inquiry
  Message: I'm interested in your furniture...

[CONSULTATION] New request from Jane Smith (jane@example.com)
  Subject: Custom Design
  Preferred Date/Time: 2026-02-20 @ 14:30
  Message: Need office furniture...
  Cart Items (2 total): $2000.00
```

---

## Debugging

### Check Email Configuration

```python
from app import create_app

app = create_app()
print(f"MAIL_SERVER: {app.config['MAIL_SERVER']}")
print(f"MAIL_PORT: {app.config['MAIL_PORT']}")
print(f"ADMIN_EMAIL: {app.config.get('ADMIN_EMAIL')}")
```

### Test Email Sending

```python
from flask_mail import Message

msg = Message(
    subject="Test Email",
    recipients=[app.config.get('ADMIN_EMAIL')],
    html="<h1>Test</h1>"
)

try:
    mail.send(msg)
    print("✓ Email sent successfully")
except Exception as e:
    print(f"✗ Email failed: {e}")
```

### Query Database

```python
from models.notification import ContactMessage, ConsultationRequest

messages = ContactMessage.query.all()
print(f"Total contact messages: {len(messages)}")

consultations = ConsultationRequest.query.all()
print(f"Total consultations: {len(consultations)}")
```

---

## Summary

✅ **Complete email forwarding system with:**
- Professional HTML email templates
- Asynchronous non-blocking delivery
- Database storage for reliability
- Cart item rendering in consultation emails
- Comprehensive error handling
- Production-ready implementation

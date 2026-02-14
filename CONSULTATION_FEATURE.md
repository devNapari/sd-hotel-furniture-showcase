# Book Consultation Feature - Implementation Guide

## Overview
The "Book Consultation" feature replaces the traditional checkout process with a consultation request system. When users add items to their shopping cart, instead of proceeding to checkout, they can book a consultation to discuss their furniture needs with the AM AWUNI team.

---

## Feature Location

### Shopping Cart (Offcanvas)
- **File:** [`templates/shop.html`](templates/shop.html:199)
- **Button Location:** Shopping cart footer (offcanvas sidebar)
- **Trigger:** Click "Book Consultation" button

---

## How It Works

### 1. User Journey
1. User browses products on the shop page
2. User adds items to shopping cart
3. Shopping cart opens (offcanvas sidebar on the right)
4. User clicks "Book Consultation" button
5. Consultation modal opens with a form
6. User fills out the form with their details
7. Form submission sends email to admin
8. User receives confirmation message

### 2. Cart Items Integration
When the consultation form is submitted, the selected cart items are automatically included in the message sent to the admin. This allows the team to see exactly which products the customer is interested in.

---

## Form Fields

### Required Fields
- **First Name** - Customer's first name
- **Last Name** - Customer's last name
- **Email Address** - Contact email
- **Phone Number** - Contact phone (WhatsApp compatible)
- **Subject** - Type of inquiry (dropdown)
- **Message** - Detailed requirements

### Optional Fields
- **Company/Organization Name** - Business name if applicable
- **Newsletter Subscription** - Opt-in checkbox

### Subject Options
1. **Furniture Inquiry** - General furniture questions
2. **Construction Project** - Construction services
3. **Request a Quote** - Pricing information
4. **Custom Design** - Custom furniture design
5. **Other** - Other inquiries

---

## Email Delivery

### Recipient
- **Admin Email:** sirenapari@gmail.com

### Email Format
The consultation request is sent as a professionally formatted HTML email containing:

#### Email Header
- Subject: "Consultation Request: [Subject]"
- Branded header with AM AWUNI FURNITURE & CONSTRUCTION logo colors

#### Email Content
- Customer name and contact information
- Phone number (clickable for direct calling)
- Email address (clickable for direct reply)
- Company/organization name
- Subject category
- Detailed message
- **Selected cart items** (if any)
- Newsletter subscription status
- Submission timestamp

#### Email Footer
- Submission date and time (UTC)
- Action reminder: "Please respond within 24 hours"
- Automated message disclaimer

---

## Technical Implementation

### Frontend (JavaScript)
**File:** [`templates/shop.html`](templates/shop.html:273)

```javascript
// Form submission handler
document.getElementById('submitConsultation').addEventListener('click', async function() {
    // Validate form
    // Get form data
    // Add cart items to message
    // Send POST request to /api/consultation
    // Show success/error message
});
```

### Backend (Flask API)
**File:** [`routes/api.py`](routes/api.py:448)

```python
@api_bp.route('/consultation', methods=['POST'])
def submit_consultation_form():
    # Validate required fields
    # Extract form data
    # Create email message
    # Send email to admin
    # Return success response
```

### Email Service
- **Library:** Flask-Mail
- **Configuration:** Set in `app.py` or `config.py`
- **Sender:** noreply@amawunifurniture.com
- **Recipient:** sirenapari@gmail.com

---

## User Experience Features

### 1. Form Validation
- Client-side validation for required fields
- Email format validation
- Phone number format validation
- Real-time error messages

### 2. Loading States
- Button shows spinner during submission
- Button text changes to "Sending..."
- Button disabled during submission

### 3. Success Feedback
- Green success alert with checkmark icon
- Confirmation message: "Your consultation request has been sent. We'll contact you within 24 hours!"
- Form automatically resets
- Modal closes after 3 seconds

### 4. Error Handling
- Red error alert with warning icon
- Clear error messages
- Retry option available
- Fallback contact information

### 5. Cart Integration
- Cart items automatically included in message
- Item names and quantities listed
- Helps admin understand customer needs

---

## Email Configuration

### Required Environment Variables
```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@amawunifurniture.com
```

### Gmail Setup (if using Gmail)
1. Enable 2-Factor Authentication
2. Generate App Password
3. Use App Password in MAIL_PASSWORD
4. Allow less secure apps (if needed)

### Alternative Email Services
- **SendGrid** - Recommended for production
- **Mailgun** - Good for high volume
- **Amazon SES** - Cost-effective
- **SMTP2GO** - Easy setup

---

## Testing

### Manual Testing Checklist
- [ ] Open shop page
- [ ] Add items to cart
- [ ] Click "Book Consultation" button
- [ ] Verify modal opens
- [ ] Fill out all required fields
- [ ] Submit form
- [ ] Verify success message appears
- [ ] Check admin email (sirenapari@gmail.com)
- [ ] Verify email contains all information
- [ ] Verify cart items are included
- [ ] Test with empty cart
- [ ] Test form validation
- [ ] Test error handling

### Test Data
```json
{
  "firstName": "John",
  "lastName": "Doe",
  "email": "john.doe@example.com",
  "phone": "+233 123 456 789",
  "company": "Test Company Ltd",
  "subject": "furniture",
  "message": "I'm interested in purchasing office furniture for our new building.",
  "newsletter": true
}
```

---

## Customization Options

### 1. Change Admin Email
**File:** [`routes/api.py`](routes/api.py:478)
```python
recipients=['your-new-email@example.com']
```

### 2. Modify Form Fields
**File:** [`templates/shop.html`](templates/shop.html:234)
- Add new fields to the form
- Update validation in JavaScript
- Update email template to include new fields

### 3. Change Email Template
**File:** [`routes/api.py`](routes/api.py:495)
- Modify HTML email template
- Change colors, fonts, layout
- Add company logo

### 4. Adjust Response Time
**File:** [`templates/shop.html`](templates/shop.html:234)
- Change "24 hours" to your preferred timeframe
- Update email footer message

---

## Troubleshooting

### Email Not Sending
1. **Check email configuration** in `config.py` or `.env`
2. **Verify SMTP credentials** are correct
3. **Check spam folder** in recipient email
4. **Review server logs** for error messages
5. **Test with different email service**

### Form Not Submitting
1. **Check browser console** for JavaScript errors
2. **Verify API endpoint** is accessible
3. **Check network tab** for failed requests
4. **Ensure all required fields** are filled

### Modal Not Opening
1. **Verify Bootstrap JS** is loaded
2. **Check for JavaScript conflicts**
3. **Ensure modal HTML** is present
4. **Check button data attributes**

---

## Security Considerations

### 1. Email Validation
- Server-side validation of email format
- Prevention of email injection attacks
- Sanitization of user input

### 2. Rate Limiting
Consider implementing rate limiting to prevent spam:
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=get_remote_address)

@api_bp.route('/consultation', methods=['POST'])
@limiter.limit("5 per hour")
def submit_consultation_form():
    # ... existing code
```

### 3. CAPTCHA
For production, consider adding reCAPTCHA:
- Google reCAPTCHA v3
- hCaptcha
- Cloudflare Turnstile

---

## Future Enhancements

### Potential Improvements
1. **SMS Notifications** - Send SMS to admin when consultation requested
2. **Calendar Integration** - Allow customers to book specific time slots
3. **File Uploads** - Let customers upload reference images
4. **Live Chat** - Add real-time chat option
5. **WhatsApp Integration** - Direct WhatsApp messaging
6. **CRM Integration** - Sync with customer relationship management system
7. **Auto-Response** - Send confirmation email to customer
8. **Admin Dashboard** - View all consultation requests in admin panel

---

## Support

### Contact Information
- **Email:** amfurnitureandconstruction@gmail.com
- **Phone:** +233 538 833 723
- **WhatsApp:** +233 538 833 723 / +233 248 962 214

### Documentation
- [`README.md`](README.md:1) - Project overview
- [`SETUP_GUIDE.md`](SETUP_GUIDE.md:1) - Installation guide
- [`ADMIN_GUIDE.md`](ADMIN_GUIDE.md:1) - Admin panel guide
- [`REBRANDING_SUMMARY.md`](REBRANDING_SUMMARY.md:1) - Rebranding details

---

**Last Updated:** November 13, 2024  
**Version:** 1.0  
**Feature Status:** ✅ Active
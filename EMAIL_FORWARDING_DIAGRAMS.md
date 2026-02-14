# Email Forwarding System - Architecture & Data Flow Diagrams

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        WEB APPLICATION                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FRONTEND (HTML/JavaScript)                                    │
│  ├─ Contact Form                                               │
│  └─ Consultation Form                                          │
│           │                                                     │
│           ▼                                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │         API LAYER (Flask Routes)                       │   │
│  │  POST /api/contact                                     │   │
│  │  POST /api/consultation                                │   │
│  └─────────────────────────────────────────────────────────┘   │
│           │              │                                      │
│           │              └──────────────────┐                   │
│           ▼                                  ▼                   │
│  ┌──────────────────┐          ┌──────────────────────────┐    │
│  │  DATABASE LAYER  │          │  EMAIL LAYER (Threading)│    │
│  │                  │          │                          │    │
│  │ contact_messages │          │ send_email_async()      │    │
│  │ consultation_... │          │ [Background Thread]     │    │
│  └──────────────────┘          └──────────────────────────┘    │
│           ▲                                  │                  │
│           │                                  ▼                  │
│           │                      ┌──────────────────────────┐   │
│           └──────────────────────│ SMTP Server             │   │
│                                  │ smtp.gmail.com:587      │   │
│                                  └──────────────────────────┘   │
│                                           │                     │
└───────────────────────────────────────────┼─────────────────────┘
                                            │
                                            ▼
                                  ┌──────────────────┐
                                  │  ADMIN EMAIL     │
                                  │  sirenapari@     │
                                  │  gmail.com       │
                                  └──────────────────┘
```

---

## Request Flow Diagram

### Contact Form Submission

```
┌──────────────────────────────────────────────────────────────────┐
│ USER SUBMITS CONTACT FORM                                        │
│ (Name, Email, Phone, Company, Subject, Message, Newsletter)     │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │ [TIME: ~10ms] POST /api/contact        │
        │ - Validate required fields             │
        │ - Convert newsletter checkbox          │
        └─────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │ [TIME: ~50ms] SAVE TO DATABASE         │
        │ - Create ContactMessage record         │
        │ - Insert into contact_messages table   │
        │ - COMMIT transaction ✓                │
        └─────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │ [TIME: <1ms] RETURN SUCCESS RESPONSE   │
        │ {                                       │
        │   "status": "success",                 │
        │   "message": "Message received",      │
        │   "id": 1                             │
        │ }                                       │
        └─────────────────────────────────────────┘
                    │
         ┌──────────┴──────────────┐
         │                         │
         ▼                         ▼
    [USER SIDE]          [BACKGROUND THREAD]
    Show success         (Non-blocking)
    message              │
                         ▼
                    ┌──────────────────┐
                    │ [TIME: ~100ms]   │
                    │ Format HTML      │
                    │ Email            │
                    └──────────────────┘
                         │
                         ▼
                    ┌──────────────────┐
                    │ [TIME: ~2-5s]    │
                    │ Connect to SMTP  │
                    │ Send Email       │
                    └──────────────────┘
                         │
                         ▼
                    Admin receives
                    email in inbox
```

**Key Insight:** User gets feedback at ~50ms (form saved), doesn't wait for email (2-5 seconds)

---

### Consultation Form Submission (with Cart)

```
┌──────────────────────────────────────────────────────────────────┐
│ USER SUBMITS CONSULTATION FORM                                   │
│ (Name, Email, Phone, Company, Subject, Message,                │
│  Preferred Date, Preferred Time, Newsletter, Cart Items)        │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │ [TIME: ~10ms] POST /api/consultation    │
        │ - Validate required fields             │
        │ - Convert newsletter checkbox          │
        │ - Validate cart items array            │
        └─────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │ [TIME: ~50ms] SAVE TO DATABASE         │
        │ - Create ConsultationRequest record    │
        │ - Serialize cart items to JSON         │
        │ - Insert into consultation_requests    │
        │ - COMMIT transaction ✓                │
        └─────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │ [TIME: <1ms] RETURN SUCCESS RESPONSE   │
        │ {                                       │
        │   "status": "success",                 │
        │   "message": "Request received",      │
        │   "id": 2                             │
        │ }                                       │
        └─────────────────────────────────────────┘
                    │
         ┌──────────┴──────────────────────────────┐
         │                                         │
         ▼                                         ▼
    [USER SIDE]                    [BACKGROUND THREAD]
    Show success                   (Non-blocking)
    message                        │
                                   ▼
                            ┌──────────────────┐
                            │ [TIME: ~100ms]   │
                            │ Get cart items   │
                            │ from JSON        │
                            └──────────────────┘
                                   │
                                   ▼
                            ┌──────────────────┐
                            │ [TIME: ~50ms]    │
                            │ Build HTML       │
                            │ Email with       │
                            │ cart table       │
                            └──────────────────┘
                                   │
                                   ▼
                            ┌──────────────────┐
                            │ [TIME: ~2-5s]    │
                            │ Send email to    │
                            │ admin            │
                            └──────────────────┘
                                   │
                                   ▼
                            Admin receives
                            email with
                            cart details
```

---

## Database Interaction Diagram

### Contact Message Flow

```
contact_messages Table
┌─────────────────────────────────────────────────────────┐
│ id | first_name | last_name | email | phone | ...     │
├─────────────────────────────────────────────────────────┤
│ 1  │ John       │ Doe       │ j@... │ +233  │ ...     │  ← Inserted
│ 2  │ Jane       │ Smith     │ j@... │ +233  │ ...     │  ← Inserted
│ 3  │ Test       │ User      │ t@... │ +233  │ ...     │  ← Inserted
└─────────────────────────────────────────────────────────┘
     ▲
     │
     └── INSERT (from /api/contact)
         VALUES (first_name, last_name, email, phone, 
                 company, subject, message, newsletter, 
                 is_read, created_at, updated_at)
```

### Consultation Request Flow

```
consultation_requests Table
┌─────────────────────────────────────────────────────────────┐
│ id | first_name | ... | cart_items (JSON) | is_read | ... │
├─────────────────────────────────────────────────────────────┤
│ 1  │ Jane       │ ... │ [{"id": 1, ...}]  │ 0       │ ... │  ← Inserted
│ 2  │ John       │ ... │ [{"id": 2, ...}]  │ 0       │ ... │  ← Inserted
└─────────────────────────────────────────────────────────────┘
     ▲
     │
     └── INSERT (from /api/consultation)
         VALUES (first_name, last_name, email, phone,
                 company, subject, message, preferred_date,
                 preferred_time, newsletter, cart_items [JSON],
                 is_read, created_at, updated_at)

Cart Items JSON Format:
[
  {"id": 1, "name": "Executive Desk", "price": 500, "quantity": 1},
  {"id": 2, "name": "Office Chair", "price": 150, "quantity": 2}
]
```

---

## Email Template Structure Diagram

### Contact Email HTML Structure

```
┌────────────────────────────────────────────────┐
│         <html><body>                           │
├────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────┐   │
│  │ HEADER                                 │   │
│  │ "New Contact Message"                  │   │
│  │ (Gold border-bottom)                   │   │
│  └────────────────────────────────────────┘   │
│                                                │
│  From: {first_name} {last_name}                │
│  Email: {email}                                │
│  Phone: {phone}                                │
│  Company: {company}                            │
│  Subject: {subject}                            │
│  Newsletter: {Yes/No}                          │
│                                                │
│  ┌────────────────────────────────────────┐   │
│  │ MESSAGE SECTION                        │   │
│  │ (Gray background, gold left border)    │   │
│  │ {full message text}                    │   │
│  └────────────────────────────────────────┘   │
│                                                │
│  Received: {created_at}                       │
│  Message ID: #{id}                             │
│                                                │
│  ┌────────────────────────────────────────┐   │
│  │ ACTION REQUIRED BOX                    │   │
│  │ (Light gray background)                │   │
│  │                                        │   │
│  │ ⚠️ ACTION REQUIRED:                    │   │
│  │ Log in to admin dashboard to view      │   │
│  │ and respond to this message            │   │
│  └────────────────────────────────────────┘   │
│                                                │
└────────────────────────────────────────────────┘
```

### Consultation Email HTML Structure

```
┌────────────────────────────────────────────────┐
│         <html><body>                           │
├────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────┐   │
│  │ HEADER                                 │   │
│  │ "New Consultation Request"             │   │
│  │ (Gold border-bottom)                   │   │
│  └────────────────────────────────────────┘   │
│                                                │
│  From: {first_name} {last_name}                │
│  Email: {email}                                │
│  Phone: {phone}                                │
│  Company: {company}                            │
│  Subject: {subject}                            │
│                                                │
│  CONSULTATION DETAILS:                         │
│  Preferred Date: {preferred_date}              │
│  Preferred Time: {preferred_time}              │
│  Newsletter: {Yes/No}                          │
│                                                │
│  ┌────────────────────────────────────────┐   │
│  │ MESSAGE SECTION                        │   │
│  │ (Gray background, gold left border)    │   │
│  │ {full message text}                    │   │
│  └────────────────────────────────────────┘   │
│                                                │
│  ┌────────────────────────────────────────┐   │
│  │ CART ITEMS TABLE                       │   │
│  │                                        │   │
│  │ Product        │ Qty │ Price  │ Total │   │
│  │ ─────────────┼─────┼────────┼─────  │   │
│  │ Item 1       │  1  │ 500.00 │ 500   │   │
│  │ Item 2       │  2  │ 150.00 │ 300   │   │
│  │ ─────────────┼─────┼────────┼─────  │   │
│  │ TOTAL        │     │        │ 800   │   │
│  └────────────────────────────────────────┘   │
│                                                │
│  Received: {created_at}                       │
│  Request ID: #{id}                             │
│                                                │
│  ┌────────────────────────────────────────┐   │
│  │ ACTION REQUIRED BOX                    │   │
│  │ (Light gray background)                │   │
│  │                                        │   │
│  │ ⚠️ ACTION REQUIRED:                    │   │
│  │ Log in to admin dashboard to view      │   │
│  │ and respond to this request            │   │
│  └────────────────────────────────────────┘   │
│                                                │
└────────────────────────────────────────────────┘
```

---

## Function Call Stack

### When /api/contact is called:

```
HTTP Request: POST /api/contact
    ↓
submit_contact_form()
    ├─ Parse JSON request
    ├─ Validate required fields
    ├─ Convert newsletter: 'on' → 1 (boolean)
    ├─ Create ContactMessage object
    ├─ db.session.add(contact_msg)
    ├─ db.session.commit()          ← Data is now persistent ✓
    ├─ Print console log
    ├─ Call: send_contact_notification_email(contact_msg)
    │  └─ Returns True/False, doesn't block
    └─ return jsonify({success})    ← User gets response ~50ms
           ↓
    [Meanwhile, in background thread...]
    send_contact_notification_email()
        ├─ Get ADMIN_EMAIL from config
        ├─ Check if email configured
        ├─ Create HTML email body
        ├─ Create Message object
        ├─ Spawn async thread:
        │  └─ send_email_async(msg)
        │     ├─ Get app context
        │     ├─ mail.send(msg)      ← SMTP connection
        │     └─ Log result
        └─ Return True
```

### When /api/consultation is called:

```
HTTP Request: POST /api/consultation
    ↓
submit_consultation_form()
    ├─ Parse JSON request
    ├─ Validate required fields
    ├─ Convert newsletter: 'on' → 1 (boolean)
    ├─ Create ConsultationRequest object
    ├─ Call: consultation.set_cart_items(cart_items)
    │  └─ Serialize cart to JSON and store
    ├─ db.session.add(consultation)
    ├─ db.session.commit()          ← Data is now persistent ✓
    ├─ Calculate cart total
    ├─ Print console log
    ├─ Call: send_consultation_notification_email(consultation)
    │  └─ Returns True/False, doesn't block
    └─ return jsonify({success})    ← User gets response ~50ms
           ↓
    [Meanwhile, in background thread...]
    send_consultation_notification_email()
        ├─ Get ADMIN_EMAIL from config
        ├─ Check if email configured
        ├─ Get cart items: consultation.get_cart_items()
        │  └─ Deserialize JSON → list
        ├─ Build cart HTML table
        │  ├─ Header row
        │  ├─ Item rows (with calculations)
        │  └─ Total row
        ├─ Create HTML email body (with table)
        ├─ Create Message object
        ├─ Spawn async thread:
        │  └─ send_email_async(msg)
        │     ├─ Get app context
        │     ├─ mail.send(msg)      ← SMTP connection
        │     └─ Log result
        └─ Return True
```

---

## Performance Timeline

### Optimal Case (SMTP responds quickly)

```
0ms     ├─ Request arrives
10ms    │
20ms    │  Parse & Validate
30ms    │
40ms    │  Database Save
50ms    ├─ ✓ SUCCESS RESPONSE (User sees message)
60ms    │
        │  Background thread continues...
100ms   │  Email HTML formatted
200ms   │
1000ms  │
2000ms  │
3000ms  ├─ Email sent to Gmail
4000ms  │
5000ms  │  ✓ Admin receives email
```

### Timeout Case (SMTP slow/offline)

```
0ms     ├─ Request arrives
10ms    │
20ms    │  Parse & Validate
30ms    │
40ms    │  Database Save
50ms    ├─ ✓ SUCCESS RESPONSE (User sees message) ← DATA SAVED!
60ms    │
        │  Background thread continues...
100ms   │  Email HTML formatted
200ms   │
1000ms  │
2000ms  │
3000ms  │
4000ms  │
5000ms  ├─ [EMAIL TIMEOUT]
6000ms  │  [EMAIL ERROR] Failed to send email: timeout
7000ms  ├─ ✗ Email failed, BUT DATA STILL IN DATABASE!
```

**Key Point:** User success is based on database save, not email send!

---

## Error Handling Flow

```
Request arrives
    ↓
Try:
    ├─ Validate input
    ├─ Save to database
    ├─ Return success  ← SUCCESS PATH
    └─ Send email async (background)
        ├─ Format email
        ├─ Send SMTP
        └─ [If fails: Log error, continue]
        
Except:
    └─ Catch exception
        ├─ Rollback database
        ├─ Log error with details
        └─ Return error response to user
```

---

## Summary

**Architecture:** Layered (Frontend → API → Database → Email)  
**Data Flow:** Synchronous to DB, Asynchronous to Email  
**Performance:** ~50ms for user response, ~2-5s for email  
**Reliability:** Database first, email second  
**Error Impact:** Email failures don't affect form submission  

---

**All diagrams represent the actual implementation in EMAIL_FORWARDING_IMPLEMENTATION.md**

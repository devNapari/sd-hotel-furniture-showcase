# Gmail SMTP Troubleshooting Guide

## The Issue: "Connection unexpectedly closed"

This error typically occurs due to one of these Gmail-specific issues:

## Solutions to Try

### 1. Verify App Password (Most Common)

**Current Status**: The password format has spaces, but this might not be an actual App Password.

**Steps to Create a Real App Password**:

1. **Enable 2-Step Verification**:
   - Go to Google Account settings
   - Security → 2-Step Verification → Enable
   - Complete the setup process

2. **Generate App Password**:
   - Go to Google Account settings → Security
   - 2-Step Verification → App passwords
   - Select "Mail" and "Other (Custom name)"
   - Enter "SD Hotel Furniture" as the name
   - Copy the 16-character password (format: xxxx xxxx xxxx xxxx)
   - Update your `.env` file with this new password

### 2. Alternative: Enable Less Secure Apps (Not Recommended)

⚠️ **Warning**: Google is phasing out this option

1. Go to Google Account settings
2. Security → Less secure app access
3. Enable "Allow less secure apps"

### 3. Check Firewall/Network Issues

Corporate or home firewalls may block SMTP. Try:
- Test from a different network
- Disable VPN temporarily
- Check Windows Defender firewall settings

### 4. Test Different SMTP Ports

Sometimes Gmail blocks specific ports. Update `.env`:

**Try Port 465 (SSL instead of TLS)**:
```
MAIL_PORT=465
MAIL_USE_TLS=false
MAIL_USE_SSL=true
```

### 5. Temporary Workaround: Log File Only

For development, we can disable email sending temporarily and just log the emails:

## Quick Fix: Disable Email Sending (Development Only)

Update `routes/api.py` to comment out email sending temporarily:

```python
# In submit_contact_form() and submit_consultation_form()
# Comment out: mail.send(msg)
# Replace with: print("Email would be sent:", msg.subject)
```

## Testing Steps

1. **First**: Create a real App Password (Solution #1)
2. **If that doesn't work**: Try port 465 (Solution #4) 
3. **For development**: Use the temporary workaround (Solution #5)

## Gmail Security Considerations

- App Passwords expire if you change your Google account password
- Google may occasionally block suspicious connections
- Some corporate networks block external SMTP entirely

## Recommended Solution

**Create a proper Gmail App Password** - this is the most reliable solution and is what Gmail currently recommends for automated email sending.
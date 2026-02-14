# Email Configuration Guide for Contact Form

The contact form is now configured to send emails to **sirenapari@gmail.com** when users submit enquiries.

## Quick Setup

### Step 1: Install Flask-Mail

```bash
pip install Flask-Mail
```

### Step 2: Configure Gmail App Password

Since the contact form sends emails via Gmail, you need to set up an App Password:

1. **Go to your Google Account**: https://myaccount.google.com/
2. **Enable 2-Step Verification** (if not already enabled):
   - Go to Security → 2-Step Verification
   - Follow the setup process

3. **Create an App Password**:
   - Go to Security → 2-Step Verification → App passwords
   - Select "Mail" and "Other (Custom name)"
   - Name it "SD Hotel Furniture Contact Form"
   - Click "Generate"
   - **Copy the 16-character password** (you won't see it again)

### Step 3: Create .env File

Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```
### Step 4: Update Email Settings in .env

Edit the `.env` file and add your email credentials:

```env
# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=sirenapari@gmail.com
MAIL_PASSWORD=qlcm elyf ilvc ytvm
MAIL_DEFAULT_SENDER=noreply@sdhotelfurniture.com
```

**Important:**
- Use the **App Password** (16 characters), NOT your regular Gmail password
- Replace `your-gmail-address@gmail.com` with the Gmail account you want to send FROM
- Emails will be sent TO: `sirenapari@gmail.com` (hardcoded in the API)

### Step 5: Test the Contact Form

1. Start your Flask application:
   ```bash
   python app.py
   ```

2. Visit the contact page: `http://localhost:5000/contact`

3. Fill out and submit the form

4. Check `sirenapari@gmail.com` for the email

## Email Features

### What Gets Sent

When a user submits the contact form, an email is sent with:

- **Sender Information**: Name, email, phone, company
- **Subject**: The selected subject category
- **Message**: The user's message
- **Newsletter Status**: Whether they opted in
- **Timestamp**: When the form was submitted

### Email Format

The email includes both:
- **Plain text version** - For email clients that don't support HTML
- **HTML version** - Beautifully formatted with styling

### Sample Email

```
From: John Doe
Email: john@example.com
Phone: +1 234 567 8900
Company: ABC Hotels
Subject: Request a Quote

Message:
I'm interested in furnishing a new 50-room hotel.
Could you provide a quote for guest room furniture?

Newsletter: ✓ Subscribed
Submitted: November 13, 2025 at 07:40 UTC
```

## Troubleshooting

### "Authentication failed" Error

**Problem**: Gmail is rejecting the login

**Solutions**:
1. Make sure you're using an **App Password**, not your regular password
2. Verify 2-Step Verification is enabled on your Google account
3. Check that the email address in `MAIL_USERNAME` is correct
4. Try generating a new App Password

### "Connection refused" Error

**Problem**: Can't connect to Gmail's SMTP server

**Solutions**:
1. Check your internet connection
2. Verify firewall isn't blocking port 587
3. Try using port 465 with SSL instead:
   ```env
   MAIL_PORT=465
   MAIL_USE_TLS=false
   MAIL_USE_SSL=true
   ```

### Emails Not Arriving

**Check**:
1. Spam/Junk folder in sirenapari@gmail.com
2. Gmail's "All Mail" folder
3. Check Flask console for error messages
4. Verify the recipient email is correct in `routes/api.py`

### "Mail not configured" Message

**Problem**: Flask-Mail isn't initialized

**Solutions**:
1. Make sure Flask-Mail is installed: `pip install Flask-Mail`
2. Restart your Flask application
3. Check that `.env` file exists and has correct values

## Security Best Practices

### DO:
- ✅ Use App Passwords (never regular passwords)
- ✅ Keep `.env` file in `.gitignore`
- ✅ Use environment variables for sensitive data
- ✅ Enable 2-Step Verification on Gmail

### DON'T:
- ❌ Commit `.env` file to Git
- ❌ Share your App Password
- ❌ Use your regular Gmail password
- ❌ Hardcode credentials in code

## Alternative Email Providers

If you prefer not to use Gmail, you can use other providers:

### SendGrid
```env
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USERNAME=apikey
MAIL_PASSWORD=your-sendgrid-api-key
```

### Mailgun
```env
MAIL_SERVER=smtp.mailgun.org
MAIL_PORT=587
MAIL_USERNAME=postmaster@your-domain.mailgun.org
MAIL_PASSWORD=your-mailgun-password
```

### Amazon SES
```env
MAIL_SERVER=email-smtp.us-east-1.amazonaws.com
MAIL_PORT=587
MAIL_USERNAME=your-ses-smtp-username
MAIL_PASSWORD=your-ses-smtp-password
```

## Changing the Recipient Email

To send emails to a different address, edit `routes/api.py`:

```python
# Line ~320
msg = Message(
    subject=f'Contact Form: {subject}',
    sender='noreply@sdhotelfurniture.com',
    recipients=['your-new-email@example.com']  # Change this
)
```

## Production Deployment

For production, consider:

1. **Use a dedicated email service** (SendGrid, Mailgun, etc.)
2. **Set up SPF/DKIM records** for better deliverability
3. **Use a custom domain** for sender address
4. **Enable email logging** for debugging
5. **Add rate limiting** to prevent spam

## Testing Without Email

For development without email setup, the contact form will still work but show:
```
"Your message has been received. (Email not configured - check server logs)"
```

The form data will be logged to the console instead.

## Support

If you encounter issues:
1. Check Flask console for error messages
2. Verify all environment variables are set
3. Test with a simple email first
4. Review Gmail's security settings

---

**Contact Form is Ready!** Once configured, all enquiries will be sent to sirenapari@gmail.com automatically.
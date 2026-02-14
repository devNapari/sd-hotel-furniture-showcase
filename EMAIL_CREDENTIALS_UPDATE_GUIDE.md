# Email Credentials Configuration Guide

## Current Status
Your contact and consultation forms now **display an error message to users** when emails fail:
> "Sorry. Email Failed to reach us. Please Try again"

---

## Where to Update Email Credentials

### Step 1: Create or Locate Your `.env` File
The `.env` file should be in your **project root directory** (same folder as `app.py`):

```
c:\Users\zoe\Downloads\New folder\New folder\sd-hotel-furniture-showcase\.env
```

If the file doesn't exist, create it with these contents:

### Step 2: Add Email Configuration to `.env`

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=sirenapari@gmail.com
MAIL_PASSWORD=your-16-character-app-password-here
MAIL_DEFAULT_SENDER=noreply@sdhotelfurniture.com
```

---

## How to Get Your Gmail App Password

### Prerequisites
- You must have **2-Factor Authentication enabled** on your Google account
- Regular Gmail password will NOT work

### Steps to Generate App Password

1. **Go to Google Account:**
   - Visit: https://myaccount.google.com

2. **Enable 2-Step Verification (if not already done):**
   - Click **Security** in the left sidebar
   - Find "2-Step Verification"
   - Click it and follow the setup wizard

3. **Generate App Password:**
   - Go back to **Security** page
   - Scroll down to **App passwords** (only visible if 2-FA is enabled)
   - Select **Mail** and **Windows Computer** (or your device)
   - Click **Generate**
   - Google will show a 16-character password like: `qlcm elyf ilvc ytvm`

4. **Copy the password** (including the spaces)

### Step 3: Update Your `.env` File

Copy the 16-character password into your `.env` file:

```env
MAIL_PASSWORD=qlcm elyf ilvc ytvm
```

**Important:** Include the spaces exactly as Google shows them!

---

## File Locations to Check

### Main Email Configuration Files

| File | Path | Purpose |
|------|------|---------|
| **.env** | `root/` | **← UPDATE HERE** (email credentials) |
| config.py | `root/config.py` | Loads env variables (no changes needed) |
| routes/api.py | `root/routes/api.py` | Contact/Consultation endpoints (already updated) |
| app.py | `root/app.py` | Initializes Flask-Mail (no changes needed) |

### Example `.env` File Structure

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development

# Database
DATABASE_URL=sqlite:///hotel_furniture.db

# Email Configuration (UPDATE THIS SECTION)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=sirenapari@gmail.com
MAIL_PASSWORD=your-app-password-here
MAIL_DEFAULT_SENDER=noreply@sdhotelfurniture.com

# Other configs
ADMIN_EMAIL=admin@sdhotelfurniture.com
```

---

## Testing Your Configuration

### 1. Restart Flask Server
```bash
python app.py
```

### 2. Test Contact Form
1. Go to your website's contact page
2. Fill out and submit the form
3. **Success Case:**
   - User sees: "Your message has been sent successfully!"
   - Email arrives in your inbox (sirenapari@gmail.com)
   
4. **Failure Case:**
   - User sees: "Sorry. Email Failed to reach us. Please Try again"
   - Check server console for error details

### 3. Check Server Logs
When form is submitted, look for one of these messages:

**✅ Success:**
```
Contact form email sent successfully to ['sirenapari@gmail.com']
```

**❌ Failure:**
```
SMTP Connection Error: Connection unexpectedly closed
Form data that would have been emailed:
From: John Doe <john@example.com>
Subject: Inquiry
Message: ...
```

---

## Troubleshooting

### Error: "Connection unexpectedly closed"
- **Cause:** Invalid Gmail App Password
- **Fix:** 
  1. Generate a NEW App Password from Google Account
  2. Make sure you're using App Password, NOT regular Gmail password
  3. Include spaces exactly as shown
  4. Update `.env` and restart Flask

### Error: "Authentication failed"
- **Cause:** 2-FA not enabled or wrong email address
- **Fix:**
  1. Enable 2-Step Verification in Google Account
  2. Verify `MAIL_USERNAME` in `.env` matches your Gmail
  3. Generate new App Password

### Error: "No module named 'flask_mail'"
- **Cause:** Flask-Mail not installed
- **Fix:** Run in terminal:
  ```bash
  pip install flask-mail
  ```

### Still not working?
1. Check the `REQUIREMENTS.md` or `requirements.txt` for dependencies
2. Ensure Python virtual environment is activated
3. Check Flask server is running on correct port
4. Verify firewall allows outbound SMTP (port 587)

---

## Email Features

### Contact Form (`/api/contact`)
- **Recipients:** sirenapari@gmail.com
- **Error Message:** "Sorry. Email Failed to reach us. Please Try again"
- **Success Message:** "Your message has been sent successfully!"

### Consultation Form (`/api/consultation`)
- **Recipients:** sirenapari@gmail.com
- **Error Message:** "Sorry. Email Failed to reach us. Please Try again"
- **Success Message:** "Your consultation request has been sent successfully!"

---

## Quick Reference

**Email Address:** sirenapari@gmail.com  
**App Password:** [Your 16-character password with spaces]  
**Server:** smtp.gmail.com  
**Port:** 587  
**Use TLS:** Yes  

**Configuration File:** `.env` (in project root)

---

## Important Security Notes

⚠️ **NEVER commit `.env` to version control!**

Make sure your `.gitignore` includes:
```
.env
.env.local
```

The `.env` file contains sensitive credentials and should only exist on your local machine and production server.

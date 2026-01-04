# How to Set Up .env File

### Open and edit .env file

Edit the `.env` file and replace the placeholder values:

```env
# Flask Configuration 
SECRET_KEY=your-actual-secret-key-here

# PostgreSQL Database
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/task_manager

# Email Configuration (Lines 9-11)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

# Scheduler (Line 14)
ENABLE_SCHEDULER=false

# Application URL
APP_URL=http://localhost:5000
```

## What Each Variable Means

### SECRET_KEY
- **What**: Flask secret key for sessions and security
- **How to generate**: Use a random string
- **Example**: `SECRET_KEY=secretkey456`

### DATABASE_URL
- **What**: PostgreSQL database connection string
- **Format**: `postgresql://username:password@host:port/database`
- **Default**: `postgresql://postgres:postgres@localhost:5432/task_manager`
- **Change**: Replace `postgres` with your PostgreSQL username and password

### MAIL_USERNAME
- **What**: Your Gmail email address
- **Example**: `MAIL_USERNAME=yourname@gmail.com`

### MAIL_PASSWORD
- **What**: Gmail App Password (NOT your regular Gmail password!)
- **How to get**:
  1. Go to https://myaccount.google.com/apppasswords
  2. Enable 2-Step Verification first (if not enabled)
  3. Generate App Password for "Mail"
  4. Copy the 16-character password
- **Example**: `MAIL_PASSWORD=abcd efgh ijkl mnop`

### MAIL_DEFAULT_SENDER
- **What**: Email address shown as sender
- **Usually**: Same as MAIL_USERNAME

### ENABLE_SCHEDULER
- **What**: Enable daily email notifications
- **Options**: `false` (disable) or `true` (enable)
- **For local dev**: Use `false`

### APP_URL
- **What**: Your application URL (for email links)
- **Local**: `http://localhost:5000`
- **Production**: Your Render URL like `https://your-app.onrender.com`

## Minimal Setup (Quick Start)

If you just want to run the app locally, minimum required:

```env
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/task_manager
```

Email settings are optional for basic functionality.


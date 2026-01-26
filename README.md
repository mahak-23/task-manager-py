# Task Manager - Flask Application

**Task Manager** is a web app for organizing tasks, built with Flask and PostgreSQL, featuring user registration and login, full CRUD on tasks, deadlines, priorities, and optional daily email reminders.

[https://task-manager-py.onrender.com](https://task-manager-py.onrender.com)

## Features

- ✅ User Registration and Authentication
- ✅ Task Creation, Editing, and Deletion
- ✅ Task Status Management (Pending, In Progress, Completed)
- ✅ Priority Levels (High, Medium, Low)
- ✅ Due Date Tracking
- ✅ Daily Email Notifications (Gmail SMTP)
- ✅ Responsive UI with HTML/CSS/JS
- ✅ PostgreSQL Database



## 🎬 Demo Video

[▶️ Watch Demo Video](https://drive.google.com/file/d/11mSlH56AhG5mmIaj3hIuG257IqrrHfzW/view)

---

## 📸 Screenshots

| Register                                 | Login                                |
| --------------------------------------- | --------------------------------------- |
| ![Register](./Screenshots/register.png) | ![Login](./Screenshots/login.png) |

| Home Page (Dashboard)                            |
| ------------------------------------- |
| ![Dashboard](./Screenshots/dashboard.png) |

| Create Task                          | Edit Task                                                |
| --------------------------------------------- | ----------------------------------------------------------- |
| ![Create](./Screenshots/create.png) | ![Edit](./Screenshots/edit.png) |

| Email Notification                      |
| --------------------------------------- |
| ![Email Notification](./Screenshots/email.png) |

---

## Tech Stack

- **Backend:** Flask 3.0.0
- **Database:** PostgreSQL
- **ORM:** Flask-SQLAlchemy
- **Authentication:** Flask-Login
- **Email:** Flask-Mail (Gmail SMTP)
- **Scheduling:** APScheduler
- **Deployment:** Render.com

## 📡 API Endpoints

### 🔐 Authentication Endpoints
| Method | Endpoint | Description |
|------|---------|------------|
| `GET` | `/auth/register` | Render user registration page |
| `POST` | `/auth/register` | Register a new user |
| `GET` | `/auth/login` | Render login page |
| `POST` | `/auth/login` | Authenticate user credentials |
| `GET` | `/auth/logout` | Logout the current user |

---

### 📝 Task Management Endpoints
| Method | Endpoint | Description |
|------|---------|------------|
| `GET` | `/dashboard` | View all tasks for logged-in user |
| `GET` | `/create` | Render create task page |
| `POST` | `/create` | Create a new task |
| `GET` | `/edit/<task_id>` | Render edit task page |
| `POST` | `/edit/<task_id>` | Update task details |
| `POST` | `/delete/<task_id>` | Delete a task |
| `POST` | `/update_status/<task_id>` | Update task status via AJAX |

> 🔒 All task-related endpoints are protected using **Flask-Login** and are accessible only to authenticated users.

---

### ⏰ Scheduler & Email
| Type | Description |
|----|------------|
| Background Job | APScheduler runs daily at **8:00 AM** |
| Email Trigger | Sends task reminder emails for tasks due today |
| Manual Test | `/test-email` (development/testing only) |

---

## 🗄️ Database Schema

### 👤 User Table
| Column | Type | Description |
|------|----|------------|
| `id` | Integer (PK) | Unique user identifier |
| `username` | String | Unique username |
| `email` | String | Unique email address |
| `password_hash` | String | Hashed password |
| `created_at` | DateTime | Account creation timestamp |

---

### 📋 Task Table
| Column | Type | Description |
|------|----|------------|
| `id` | Integer (PK) | Unique task identifier |
| `title` | String | Task title |
| `description` | Text | Optional task description |
| `priority` | Enum | `high`, `medium`, `low` |
| `status` | Enum | `pending`, `in_progress`, `completed` |
| `due_date` | Date | Task deadline |
| `created_at` | DateTime | Task creation time |
| `updated_at` | DateTime | Last update time |
| `user_id` | Integer (FK) | Associated user |

---

## 🔐 Security & Access Control

- Passwords are securely hashed before storage
- Users can only access **their own tasks**
- Authentication handled using **Flask-Login**
- Database operations use **SQLAlchemy ORM**

---


## Project Structure

```
task-manager/
├── app.py                  # Flask entrypoint
├── config.py               # Configuration
├── models.py               # Database models
│
├── routes/                 # Blueprints
│   ├── __init__.py
│   ├── auth.py             # Register/login/logout routes
│   └── tasks.py            # Task CRUD routes
│
├── services/               # Business logic
│   ├── __init__.py
│   ├── email_service.py    # Email notifications
│   └── scheduler.py        # Daily scheduler
│
├── requirements.txt        # Python dependencies
├── render.yaml             # Render.com deployment config
│
├── templates/              # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── create_task.html
│   └── edit_task.html
│
├── static/                 # CSS/JS
│   ├── style.css
│   └── script.js
│
└── README.md               # You are here!
```

## Local Development: Quick Start

**Requirements:**

- Python 3.12.10+
- Optionally: PostgreSQL (for full functionality)
- Optionally: Gmail account (for notifications, can skip for dev)

### 1. Clone the Project

```bash
git clone https://github.com/yourusername/task-manager.git
cd task-manager
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/task_manager
MAIL_USERNAME=your-email@gmail.com       # Optional for development
MAIL_PASSWORD=your-gmail-app-password    # Optional for development
MAIL_DEFAULT_SENDER=your-email@gmail.com # Optional for development
ENABLE_SCHEDULER=false                   # Set to true for email scheduler
APP_URL=http://localhost:5000
```

> **Tip:** For local PostgreSQL, create your DB first:
>
> ```sql
> CREATE DATABASE task_manager;
> ```

### 5. Start the App

```bash
python app.py
```

App runs at: [http://localhost:5000](http://localhost:5000)

### 6. Initialize Database (if needed)

App creates tables automatically on first run.  
Or, for manual control:

```bash
python
>>> from app import create_app
>>> from models import db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
```

## Gmail SMTP for Email Reminders

To enable daily email notifications:

1. Enable 2-Step Verification on your Google Account
2. Create an [App Password](https://myaccount.google.com/apppasswords) (16 chars)
3. Put this in `.env` as `MAIL_PASSWORD`

> Without SMTP config, the app works but won’t send emails

## Daily Email Reminders

- Scheduler runs at 8:00 AM UTC (if `ENABLE_SCHEDULER=true`)
- Users get an email of their tasks due that day
- Only runs for users with due tasks
- Uses Gmail SMTP

To change send time, open `services/scheduler.py` and adjust:

```python
trigger=CronTrigger(hour=8, minute=0)  # Change hour/minute if you want
```

## Usage Overview

1. **Register**: Create a new account
2. **Login**: Access your dashboard
3. **Create Tasks**: Add tasks with title, description, priority, and due date
4. **Manage Tasks**: Edit, delete, or update task status
5. **View Dashboard**: See all your tasks with filtering options
6. **Email Notifications**: Receive daily emails about tasks due today

Enjoy easy, productive task management. 🚀

# 📚 Library Management System

A complete Flask-based Library Management System that provides separate dashboards for Admins and Users, allowing book management, user management, borrowing and returning functionality, and Excel file uploads. It also supports email reminders for due books.


---

## Table of Contents

1. [Architecture](#architecture)
2. [Features](#features)
3. [Setup & Deployment](#setup--deployment)
4. [File Structure](#file-structure)
5. [Usage](#usage)
6. [Technologies](#technologies)
7. [Notes & Best Practices](#notes--best-practices)

---

## Architecture

The system follows a **modular MVC architecture**:

- **Models**: SQLAlchemy models for `User`, `Book`, `Issue`, `Borrow`, and `Review`.
- **Views / Routes**:
  - `auth`: Registration, login, logout
  - `admin`: Admin dashboard, book/user management, data export/import
  - `user`: User dashboard, book borrowing, review submission
  - `upload`: Excel upload functionality
  - `export`: Excel export functionality
- **Controllers / Utilities**:
  - `email_utils.py`: Scheduled email reminders
  - `file_utils.py`: Excel processing
- **Templates**: Jinja2 templates for rendering HTML
- **Static**: CSS, images, JS assets


### FILE STRUCTURE
library_mgmt/
│
├── app/
│   ├── auth/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── book.py
│   │   ├── issue.py
│   │   └── review.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── user.py
│   │   ├── main.py
│   │   ├── upload.py
│   │   └── export.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── file_utils.py
│   │   ├── email_utils.py
│   │   └── schedule_utils.py
│   ├── templates/
│   └── static/
│       └── css/style.css
├── migrations/
├── uploads/
├── .env
├── config.py
├── main.py
└── requirements.txt

### Diagram

![Architecture Diagram](docs/architecture.png)  

---

## Features

### Admin

- Add, update, and delete books
- Add and manage users
- Export books, users, and issues to Excel
- Upload Excel files for bulk updates

### User

- View available books
- Borrow books (with due dates)
- Return books
- Submit reviews for books
- View borrowing history

### Automated

- Email reminders for due books (configurable interval)
- Password hashing and secure login using Flask-Login

---

## Setup & Deployment

### Prerequisites

- Python 3.10+
- pip
- SQLite (default DB)
- Gmail account for email notifications (or configure SMTP)

### Steps

1. **Clone the repository**

```bash
git clone <repo_url>
cd library_mgmt

2. ** create virtual environment**
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3. **Install Dependencies**
pip install -r requirements.txt

4. ** Set Up Environment Variables**

Create a .env file in the root directory and add:

SECRET_KEY=your_secret_key
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_gmail_app_password

⚠️ Note: You must use an App Password for Gmail (not your regular password).
Create one from: Google App Passwords



🧩 Configuration (config.py)

Key configurations are defined in config.py:

SQLALCHEMY_DATABASE_URI = 'sqlite:///library.db'
UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
ALLOWED_EXTENSIONS = {'xlsx'}
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True

🗄️ Database Models
Model	Description
User	Stores user details (name, email, password, role).
Book	Contains book information (title, author, category, quantity).
Issue	Tracks issued books.
Review	Stores user reviews and ratings for books.
Borrow	Handles book borrowing and return records.

5. ** Run the Application**

Initialize the database
flask db init
flask db migrate
flask db upgrade

Start the server
python main.py

Now open your browser and go to:
👉 http://127.0.0.1:5000




🧰 Tech Stack

Backend: Flask (Python)

Database: SQLite (via SQLAlchemy)

Frontend: HTML, CSS (Bootstrap)

Authentication: Flask-Login

Email: Flask-Mail

Excel Handling: Pandas, OpenPyXL



Notes & Best Practices

Email reminders use Gmail SMTP. Make sure Less secure app access is enabled or use App Password.

Password storage is hashed securely using Werkzeug.

Future enhancements:

Add search & filter for books

Pagination for large datasets

Role-based access for finer permissions

Unit tests with pytest

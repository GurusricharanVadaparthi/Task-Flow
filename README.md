# 🚀 TaskFlow – Full-Stack Task Management Web Application

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python\&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2-092E20?logo=django\&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-F7DF1E?logo=javascript\&logoColor=black)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite\&logoColor=white)
![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?logo=render\&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**TaskFlow** is a full-stack task management web application built with **Django**. It provides users with a centralized platform to create, organize, track, and analyze their tasks with features such as priorities, due dates, analytics, calendar views, notifications, data export, and customizable user settings.

## 🌐 Live Demo

TaskFlow is deployed and available online using **Render**.

👉 **Live Application:**
https://task-flow-zuxu.onrender.com/

You can access the application directly from your browser and explore the complete task management workflow.

---

## 🌟 Features

### 🔐 Authentication & Security

* User registration and login system
* Secure password hashing using PBKDF2-SHA256
* Password reset functionality through email
* Session-based authentication
* User-specific data isolation
* Protected authenticated routes

### ✅ Task Management

* Create, Read, Update, and Delete (CRUD) operations
* Task priorities:

  * 🟢 Low
  * 🟡 Medium
  * 🔴 High
* Due-date scheduling
* Automatic overdue task detection
* Task descriptions
* Mark tasks as completed or incomplete
* Delete confirmation modal
* User-specific task management

### 🔍 Search, Filtering & Sorting

* Search tasks by name
* Filter tasks by:

  * All
  * Pending
  * Completed
  * Overdue
* Filter tasks by priority:

  * Low
  * Medium
  * High
* Sort tasks by:

  * Newest
  * Oldest
  * Due Date
  * Priority
  * Name

### 📊 Analytics Dashboard

* Interactive charts powered by **Chart.js**
* 7-day task activity trends
* Line chart for task activity
* Doughnut chart for priority distribution
* Overall task completion percentage
* Statistics cards for:

  * Total Tasks
  * Completed Tasks
  * Pending Tasks
  * Overdue Tasks

### 📅 Calendar View

* Monthly calendar interface
* Tasks displayed on their respective due dates
* Month and year navigation
* "Today" button for quick navigation
* Color-coded tasks based on priority
* Responsive calendar layout

### 🕒 Activity Timeline

* Activity logging for task-related actions
* Tracks activities such as:

  * Task creation
  * Task editing
  * Task completion
  * Task deletion
* Color-coded activity timeline
* Displays the latest 100 activities

### 🔔 Notifications

* Notifications for overdue tasks
* Notifications for tasks due today
* Native OS notifications
* In-app notification page
* Categorized notifications
* Notification deduplication to prevent repeated alerts
* User-controlled notification preferences

### 📤 Data Export

#### CSV Export

* Export tasks into CSV format
* Spreadsheet-compatible output
* Includes task information such as title, priority, status, and due date

#### PDF Export

* Generate formatted PDF task reports
* PDF generation powered by **ReportLab**
* Structured tables with headers
* Styled and readable report format

### 🎨 UI/UX

* Modern and responsive user interface
* Light Mode
* Dark Mode
* System theme option
* Mobile-friendly responsive design
* Hamburger navigation menu
* Loading animations
* Button spinners
* Fade-in animations
* Slide-up modal animations
* Smooth transitions
* Hover effects
* Delete confirmation dialogs

### 👤 User Profile & Settings

* Editable user profile
* Profile name
* Email
* Bio
* Profile statistics
* Total task count
* Completed task count
* Account join date
* Custom default task priority
* Custom default sorting preference
* Theme preferences
* Notification preferences

---

## 🖼️ Screenshots

### 🔐 Login Page

![Login Page](screenshots/login.png)

### 📋 Dashboard

![Dashboard](screenshots/dashboard.png)

### 📅 Calendar View

![Calendar View](screenshots/calendar.png)

### 📊 Analytics Dashboard

![Analytics Charts](screenshots/analytics1.png)

![Analytics Charts](screenshots/analytics2.png)

---

## 🛠️ Tech Stack

| Category                 | Technology                    |
| ------------------------ | ----------------------------- |
| **Backend**              | Django 4.2                    |
| **Programming Language** | Python 3.13                   |
| **Frontend**             | HTML5, CSS3, JavaScript (ES6) |
| **Database**             | SQLite 3                      |
| **Charts**               | Chart.js                      |
| **PDF Generation**       | ReportLab                     |
| **Authentication**       | Django Authentication System  |
| **Styling**              | CSS3                          |
| **Fonts**                | Google Fonts – Inter          |
| **Deployment**           | Render                        |
| **Version Control**      | Git & GitHub                  |

---

## 🏗️ Application Architecture

```text
User
 │
 ▼
Frontend
HTML + CSS + JavaScript
 │
 ▼
Django Views
 │
 ├── Authentication
 ├── Task Management
 ├── Search & Filtering
 ├── Analytics
 ├── Calendar
 ├── Notifications
 ├── Activity Tracking
 └── Data Export
 │
 ▼
Django Models
 │
 ▼
SQLite Database
```

---

## 📂 Project Structure

```text
Task-Flow/
│
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── taskflow/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── tasks/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── screenshots/
│   ├── login.png
│   ├── dashboard.png
│   ├── calendar.png
│   ├── analytics1.png
│   └── analytics2.png
│
└── db.sqlite3
```

> The exact structure may vary depending on the latest version of the project.

---

## 📦 Installation

### Prerequisites

Make sure the following are installed:

* Python 3.10 or higher
* pip
* Git

### 1. Clone the Repository

```bash
git clone https://github.com/GurusricharanVadaparthi/Task-Flow.git
cd Task-Flow
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations

```bash
python manage.py migrate
```

### 5. Create a Superuser

```bash
python manage.py createsuperuser
```

Follow the instructions in the terminal to create the administrator account.

### 6. Start the Development Server

```bash
python manage.py runserver
```

Open the application at:

```text
http://127.0.0.1:8000/
```

---

## 🔑 Authentication Flow

TaskFlow provides a complete authentication workflow:

```text
Registration
     ↓
Login
     ↓
Authenticated Dashboard
     ↓
Task Management
     ↓
Profile & Settings
```

Users can securely register, log in, manage their tasks, update their profile, and reset their password through the email-based password reset workflow.

---

## 📊 Task Workflow

```text
Create Task
     ↓
Set Priority
     ↓
Set Due Date
     ↓
Manage Task
     ↓
Pending / Completed
     ↓
Analytics & Activity Tracking
     ↓
Export Data
```

Overdue tasks are automatically identified based on their due dates.

---

## 🌐 Deployment

TaskFlow is deployed using **Render**.

### Production Application

**Live URL:**

https://task-flow-zuxu.onrender.com/

The deployed version provides access to the application's main functionality through a publicly accessible web interface.

### Deployment Stack

```text
GitHub Repository
       ↓
     Render
       ↓
Django Application
       ↓
Production Web Server
```

---

## 🔧 Environment Variables

For production deployment, sensitive configuration values should be stored as environment variables rather than directly inside the source code.

Example:

```text
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-email-password
```

> Do not commit secret keys, email passwords, API keys, or other sensitive credentials to GitHub.

---

## 📈 Future Improvements

Potential future enhancements include:

* REST API using Django REST Framework
* PostgreSQL database for production
* Advanced task recurrence
* Drag-and-drop task management
* Real-time notifications using WebSockets
* Team collaboration
* Task sharing
* Role-based access control
* Google OAuth authentication
* Improved analytics and reporting
* Automated testing with PyTest
* CI/CD pipeline using GitHub Actions

---

## 🎯 Learning Outcomes

This project helped strengthen practical understanding of:

* Django web development
* Python programming
* CRUD application development
* User authentication
* Database modeling
* Django ORM
* Frontend development
* JavaScript interactions
* Data visualization
* PDF generation
* CSV data processing
* Email-based workflows
* Responsive UI development
* Git and GitHub
* Web application deployment
* Production configuration

---

## 👨‍💻 Author

**Guru Sri Charan Vadaparthi**

Computer Science & Engineering
Indian Institute of Technology Bhubaneswar

---

## 📄 License

This project is licensed under the **MIT License**.

You are free to use, modify, and distribute this project according to the terms of the license.

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

**GitHub Repository:**
https://github.com/GurusricharanVadaparthi/Task-Flow

**Live Demo:**
https://task-flow-zuxu.onrender.com/

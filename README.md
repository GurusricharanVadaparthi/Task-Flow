# 🚀 TaskFlow – Full-Stack Task Management Web Application

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2-092E20?logo=django&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-F7DF1E?logo=javascript&logoColor=black)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**TaskFlow** is a modern, feature-rich task management web application built with Django. It helps users organize their daily tasks with priorities, due dates, analytics, and a beautiful responsive interface — all in one place.

---

## 🌟 Features

### 🔐 Authentication & Security
- User registration and login system
- Secure password hashing (PBKDF2-SHA256)
- Password reset flow via email
- Session-based authentication
- User-specific data isolation

### ✅ Task Management
- Create, Read, Update, Delete (CRUD) operations
- Task priorities (Low, Medium, High) with color coding
- Due date scheduling with overdue detection
- Rich task descriptions
- Mark tasks as complete/incomplete
- Delete confirmation modal

### 🔍 Search & Filtering
- Real-time task search by name
- Filter by status (All, Pending, Completed, Overdue)
- Filter by priority (Low, Medium, High)
- Customizable sort order (Newest, Oldest, Due Date, Priority, Name)

### 📊 Analytics Dashboard
- Interactive charts powered by Chart.js
- 7-day activity trends (line chart)
- Priority distribution (doughnut chart)
- Overall progress bar with percentage
- Statistics cards (Total, Completed, Pending, Overdue)

### 📅 Calendar View
- Monthly calendar with tasks displayed on due dates
- Quick navigation with month/year dropdowns
- "Today" button for instant jump to current date
- Color-coded tasks by priority
- Fully responsive on mobile

### 🕒 Activity Timeline
- Real-time activity logging
- Tracks all actions: create, edit, complete, delete
- Beautiful timeline UI with color-coded events
- Last 100 activities displayed

### 🔔 Notifications
- Browser push notifications for overdue/due-today tasks
- Native OS toast notifications (Windows Action Center / macOS)
- In-app notification page with categorized alerts
- Smart deduplication (won't spam same notification)

### 📤 Data Export
- **CSV Export** – Download all tasks in spreadsheet format
- **PDF Export** – Generate professional PDF reports using ReportLab
- Styled tables with headers, colors, and formatting

### 🎨 UI/UX Highlights
- **Dark Mode** – Light, Dark, and System theme options
- **Responsive Design** – Mobile-first approach with hamburger menu
- **Loading Animations** – Button spinners, fade-in cards, slide-up modals
- **Modal Confirmations** – Beautiful delete confirmation dialogs
- Smooth transitions and hover effects

### 👤 User Profile & Settings
- Editable user profile (name, bio, email)
- Profile stats (total tasks, completed, join date)
- Customizable defaults (priority, sort order)
- Theme preferences saved per user
- Notification preferences

---

## 🖼️ Screenshots

### Login Page
![Login Page](screenshots/login.png)

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Calendar View
![Calendar View](screenshots/calendar.png)

### Analytics
![Analytics Charts](screenshots/analytics1.png)
![Analytics Charts](screenshots/analytics2.png)

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| **Backend** | Django 4.2, Python 3.13 |
| **Frontend** | HTML5, CSS3, JavaScript (ES6) |
| **Database** | SQLite 3 |
| **Charts** | Chart.js |
| **PDF Generation** | ReportLab |
| **Authentication** | Django Auth (session-based) |
| **Icons/Fonts** | Google Fonts (Inter) |

---

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/GurusricharanVadaparthi/taskflow.git
   cd taskflow
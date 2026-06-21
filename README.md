# 🎓 Faculty Attendance Notification System (FANS)

A smart, face-recognition-based attendance management system for faculty members, with automated email notifications and report scheduling.

---

## 📌 Features

- 🔍 **Face Recognition** – Automatically marks attendance using OpenCV's LBPH Face Recognizer
- 📧 **Email Notifications** – Sends instant email alerts to faculty when attendance is marked
- 📊 **Admin Dashboard** – Web-based admin panel to view attendance, manage faculty, and generate reports
- 📅 **Automated Reports** – Daily, Weekly, and Monthly attendance reports sent via email
- ⏰ **Scheduler** – Background scheduler automates report sending at configured times
- 🔐 **Role-Based Login** – Separate dashboards for Admin and Faculty roles

---

## 🗂️ Project Structure

```
FANS/
├── app.py                  # Flask backend (main server)
├── attendance.py           # Face recognition attendance module
├── capture_images.py       # Captures face images for training
├── train_model.py          # Trains the LBPH face recognition model
├── report_scheduler.py     # Email report logic (daily/weekly/monthly)
├── auto_scheduler.py       # Background cron-style scheduler
├── faculty_details.csv     # Faculty data (name, email, password, role)
├── attendance.csv          # Attendance records (auto-generated)
├── labels.pkl              # Label mappings for face model
├── templates/
│   ├── index.html          # Login page
│   ├── admin.html          # Admin dashboard
│   └── faculty.html        # Faculty dashboard
└── dataset/                # Face image dataset (not tracked in git)
```

---

## 🚀 Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/SanjanaAlavandi/Faculty_AttendanceNotificationSystem.git
cd Faculty_AttendanceNotificationSystem
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
```

### 3. Install dependencies
```bash
pip install flask opencv-contrib-python schedule
```

### 4. Configure Email Credentials

In `app.py`, `attendance.py`, and `report_scheduler.py`, update:
```python
SENDER_EMAIL = "your_email@gmail.com"
PASSWORD = "your_app_password"
ADMIN_EMAIL = "admin_email@gmail.com"
```

> ⚠️ Use a **Gmail App Password** (not your main password).  
> Enable 2FA → Google Account → App Passwords → Generate one.

---

## 🧠 Training the Model

1. **Capture face images** for each faculty member:
```bash
python capture_images.py
```

2. **Train the model**:
```bash
python train_model.py
```
This generates `trainer.yml` and `labels.pkl`.

---

## ▶️ Running the System

### Start the Flask Web Server
```bash
python app.py
```
Visit: `http://127.0.0.1:5000`

### Start the Attendance (Face Recognition)
Use the **Admin Dashboard → Start Attendance** button, or run directly:
```bash
python attendance.py
```

### Start the Automated Report Scheduler
```bash
python auto_scheduler.py
```

---

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Login page |
| POST | `/login` | Authenticate user |
| GET | `/admin-dashboard` | Admin panel |
| GET | `/faculty-dashboard` | Faculty panel |
| POST | `/add-user` | Add new faculty |
| GET | `/get-faculty` | List all faculty |
| GET | `/attendance-by-date?date=YYYY-MM-DD` | Attendance for a date |
| POST | `/start-attendance` | Launch face recognition |
| POST | `/daily-report` | Send daily report email |
| POST | `/weekly-report` | Send weekly report email |
| POST | `/monthly-report` | Send monthly report email |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| Face Recognition | OpenCV (LBPH) |
| Email | smtplib, Gmail SMTP |
| Frontend | HTML, CSS, JavaScript |
| Scheduler | `schedule` library |
| Data Storage | CSV files |

---

## 👥 Team

**Team No. 34**

---

## 📄 License

This project is for academic/educational purposes.

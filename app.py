from flask import Flask, render_template, request, jsonify
import subprocess
import csv
app = Flask(__name__)
import datetime
import os
from report_scheduler import send_daily_report, send_monthly_report, send_weekly_report
import csv
from datetime import datetime, timedelta
from email.mime.text import MIMEText
import smtplib

app = Flask(__name__)

ADMIN_EMAIL = "admingit1@gmail.com"
SENDER_EMAIL = "admingit1@gmail.com"
PASSWORD = "pgoe zwuh nsyt gvbf"
# Dummy users (you can replace later with DB)


def check_user(email, password):
    with open("faculty_details.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Email"] == email and row["Password"] == password:
                return row["Role"], row["Name"]
    return None, None
@app.route('/')
def home():
    return render_template("index.html")   # your HTML file

@app.route('/admin-dashboard')
def dashboard():
    return render_template("admin.html")

@app.route('/faculty-dashboard')
def faculty_dashboard():
    return render_template("faculty.html")

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    role, name = check_user(email, password)
    if role:
        return jsonify({"status": "success", "role": role, "name": name})  
    else:
        return jsonify({"status": "fail"})  
    
@app.route('/add-user', methods=['POST'])
def add_user():
    data = request.json

    name = data["name"]
    email = data["email"]
    password = data["password"]
    role = data["role"]

    with open("faculty_details.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, email, password, role])

    return jsonify({"status": "added"})


@app.route('/capture-images', methods=['POST'])
def capture_images():
    name = request.json["name"]
    subprocess.Popen(["python", "capture_images.py", name])
    return jsonify({"status": "capturing"})

@app.route('/get-faculty')
def get_faculty():
   
    faculty = []

    with open("faculty_details.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            faculty.append({
                "name": row["Name"],
                "email": row["Email"],
                "role": row["Role"]
            })

    return jsonify(faculty)

@app.route('/attendance-by-date')
def attendance_by_date():
    date = request.args.get('date')

    faculty_list = []
    attendance_map = {}

    # Read faculty list
    with open('faculty_details.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            faculty_list.append(row["Name"])

    # Read attendance
    if os.path.exists('attendance.csv'):
        with open('attendance.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 3:
                    name, d, time = row
                    if d == date:
                        attendance_map[name] = "Present"

    # Final result
    result = []
    for name in faculty_list:
        status = "Present" if name in attendance_map else "Absent"
        result.append({"name": name, "status": status})

    return jsonify(result)

# 🔥 START ATTENDANCE SYSTEM
@app.route('/start-attendance', methods=['POST'])
def start_attendance():
    subprocess.Popen(["python", "attendance.py"])
    return jsonify({"status": "started"})


def send_admin_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = ADMIN_EMAIL

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, PASSWORD)
            server.send_message(msg)
        print("Report email sent!")
    except Exception as e:
        print("Error sending email:", e)

@app.route('/daily-report', methods=['POST'])
def daily_report():
    today = datetime.now().strftime("%Y-%m-%d")

    present = set()

    with open("attendance.csv", "r") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if row[1] == today:
                present.add(row[0])

    all_faculty = []
    with open("faculty_details.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            all_faculty.append(row["Name"])

    absent = [f for f in all_faculty if f not in present]

    message = f"""
📅 DAILY ATTENDANCE REPORT

Date: {today}

✅ Present:
{', '.join(present) if present else 'None'}

❌ Absent:
{', '.join(absent) if absent else 'None'}
"""

    send_admin_email("Daily Report", message)

    return jsonify({"message": "Daily report sent!"})


@app.route('/weekly-report', methods=['POST'])
def weekly_report():
    last_7_days = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

    count = {}

    with open("attendance.csv", "r") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            name, date = row[0], row[1]
            if date in last_7_days:
                count[name] = count.get(name, 0) + 1

    message = "📅 WEEKLY REPORT\n\n"
    for name, days in count.items():
        message += f"{name}: {days} days present\n"

    send_admin_email("Weekly Report", message)

    return jsonify({"message": "Weekly report sent!"})


@app.route('/monthly-report', methods=['POST'])
def monthly_report():
    last_30_days = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]

    count = {}

    with open("attendance.csv", "r") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            name, date = row[0], row[1]
            if date in last_30_days:
                count[name] = count.get(name, 0) + 1

    message = "📊 MONTHLY REPORT (Last 30 Days)\n\n"

    with open("faculty_details.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["Name"]
            days = count.get(name, 0)
            message += f"{name}: {days} days present\n"

    send_admin_email("Monthly Report", message)

    return jsonify({"message": "Monthly report sent!"})


if __name__ == "__main__":
    app.run(debug=True)
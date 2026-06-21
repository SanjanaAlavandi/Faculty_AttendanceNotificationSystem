import csv
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta

ADMIN_EMAIL = "admingit1@gmail.com"
SENDER_EMAIL = "admingit1@gmail.com"
SENDER_PASSWORD = "pgoe zwuh nsyt gvbf"


# 📌 Get all faculty names
def get_all_faculty():
    names = []
    with open("faculty_details.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            names.append(row["Name"].strip())
    return names


# 📌 Get present faculty for a specific date
def get_present_faculty(date):
    present = set()

    try:
        with open("attendance.csv", "r") as f:
            reader = csv.reader(f)
            next(reader, None)

            for row in reader:
                if len(row) >= 2 and row[1] == date:
                    present.add(row[0].strip())
    except:
        pass

    return present


# 📧 Send Email
def send_email(subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = ADMIN_EMAIL

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print("Report sent!")
    except Exception as e:
        print("Email error:", e)


# 📅 DAILY REPORT
def send_daily_report():
    today = datetime.now().strftime("%Y-%m-%d")

    all_faculty = set(get_all_faculty())
    present = get_present_faculty(today)
    absent = all_faculty - present

    message = f"""
📊 DAILY ATTENDANCE REPORT ({today})

✅ Present ({len(present)}):
{', '.join(present) if present else 'None'}

❌ Absent ({len(absent)}):
{', '.join(absent) if absent else 'None'}
"""

    send_email("Daily Attendance Report", message)


# 📆 MONTHLY REPORT


def send_monthly_report():
    today = datetime.now()
    last_30_days = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]

    all_faculty = get_all_faculty()

    # Initialize count
    present_count = {name: 0 for name in all_faculty}

    try:
        with open("attendance.csv", "r") as f:
            reader = csv.reader(f)
            next(reader, None)

            for row in reader:
                if len(row) >= 2:
                    name = row[0].strip()
                    date = row[1].strip()

                    if date in last_30_days:
                        present_count[name] += 1

    except Exception as e:
        print("Error reading attendance:", e)

    # Create report
    report = "📆 MONTHLY ATTENDANCE REPORT (Last 30 Days)\n\n"

    for name in all_faculty:
        report += f"{name} → {present_count[name]} days present\n"

    send_email("Monthly Attendance Report", report)


def send_weekly_report():
    today = datetime.now()
    last_7_days = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

    all_faculty = get_all_faculty()
    present_count = {name: 0 for name in all_faculty}

    try:
        with open("attendance.csv", "r") as f:
            reader = csv.reader(f)
            next(reader, None)

            for row in reader:
                if len(row) >= 2:
                    name = row[0].strip()
                    date = row[1].strip()

                    if date in last_7_days:
                        present_count[name] += 1
    except:
        pass

    report = "📆 WEEKLY ATTENDANCE REPORT (Last 7 Days)\n\n"

    for name in all_faculty:
        report += f"{name} → {present_count[name]} days present\n"

    send_email("Weekly Attendance Report", report)

    
if __name__ == "__main__":
    send_daily_report()
    send_monthly_report()       
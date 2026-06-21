import schedule
import time
from datetime import datetime
from report_scheduler import send_daily_report, send_monthly_report

print("Scheduler started...")

# ✅ DAILY REPORT (set time you want)
schedule.every().day.at("00:57").do(send_daily_report)

# ✅ MONTHLY REPORT (last 30 days logic)
def monthly_wrapper():
    today = datetime.now()
    
    # You can keep ANY condition here (for demo just run once)
    if today.day == 18:   # or change to today.day == datetime.now().day for testing
        send_monthly_report()

schedule.every().day.at("23:59").do(monthly_wrapper)

# 🔁 RUN LOOP
while True:
    schedule.run_pending()
    time.sleep(30)
import cv2
import pickle
import csv
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
close_clicked=False

def mouse_callback(event, x, y, flags, param):
    global close_clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        if 500 < x < 620 and 10 < y < 50:
            close_clicked = True

def send_email(name, date, time):
    sender = "admingit1@gmail.com"
    password = "pgoe zwuh nsyt gvbf"
    
    def get_email(name):
        with open("faculty_details.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Name"] == name:
                    return row["Email"]
        return None
    receiver = get_email(name)
    message = f"{name} marked attendance on {date} at {time}"

    msg = MIMEText(message)
    msg['Subject'] = "Attendance Alert"
    msg['From'] = sender
    msg['To'] = receiver

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        print("Email sent!")
    except Exception as e:
        print("Error:", e)


# Load trained model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

# Load labels
with open("labels.pkl", "rb") as f:
    labels = pickle.load(f)

# Face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Attendance file
file_name = "attendance.csv"

# Create file if not exists
if not os.path.exists(file_name):
    with open(file_name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Date","Time"])

# Track already marked names
marked = set()
# Track already marked names (LOAD FROM CSV)
marked = set()

if os.path.exists(file_name):
    with open(file_name, "r") as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header

        for row in reader:
            if len(row) >= 2:
                name = row[0].strip()
                date = row[1].strip()
                marked.add((name, date))
# Start webcam
cap = cv2.VideoCapture(0)

print("Starting attendance system... Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]

        id_, confidence = recognizer.predict(face)

        if confidence < 70:   # lower = better match
            name = labels[id_].strip()
            date_now=datetime.now().strftime("%Y-%m-%d")
            time_now = datetime.now().strftime("%H:%M:%S")

            if (name, date_now) not in marked:
                marked.add((name, date_now))

                with open(file_name, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([name, date_now, time_now])

                status_text = f"{name} marked present"
                send_email(name, date_now, time_now)
                
            else:
                status_text=f"{name} already marked today!" 

            label = f"{name} ({int(confidence)})"
        else:
            label = "Unknown"

        # Draw rectangle + name
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(frame, status_text, (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX, 1,
            (0, 255, 0), 2)

    cv2.imshow("Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
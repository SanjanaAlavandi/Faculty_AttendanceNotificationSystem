import cv2
import os
import sys
import time 

# Ask user name
name = sys.argv[1]

# Create folder
dataset_path = f"dataset/{name}"
person_path = os.path.join(dataset_path, name)

if not os.path.exists(person_path):
    os.makedirs(person_path)

# Load face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Start webcam
cap = cv2.VideoCapture(0)

count = 0
max_images = 100
last_capture_time = time.time()
while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        current_time = time.time()

        # ⏳ Capture every 0.5 seconds
        if current_time - last_capture_time > 0.5:
            count += 1

            face = gray[y:y+h, x:x+w]
            file_path = os.path.join(person_path, f"{count}.jpg")
            cv2.imwrite(file_path, face)

            last_capture_time = current_time
    cv2.imshow("Capturing Faces", frame)

    # Stop after 80 images or press 'q'
    if count >= max_images:
        print("Finished capturing images.")
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print("Dataset created successfully!")
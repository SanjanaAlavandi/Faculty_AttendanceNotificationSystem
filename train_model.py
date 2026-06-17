import cv2
import os
import numpy as np
from PIL import Image
import pickle

dataset_path = "dataset"

# Initialize recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

face_samples = []
ids = []
label_map = {}
current_id = 0

for root, dirs, files in os.walk(dataset_path):
    for dir_name in dirs:
        label_map[current_id] = dir_name
        person_path = os.path.join(root, dir_name)

        for file in os.listdir(person_path):
            if file.endswith("jpg"):
                img_path = os.path.join(person_path, file)
                img = Image.open(img_path).convert('L')
                img_np = np.array(img, 'uint8')

                face_samples.append(img_np)
                ids.append(current_id)

        current_id += 1

# Train model
recognizer.train(face_samples, np.array(ids))

# Save model
recognizer.save("trainer.yml")

# Save label mapping
with open("labels.pkl", "wb") as f:
    pickle.dump(label_map, f)

print("Model trained successfully!")
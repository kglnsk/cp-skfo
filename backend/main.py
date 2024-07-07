from fastapi import FastAPI, HTTPException
from minio import Minio
from minio.error import S3Error
from typing import List
import os
from fastapi.middleware.cors import CORSMiddleware

import os
from datetime import timedelta
from typing import List
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ultralytics import YOLO
from PIL import Image
from collections import Counter
import pandas as pd
import shutil
import tempfile
from PIL.ExifTags import TAGS

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace '*' with the actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Minio client
minio_client = Minio(
    "minio",  # Minio service endpoint
    access_key="YIbky86nWbY9dk6ZwpQm",  # Access key as defined in the docker-compose file
    secret_key="cXkGzbiW1tlGLRW8mbdu9yp7y7Lhmd4johYJSs5g",  # Secret key as defined in the docker-compose file
    secure=False  # Set to True if using HTTPS
)




# Load the YOLO model
model = YOLO('last.pt')

class RegistrationData(BaseModel):
    folder_name: str
    class_name: str
    date_registration_start: str
    date_registration_end: str
    count: int

@app.post("/upload/", response_model=List[RegistrationData])
async def upload_files(folder_name: str = Form(...), files: List[UploadFile] = File(...)):
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save uploaded files to temporary directory
        for file in files:
            file_path = os.path.join(temp_dir, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

        # Process images
        image_names = []
        majority_classes = []
        object_counts = []
        date_times = []

        for filename in os.listdir(temp_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(temp_dir, filename)
                
                # Extract EXIF datetime
                image = Image.open(file_path)
                exif_data = image._getexif()
                if exif_data:
                    for tag_id, value in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        if tag == "DateTimeOriginal":
                            date_times.append(value)
                            break
                else:
                    date_times.append(None)

                # Process image with YOLO
                results = model(image)
                
                class_names = results[0].names
                detected_classes = results[0].boxes.cls.cpu().numpy()

                object_count = len(detected_classes)
                if object_count > 0:
                    majority_class = class_names[Counter(detected_classes).most_common(1)[0][0]]
                else:
                    majority_class = 'No detections'

                image_names.append(filename)
                majority_classes.append(majority_class)
                object_counts.append(object_count)

        # Create DataFrame
        df = pd.DataFrame({
            'Image Name': image_names,
            'Majority Class': majority_classes,
            'Object Count': object_counts,
            'date_time': date_times,
            'Name Folder': folder_name
        })

        # Convert date_time to datetime and sort
        df['date_time'] = pd.to_datetime(df['date_time'], format='%Y:%m:%d %H:%M:%S')
        df = df.sort_values('date_time')

        # Process registrations
        registrations = []
        current_registration = None

        for _, row in df.iterrows():
            if current_registration is None:
                current_registration = {
                    'folder_name': row['Name Folder'],
                    'class': row['Majority Class'],
                    'date_registration_start': row['date_time'],
                    'date_registration_end': row['date_time'],
                    'count': row['Object Count']
                }
            elif (row['date_time'] - current_registration['date_registration_end'] <= timedelta(minutes=30) and
                  row['Majority Class'] == current_registration['class']):
                current_registration['date_registration_end'] = row['date_time']
                current_registration['count'] = max(current_registration['count'], row['Object Count'])
            else:
                registrations.append(current_registration)
                current_registration = {
                    'folder_name': row['Name Folder'],
                    'class': row['Majority Class'],
                    'date_registration_start': row['date_time'],
                    'date_registration_end': row['date_time'],
                    'count': row['Object Count']
                }

        if current_registration is not None:
            registrations.append(current_registration)

        # Format output
        result = []
        for reg in registrations:
            result.append({
                "folder_name": reg['folder_name'],
                "class": reg['class'],
                "date_registration_start": reg['date_registration_start'].strftime("%Y-%m-%dT%H:%M:%SZ"),
                "date_registration_end": reg['date_registration_end'].strftime("%Y-%m-%dT%H:%M:%SZ"),
                "count": reg['count']
            })

        return JSONResponse(content=result)




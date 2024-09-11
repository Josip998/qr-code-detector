import os
from datetime import datetime
from typing import List
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
import numpy as np
import io
import cv2
import requests
import firebase_admin
from firebase_admin import credentials, auth, firestore
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

# Initialize OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust this URL to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize Firebase Admin
cred = credentials.Certificate(r"C:\Users\Josip\Desktop\qr-code-detector-bd93c-firebase-adminsdk-tgnic-d0302df0db.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

class QRCodeResponse(BaseModel):
    qr_codes: list

@app.post("/detect-qr/", response_model=QRCodeResponse)
async def detect_qr(file: UploadFile = File(...), token: str = Depends(oauth2_scheme)):
    try:
        # Verify token
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Read the uploaded image
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

    # Convert to OpenCV format
    open_cv_image = np.array(image)
    open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

    # Create a QRCode detector
    detector = cv2.QRCodeDetector()

    # Detect and decode QR codes
    decoded_text, points, _ = detector.detectAndDecode(open_cv_image)

    detected_qr_codes = []

    if points is not None:
        # Ensure points is a NumPy array
        if isinstance(points, np.ndarray):
            if points.ndim == 3:
                for i in range(points.shape[0]):
                    point = points[i]
                    
                    # Convert points to integer
                    point = np.int32(point).reshape(-1, 2)

                    # Draw the bounding box around the QR code
                    cv2.polylines(open_cv_image, [point], isClosed=True, color=(0, 0, 255), thickness=2)

                    # Extract the QR code image
                    x_min = int(min(point[:, 0]))
                    y_min = int(min(point[:, 1]))
                    x_max = int(max(point[:, 0]))
                    y_max = int(max(point[:, 1]))
                    
                    qr_code_image = open_cv_image[y_min:y_max, x_min:x_max]
                    
                    # Save the QR code image
                    qr_code_pil_image = Image.fromarray(cv2.cvtColor(qr_code_image, cv2.COLOR_BGR2RGB))
                    qr_code_filename = f"processed_images/qr_code_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.jpg"
                    qr_code_pil_image.save(qr_code_filename)

                    # Resolve the short URL if necessary
                    short_url = decoded_text if decoded_text else None
                    full_url = short_url
                    if short_url:
                        try:
                            response = requests.head(short_url, allow_redirects=True)
                            if response.url != short_url:
                                full_url = response.url
                        except requests.RequestException as e:
                            print(f"Error resolving URL: {e}")

                    detected_qr_codes.append({
                        "data": full_url,
                        "rect": {
                            "x": x_min,
                            "y": y_min,
                            "width": x_max - x_min,
                            "height": y_max - y_min
                        },
                        "image_path": qr_code_filename
                    })

                    # Save the QR code data to Firestore
                    doc_ref = db.collection("users").document(uid).collection("scans").document()
                    doc_ref.set({
                        "data": full_url,
                        "rect": {
                            "x": x_min,
                            "y": y_min,
                            "width": x_max - x_min,
                            "height": y_max - y_min
                        },
                        "image_path": qr_code_filename,
                        "timestamp": datetime.now().isoformat()
                    })
            else:
                print("Unexpected points shape:", points.shape)
        else:
            print("Unexpected type for points:", type(points))
    else:
        print("No QR codes detected.")

    # Save the processed image with detected QR code bounding boxes
    img_with_boxes = Image.fromarray(cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    img_filename = f"processed_images/qr_processed_{timestamp}.jpg"
    img_with_boxes.save(img_filename)

    # Return the detected QR codes and their data
    return QRCodeResponse(qr_codes=detected_qr_codes)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        return {"uid": uid}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/user-scans/", response_model=List[QRCodeResponse])
async def get_user_scans(token: str = Depends(get_current_user)):
    uid = token['uid']
    try:
        user_scans_ref = db.collection("users").document(uid).collection("scans")
        user_scans = user_scans_ref.stream()
        scans = []
        for scan in user_scans:
            scans.append(QRCodeResponse(
                qr_codes=[scan.to_dict()]  # Wrap the single scan item in a list
            ))
        return scans  # Return the list of QRCodeResponse items
    except Exception as e:
        raise HTTPException(status_code=404, detail="User not found")





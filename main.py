from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

# --- CORS MIDDLEWARE ---
# This allows the Base44 frontend to talk to this Render backend safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (POST, GET, etc.)
    allow_headers=["*"],  # Allows all headers
)

# --- CONFIGURATION ---
# Your BigFat Tech Solution credentials
HIVE_API_KEY = "hyRTmij5G6i08V41DMzPOw=="
HIVE_URL = "https://api.thehive.ai/api/v2/models/ai_generated_image_detection/predict"

@app.get("/")
async def root():
    """Testing route: Visit your Render URL in a browser to see this."""
    return {
        "status": "online",
        "service": "BigFat AI Detector API",
        "message": "Ready for Base44 connection"
    }

@app.post("/detect")
async def detect_ai(file: UploadFile = File(...)):
    """Main detection route for Base44 uploads"""
    try:
        # 1. Read the image file content
        content = await file.read()
        
        # 2. Set up headers and the file for the Hive API
        headers = {"Authorization": f"token {HIVE_API_KEY}"}
        files = {"media": (file.filename, content, file.content_type)}

        # 3. Send the data to Hive for analysis
        response = requests.post(HIVE_URL, headers=headers, files=files)
        
        # Check if the Hive API rejected the request
        if response.status_code != 200:
            return {
                "error": "External API Error",
                "details": response.text,
                "status_code": response.status_code
            }

        # 4. Parse the response
        data = response.json()
        
        # Extract the score and class (Hive returns a list in 'status')
        status_list = data.get('status', [])
        if not status_list:
             return {"error": "No status returned from detection service"}
             
        prediction = status_list[0]
        
        # 5. Return clean data to Base44
        return {
            "is_ai": prediction.get('class') == 'yes',
            "confidence": prediction.get('score', 0),
            "filename": file.filename,
            "provider": "BigFat Tech Solution"
        }

    except Exception as e:
        # Catch any unexpected errors (like network issues)
        raise HTTPException(status_code=500, detail=str(e))

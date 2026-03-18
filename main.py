from fastapi import FastAPI, UploadFile, File, HTTPException
import requests
import os

app = FastAPI()

# You will get this API Key from HiveModeration.com
HIVE_API_KEY = "hyRTmij5G6i08V41DMzPOw=="
HIVE_URL = "https://api.thehive.ai/api/v2/models/ai_generated_image_detection/predict"

@app.post("/detect")
async def detect_ai(file: UploadFile = File(...)):
    # 1. Read the file uploaded from Base44
    content = await file.read()
    
    # 2. Prepare the request for the Hive AI
    headers = {"Authorization": f"token {hyRTmij5G6i08V41DMzPOw==}"}
    files = {"media": (file.filename, content, file.content_type)}

    # 3. Ask Hive if it's AI
    response = requests.post(HIVE_URL, headers=headers, files=files)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="AI Detection Service failed")

    # 4. Return the result back to your Base44 site
    data = response.json()
    return {
        "is_ai": data['status'][0]['class'] == 'yes',
        "confidence": data['status'][0]['score'],
        "message": "Analysis complete by BigFat Tech Solution"
    }

from fastapi import FastAPI, UploadFile, File, HTTPException
import requests
import os

app = FastAPI()

# Your API Key is safely stored in this variable
HIVE_API_KEY = "hyRTmij5G6i08V41DMzPOw=="
HIVE_URL = "https://api.thehive.ai/api/v2/models/ai_generated_image_detection/predict"

@app.post("/detect")
async def detect_ai(file: UploadFile = File(...)):
    # 1. Read the file uploaded from Base44
    content = await file.read()
    
    # 2. Prepare the request for the Hive AI
    # FIX: We use the variable HIVE_API_KEY here instead of the raw key
    headers = {"Authorization": f"token {HIVE_API_KEY}"}
    files = {"media": (file.filename, content, file.content_type)}

    # 3. Ask Hive if it's AI
    try:
        response = requests.post(HIVE_URL, headers=headers, files=files)
        
        if response.status_code != 200:
            # This helps you see the actual error from Hive if it fails
            return {"error": "Hive API Error", "details": response.text}

        # 4. Return the result back to your Base44 site
        data = response.json()
        
        # Hive returns a list of results, we take the first one
        status_data = data.get('status', [{}])[0]
        
        return {
            "is_ai": status_data.get('class') == 'yes',
            "confidence": status_data.get('score', 0),
            "message": "Analysis complete by BigFat Tech Solution"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

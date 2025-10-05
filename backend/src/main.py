import os
import io
import json
import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse, StreamingResponse
from sklearn.ensemble import RandomForestClassifier
from dotenv import load_dotenv

from src.utils.gemini_api import call_gemini
from src.utils.image_utils import generate_planet_image, process_uploaded_image

load_dotenv()

app = FastAPI(title="Ovydra AI - Advanced Exoplanet Analysis")

MODEL_PATH = "src/model/exoplanet_model.joblib"
USER_MEMORY_FILE = "src/model/user_memory.json"

# Load NASA exoplanet data
try:
    df = pd.read_csv(
        "https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets&format=csv"
    )
    df.fillna(0, inplace=True)
    print(f"Loaded NASA Exoplanet data, rows: {len(df)}")
except Exception as e:
    print(f"Failed to load NASA exoplanet data: {e}")
    df = pd.DataFrame()

# Load or train model
if not os.path.exists(MODEL_PATH) and not df.empty:
    if 'pl_name' in df.columns and 'pl_bmasse' in df.columns and 'pl_rade' in df.columns:
        X = df[['pl_bmasse', 'pl_rade']].fillna(0)
        y = df['pl_name'].astype(str)
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X, y)
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump(model, MODEL_PATH)
    else:
        model = None
else:
    model = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None

# Ensure user memory file exists
os.makedirs(os.path.dirname(USER_MEMORY_FILE), exist_ok=True)
if not os.path.exists(USER_MEMORY_FILE):
    with open(USER_MEMORY_FILE, "w") as f:
        json.dump([], f)

@app.post("/analyze/")
async def analyze(prompt: str = Form(...), upload_file: UploadFile = None):
    response_text = ""
    radius = 10  # default planet radius

    if upload_file:
        try:
            file_bytes = await upload_file.read()
            radius = process_uploaded_image(file_bytes)
            response_text += f"Detected object radius: {radius} px. "
        except Exception as e:
            response_text += f"Image processing error: {e}. "

    if model and not df.empty:
        try:
            X_input = np.array([[df['pl_bmasse'].mean(), df['pl_rade'].mean()]])
            pred = model.predict(X_input)[0]
            response_text += f"Predicted exoplanet: {pred}. "
        except Exception as e:
            response_text += f"ML prediction error: {e}. "

    gemini_response = call_gemini(prompt)
    if gemini_response:
        response_text += f"Gemini AI context: {gemini_response} "

    try:
        with open(USER_MEMORY_FILE, "r+") as f:
            memory = json.load(f)
            memory.append({"prompt": prompt, "response": response_text})
            f.seek(0)
            json.dump(memory, f, indent=2)
    except Exception as e:
        print(f"Failed to save memory: {e}")

    planet_image = generate_planet_image(radius=radius)

    return StreamingResponse(planet_image, media_type="image/png")


@app.get("/memory/")
def get_memory():
    try:
        with open(USER_MEMORY_FILE, "r") as f:
            memory = json.load(f)
        return JSONResponse(content=memory)
    except Exception as e:
        return JSONResponse(content={"error": str(e)})


@app.get("/")
def root():
    return {"message": "Ovydra AI Backend Online. Use /analyze/ to submit prompt or file."}

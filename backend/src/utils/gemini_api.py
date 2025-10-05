import os
import requests
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def call_gemini(prompt: str) -> str:
    """
    Call Gemini AI API with a prompt and return the response as string.
    Handles API errors and returns empty string if fails.
    """
    try:
        url = "https://api.gemini.ai/analyze"
        headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}
        data = {"prompt": prompt}
        response = requests.post(url, json=data, headers=headers, timeout=15)
        if response.status_code == 200:
            return response.json().get("response", "")
        return ""
    except Exception as e:
        print(f"Gemini API error: {e}")
        return ""

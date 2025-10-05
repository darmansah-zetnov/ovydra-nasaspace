import numpy as np
import cv2
import io

def generate_planet_image(radius: float = 10) -> io.BytesIO:
    """
    Generate a simple red planet image with given radius (default 10).
    Returns a BytesIO object with PNG data.
    """
    img = np.zeros((300, 300, 3), dtype=np.uint8)
    center = (150, 150)
    color = (0, 0, 255)  # Red planet
    cv2.circle(img, center, int(radius * 5), color, -1)
    _, buffer = cv2.imencode(".png", img)
    return io.BytesIO(buffer)

def process_uploaded_image(file_bytes: bytes) -> int:
    """
    Process uploaded image and return the radius of the largest object detected.
    """
    try:
        npimg = np.frombuffer(file_bytes, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest = max(contours, key=cv2.contourArea)
            (_, _), radius = cv2.minEnclosingCircle(largest)
            return int(radius)
    except Exception as e:
        print(f"Image processing error: {e}")
    return 0

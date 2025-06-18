import cv2
from flask import Flask, jsonify 
from flask_cors import CORS 

PARKING_SPOTS = [
    (50, 50, 150, 150),
    (200, 50, 300, 150),
    (350, 50, 450, 150),
    (500, 50, 600, 150),
    (50, 200, 150, 300),
    (200, 200, 300, 300),
    (350, 200, 450, 300),
    (500, 200, 600, 300),
    (50, 350, 150, 450),
    (200, 350, 300, 450),
]
PIXEL_THRESHOLD = 5000
IMAGE_PATH = "im2.png"

def analyze_parking_status():
    print("Starting parking status analysis...")
    image = cv2.imread(IMAGE_PATH)
    if image is None:
        print(f"Error: file '{IMAGE_PATH}' not found or cannot be read!")
        return []
    print("Image successfully read.")

    try:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print("Image converted to grayscale.")
    except Exception as e:
        print(f"Critical error converting image to grayscale: {e}")
        return []

    statuses = []
    for i, (x1, y1, x2, y2) in enumerate(PARKING_SPOTS):
        try:
            if y1 >= gray_image.shape[0] or y2 > gray_image.shape[0] or \
               x1 >= gray_image.shape[1] or x2 > gray_image.shape[1] or \
               y1 < 0 or x1 < 0:
                print(f"Warning: Coordinates for spot {i+1} ({x1},{y1},{x2},{y2}) are out of image bounds {gray_image.shape}.")
                statuses.append({"id": i + 1, "status": "out_of_bounds"})
                continue

            roi = gray_image[y1:y2, x1:x2]
            _, thresh = cv2.threshold(roi, 120, 255, cv2.THRESH_BINARY)
            white_pixels = cv2.countNonZero(thresh)
            is_free = white_pixels > PIXEL_THRESHOLD

            spot_status = {
                "id": i + 1,
                "status": "free" if is_free else "occupied"
            }
            statuses.append(spot_status)
            print(f"Spot {i+1} processed. Status: {spot_status['status']}")
        except Exception as e:
            print(f"Error processing parking spot {i+1}: {e}")
            statuses.append({"id": i + 1, "status": "error"})

    print("Parking status analysis completed.")
    return statuses

# Function call for testing
result = analyze_parking_status()
print("\nAnalysis Result:", result)

#python -m http.server 8000

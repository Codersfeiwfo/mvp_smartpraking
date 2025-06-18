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
    print("Начинаем анализ парковочного статуса (в Colab)...")
    image = cv2.imread(IMAGE_PATH)
    if image is None:
        print(f"Ошибка: файл '{IMAGE_PATH}' не найден или не может быть прочитан! (в Colab)")
        return []
    print("Изображение успешно прочитано (в Colab).")

    try:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print("Изображение преобразовано в оттенки серого (в Colab).")
    except Exception as e:
        print(f"Критическая ошибка при преобразовании изображения в оттенки серого (в Colab): {e}")
        return []

    statuses = []
    for i, (x1, y1, x2, y2) in enumerate(PARKING_SPOTS):
        try:
            if y1 >= gray_image.shape[0] or y2 > gray_image.shape[0] or \
               x1 >= gray_image.shape[1] or x2 > gray_image.shape[1] or \
               y1 < 0 or x1 < 0:
                print(f"Предупреждение: Координаты места {i+1} ({x1},{y1},{x2},{y2}) выходят за границы изображения {gray_image.shape}.")
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
            print(f"Место {i+1} обработано. Статус: {spot_status['status']}")
        except Exception as e:
            print(f"Ошибка при обработке парковочного места {i+1}: {e}")
            statuses.append({"id": i + 1, "status": "error"})

    print("Анализ парковочного статуса завершен (в Colab).")
    return statuses

# Вызов функции для проверки
result = analyze_parking_status()
print("\nРезультат анализа:", result)

#python -m http.server 8000

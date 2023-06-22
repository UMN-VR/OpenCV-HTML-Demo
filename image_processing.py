# image_processing.py

import cv2
import json
import numpy as np

def load_image(file_name):
    image = cv2.imread(file_name)
    if image is None:
        print(f"Unable to open image file: {file_name}")
    return image

def process_image(image, objects_data):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rectangle_multiplier = 1.0
    results = []
    max_id = max([obj['id'] for obj in objects_data], default=-1)

    for i, contour in enumerate(contours):
        M = cv2.moments(contour)
        
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            continue

        x, y, w, h = cv2.boundingRect(contour)
        w = int(w * rectangle_multiplier)
        h = int(h * rectangle_multiplier)
        x = int(cX - w / 2)
        y = int(cY - h / 2)
        area = cv2.contourArea(contour)

        for obj in objects_data:
            obj_centroid = np.array(obj['position'])
            current_centroid = np.array([cX, cY])
            if np.linalg.norm(obj_centroid - current_centroid) <= np.hypot(w / 2, h / 2):
                id_ = obj['id']  # Use the existing ID
                break
        else:
            max_id += 1
            id_ = max_id  # Assign a new ID

        results.append({
            'id': id_,
            'position': (cX, cY),
            'size': area,
            'rect_coords': (x, y, w, h)
        })

    with open('objects.json', 'w') as json_file:
        json.dump(results, json_file, indent=4)

    return image, results

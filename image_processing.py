# image_processing.py

import cv2    #Import OpenCV so we can use Computer Vision
import json    #Import JSON so we can use JSON object Format
import numpy as np    #Import numpy so we can do matrix math and treat the image as a pixel value matrix

def load_image(file_name):    #Create a new function called "load image" that takes in an image file (from file name give as parameter) and turns it into a pixel value matrix
    image = cv2.imread(file_name)    #Read in image as matrix of color values!
    if image is None:    #If the image matrix is empty, print out an error
        print(f"Unable to open image file: {file_name}")
    return image    #return image pixel matrix!

def process_image(image, objects_data):    #Create a new function called "process image." Take in two parameters, the image array parameter and a json object for results
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)     #Convert color encoding of image matrix 
    lower_red = np.array([0, 100, 100])    #Create an single pixle array. This 
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

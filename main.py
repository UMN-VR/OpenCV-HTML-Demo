import os
import cv2
import json
import subprocess
from image_processing import load_image, process_image
from html_generator import generate_html
import numpy as np

def get_objects_data():
    if os.path.exists('objects.json'):
        with open('objects.json', 'r') as json_file:
            return json.load(json_file)
    else:
        return []

def perspective_transform(image, toggle='original'):
    # Check if the image is valid
    if image is None:
        print("Invalid image.")
        return None
    # Split the image into two halves
    mid_point = image.shape[1] // 2
    original = image[:, :mid_point]
    processed = image[:, mid_point:]
    # Check if the splitting worked correctly
    print(f"Original shape: {original.shape}, Processed shape: {processed.shape}")
    # Choose the image based on the toggle
    if toggle == 'original':
        chosen_image = original
    elif toggle == 'processed':
        chosen_image = processed
    else:
        raise ValueError("Toggle must be 'original' or 'processed'")
    
    try:
        # Convert to HSV
        hsv = cv2.cvtColor(chosen_image, cv2.COLOR_BGR2HSV)
        # Check the hsv conversion
        print(f"HSV shape: {hsv.shape}, Type: {type(hsv)}")
        # Define color range for mask
        lower_range = np.array([10, 80, 80])
        upper_range = np.array([70, 255, 255])
        # Create mask
        mask = cv2.inRange(hsv, lower_range, upper_range)
        # Check the mask
        print(f"Mask shape: {mask.shape}, Type: {type(mask)}")
        # Find the points where the mask is white
        y, x = np.where(mask == 255)
        points = np.transpose(np.vstack((x, y)))
        # Find minimum area rectangle
        rect = cv2.minAreaRect(points)
        # Get the four corners of the rectangle
        box = cv2.boxPoints(rect)
        box = np.int0(box)  # Convert to int
        # Draw the rectangle on the mask for visual verification
        mask_with_rectangle = cv2.drawContours(mask.copy(), [box], 0, (255, 0, 0), 2)
        # Save the mask with rectangle for inspection
        cv2.imwrite(f'{toggle}_mask_with_rectangle.png', mask_with_rectangle)
        # Extract corner points
        pts1 = np.float32(box)
        # Define points for output image
        width, height = 500, 500
        pts2 = np.float32([[0, 0], [width, 0], [height, 0], [0, height]])
        # Compute transformation matrix
        M = cv2.getPerspectiveTransform(pts1, pts2)
        # Check the transformation matrix
        print(f"Transformation Matrix: {M}")
        # Perform perspective transformation
        transformed = cv2.warpPerspective(chosen_image, M, (width, height))
        return transformed
    except Exception as e:
        print(f"Error during perspective transform: {str(e)}")
        return chosen_image


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    while True:
        file_name = input("Enter the file name (or 'exit' to stop): ")
        if file_name.lower() == 'exit':
            break
        objects_data = get_objects_data()
        image = load_image(file_name)
        if image is None:
            print(f"Could not load image {file_name}")
            continue
        toggle = input("Enter which image to transform (original/processed): ")
        image = perspective_transform(image, toggle)
        if image is None:
            print(f"Could not transform image {file_name}")
            continue
        # Save the transformed image for inspection
        cv2.imwrite(f'{file_name}_{toggle}_transformed.png', image)
        image, results = process_image(image, objects_data)
        modified_image_file = "modified_image.jpg"
        for result in results:
            x, y, w, h = result['rect_coords']
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            print(f"ID: {result['id']}, Position: {result['position']}, Size: {result['size']}")
        cv2.imwrite(modified_image_file, image)
        result_file_name, ext = os.path.splitext(file_name)
        result_file_name += "_result.html"
        generate_html(modified_image_file, results, result_file_name)
        cv2.destroyAllWindows()
        os.remove(modified_image_file)
        print(f"\nHTML file generated successfully.\n")
        # Open the HTML file
        subprocess.run(["xdg-open", result_file_name], stderr=subprocess.DEVNULL)  # Redirect stderr to /dev/null

if __name__ == '__main__':
    main()

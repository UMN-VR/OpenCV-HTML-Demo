import os
import cv2
import json
import subprocess
from image_processing import load_image, process_image
from html_generator import generate_html

def get_objects_data():
    if os.path.exists('objects.json'):
        with open('objects.json', 'r') as json_file:
            return json.load(json_file)
    else:
        return []

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    while True:
        file_name = input("Enter the file name (or 'exit' to stop): ")

        if file_name.lower() == 'exit':
            break

        objects_data = get_objects_data()
        image = load_image(file_name)
        if image is None:
            continue

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

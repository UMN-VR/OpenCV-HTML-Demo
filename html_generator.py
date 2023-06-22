#html_generator.py
import base64
from jinja2 import Template
import cv2

def generate_html(image_file, results, output_file):
    with open(image_file, "rb") as f:
        image_data = f.read()

    encoded_image = base64.b64encode(image_data).decode()

    # Prepare HTML content
    html_template = Template("""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .image-container {
                position: relative;
                display: inline-block;
            }
            .image-container img {
                display: block;
                margin: 0;
                padding: 0;
                max-width: 100%;
                height: auto;
            }
            .rectangle {
                position: absolute;
                border: 2px solid green;
                transform: translate(-50%, -50%);
            }
            .tooltip {
                visibility: hidden;
                background-color: rgba(0, 0, 0, 0.7);
                color: white;
                text-align: center;
                border-radius: 4px;
                padding: 2px 5px;
                position: absolute;
                z-index: 1;
                transform: translate(-50%, -100%);
                white-space: nowrap;
            }
            .rectangle:hover .tooltip {
                visibility: visible;
            }
        </style>
    </head>
    <body>
        <div class="image-container">
            <img src="data:image/jpeg;base64,{{ encoded_image }}" alt="Image" id="image">
            <!-- Add the rectangles and tooltips -->
            {% for result in results %}
            <div class="rectangle" style="top: {{ (result['rect_coords'][1] + result['rect_coords'][3]//2) / image_height * 100 }}%; left: {{ (result['rect_coords'][0] + result['rect_coords'][2]//2) / image_width * 100 }}%; width: {{ result['rect_coords'][2] }}px; height: {{ result['rect_coords'][3] }}px; transform: translate(-50%, -50%);">
                <div class="tooltip">
                    <strong>ID:</strong> {{ result['id'] }}<br>
                    <strong>Position:</strong> {{ result['position'] }}<br>
                    <strong>Size:</strong> {{ result['size'] }}
                </div>
            </div>
            {% endfor %}
        </div>
    </body>
    </html>
    """)

    # Get the image dimensions
    image = cv2.imread(image_file)
    image_height, image_width, _ = image.shape

    html_content = html_template.render(encoded_image=encoded_image, results=results, image_height=image_height, image_width=image_width)

    # Save the HTML file
    with open(output_file, "w") as html_file:
        html_file.write(html_content)

    print("HTML file generated successfully.")

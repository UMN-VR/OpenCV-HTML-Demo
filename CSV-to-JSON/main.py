import csv
import json
import os

csv_location = '/home/goldyosv7/Desktop/OpenCV-HTML/CSV-to-JSON/'
csv_filename = os.path.join(csv_location, 'RootPainterData.csv')
output_directory = os.path.join(csv_location, 'output')

# Read the CSV file and generate data structures
crop_data = {}

with open(csv_filename, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:
        file_name = row['file_name']
        crop_number = file_name[-4:]
        date = file_name[:8]
        area = float(row['area'])

        # Check if the area is greater than 3
        if area <= 3:
            continue

        if crop_number.startswith('p'):
            crop_number = crop_number[1:]

        if crop_number not in crop_data:
            crop_data[crop_number] = {}

        if date not in crop_data[crop_number]:
            crop_data[crop_number][date] = []

        entry = {
            'x': float(row['x']),
            'y': float(row['y']),
            'diameter': float(row['diameter']),
            'perimeter': float(row['perimeter']),
            'eccentricity': float(row['eccentricity'])
        }

        crop_data[crop_number][date].append(entry)

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Write the grouped data as JSON files
for crop_number, data in crop_data.items():
    output_filename = os.path.join(output_directory, f'crop{crop_number}.json')

    with open(output_filename, 'w') as json_file:
        json.dump(data, json_file)

    print(f"JSON file created for crop {crop_number}: {output_filename}")

print("All JSON files have been created.")

import json
import matplotlib.pyplot as plt
import os

def load_data(json_file):
    """
    Load nodule information from the JSON file.
    
    :param json_file: Path to the JSON file containing the nodule information.
    :return: The loaded nodule information as a Python dictionary.
    """

    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"No file found for the name {json_file}")
        return None


def match_ids(nodule_info, current_date, next_date):
    """
    Find the closest nodule at the next date for each nodule at the current date and match their IDs.
    
    :param nodule_info: The nodule information.
    :param current_date: The current date.
    :param next_date: The next date.
    :return: A dictionary with the IDs of the nodules at the current date as the keys and the IDs of the closest nodules
             at the next date as the values.
    """
    current_nodules = nodule_info[current_date]
    next_nodules = nodule_info[next_date]
    id_mapping = {}

    # Iterate over current nodules
    for i in range(len(current_nodules)):
        current_nodule = current_nodules[i]
        current_x = current_nodule['x']
        current_y = current_nodule['y']
        closest_nodule = None
        min_distance = float('inf')

        # Find the closest nodule in the next date
        for j in range(len(next_nodules)):
            next_nodule = next_nodules[j]
            next_x = next_nodule['x']
            next_y = next_nodule['y']
            distance = ((current_x - next_x) ** 2 + (current_y - next_y) ** 2) ** 0.5

            if distance < min_distance:
                closest_nodule = next_nodule
                min_distance = distance

        if closest_nodule:
            current_id = i + 1
            next_id = next_nodules.index(closest_nodule) + 1
            id_mapping[current_id] = next_id

    return id_mapping


def plot_flow_field(nodule_info, current_date, next_date, id_mapping, output_dir):

    """
    Plot the movement of the nodules from the current date to the next date as a flow field.
    
    :param nodule_info: The nodule information.
    :param current_date: The current date.
    :param next_date: The next date.
    :param id_mapping: The ID mapping from the current date to the next date.
    """
    current_nodules = nodule_info[current_date]
    next_nodules = nodule_info[next_date]

    # Set up the plot
    plt.figure(figsize=(8, 6))

    # Plot current nodules
    for nodule in current_nodules:
        x = nodule['x']
        y = nodule['y']
        nodule_id = current_nodules.index(nodule) + 1
        plt.text(x, y, str(nodule_id), ha="center", va="center", color='blue')

    # Plot next nodules and connect them with lines
    for nodule in next_nodules:
        x = nodule['x']
        y = nodule['y']
        nodule_id = next_nodules.index(nodule) + 1
        plt.text(x, y, str(nodule_id), ha="center", va="center", color='red')

        if nodule_id in id_mapping.values():
            current_id = [key for key, value in id_mapping.items() if value == nodule_id][0]
            if current_id <= len(current_nodules):
                current_nodule = current_nodules[current_id - 1]
                current_x = current_nodule['x']
                current_y = current_nodule['y']
                plt.plot([current_x, x], [current_y, y], color='black')
            else:
                print("Current ID out of range")

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'Flow Field: {current_date} to {next_date}')
    plt.axis('equal')

    # Save the plot as an image
    plt.savefig(os.path.join(output_dir, f'flow_field_{current_date}_{next_date}.png'))
    plt.close()

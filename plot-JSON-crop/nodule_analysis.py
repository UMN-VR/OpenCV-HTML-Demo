# nodule_analysis.py
from nodule_utils import load_data, match_ids, plot_flow_field
from logger import NoduleAnalysisLogger
import json
import os

path = "OpenCV-HTML/plot-JSON-crop/"

def generate_flow_fields(json_file):
    filename = path + os.path.basename(json_file)
    logger = NoduleAnalysisLogger("nodule_analysis.log", filename).get_logger()
    logger.info('Loading data from json file.')
    nodule_info = load_data(json_file)

    dates = list(nodule_info.keys())
    dates.sort()  # This sorts dates in ascending order, i.e., from the earliest to the latest

    logger.info('Data loaded successfully. Starting analysis.')

    for i in range(len(dates) - 1):
        current_date = dates[i]
        next_date = dates[i + 1]
        logger.info(f'Matching IDs for dates: {current_date} and {next_date}.')
        id_mapping = match_ids(nodule_info, current_date, next_date)
        logger.info(f'Plotting flow field for dates: {current_date} and {next_date}.')
        plot_flow_field(nodule_info, current_date, next_date, id_mapping)
        logger.info(f'Flow field for dates: {current_date} and {next_date} plotted successfully.')

        # Collect the data between the transition into a dictionary
        transition_data = {
            'cd': current_date,
            'nd': next_date,
            'c_nodules': [[round(nodule['x'], 2), round(nodule['y'], 2), round(nodule['diameter'], 2), 
                          round(nodule['perimeter'], 2), round(nodule['eccentricity'], 4)] 
                         for nodule in nodule_info[current_date]],
            'n_nodules': [[round(nodule['x'], 2), round(nodule['y'], 2), round(nodule['diameter'], 2), 
                          round(nodule['perimeter'], 2), round(nodule['eccentricity'], 4)] 
                         for nodule in nodule_info[next_date]],
            'id_map': id_mapping
        }

        # Save the transition data as a separate JSON file for each transition
        transition_file = f'transition_data_{current_date}_{next_date}.json'
        with open(transition_file, 'w') as f:
            json.dump(transition_data, f, indent=4)

        logger.info(f'Transition data saved to {transition_file}.')

    logger.info('Analysis complete.')



if __name__ == '__main__':
    json_file = input("Enter the path to the JSON file: ")
    generate_flow_fields(json_file)

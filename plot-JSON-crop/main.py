#main.py
import json
import nodule_utils
from nodule_analysis import generate_flow_fields
from logger import NoduleAnalysisLogger
import os

def main():
    json_file = input("Enter the path to the JSON file: ")

    # Create an output directory for this run
    output_dir = f"{os.path.splitext(json_file)[0]}-output"
    os.makedirs(output_dir, exist_ok=True)

    # Initialize the logger
    logger = NoduleAnalysisLogger("nodule_analysis.log", output_dir).get_logger()

    # Call the nodule analysis function
    logger.info("Starting nodule analysis.")
    generate_flow_fields(json_file)
    logger.info("Nodule analysis completed.")


if __name__ == '__main__':
    main()

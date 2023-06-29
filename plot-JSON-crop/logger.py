# logger.py
import logging
import os

class NoduleAnalysisLogger:
    def __init__(self, filename, output_dir):
        self.logger = logging.getLogger("nodule_analysis")
        self.logger.setLevel(logging.INFO)
        
        # Create a file handler
        f_handler = logging.FileHandler(os.path.join(output_dir, filename))
        f_handler.setLevel(logging.INFO)
        
        # Create a formatter and add it to the handler
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        f_handler.setFormatter(f_format)
        
        # Add the handler to the logger
        self.logger.addHandler(f_handler)
    
    def get_logger(self):
        return self.logger

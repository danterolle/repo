import os
import logging

def setup_logging(log_name):
    # Get the directory of the script file
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Create the tmp folder in the same directory as the script file
    tmp_dir = os.path.join(script_dir, 'tmp')
    os.makedirs(tmp_dir, exist_ok=True)

    # Create the complete path for the log file inside the tmp folder
    log_file_path = os.path.join(tmp_dir, log_name)

    # Use logging lib to check any errors
    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(filename=log_file_path, filemode='w', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    logging.info(f"Logging initialized. Log file: {log_file_path}")
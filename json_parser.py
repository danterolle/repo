# This script recursively processes a specified root directory, 
# identifies "Packages" files within it, extracts information from these files, 
# and saves the parsed data in JSON format. 

# The resulting JSON files are organized in a specified output directory,
# maintaining the directory structure of the input. 

import os
import re
import json
import argparse
import logging

def parse_packages(package_content):
    """
    Parse the content of a Packages file and extract information for each package entry.

    Args:
        package_content (str): The content of the Packages file.

    Returns:
        list: A list of dictionaries, each representing a parsed package entry.
    """
    
    packages = []
    current_package = {}
    current_id = 1

    # Split the file content into individual packages
    package_entries = re.split(r'\n\n', package_content.strip())

    for entry in package_entries:
        lines = entry.strip().split('\n')

        for line in lines:
            # Split each line into key and value
            parts = line.split(': ', 1)
            if len(parts) == 2:
                key, value = map(str.strip, parts)
            else:
                key, value = parts[0].strip(), ""

            # Check for the start of a new package entry
            if key == 'Package':
                if current_package:
                    current_package['id'] = current_id
                    packages.append(current_package)
                    current_id += 1
                current_package = {'id': current_id}

            # Handle multi-line fields
            if key in current_package:
                current_package[key] += '\n' + value
            else:
                current_package[key] = value

    if current_package:
        current_package['id'] = current_id
        packages.append(current_package)

    return packages

def process_packages_file(input_path, output_directory, input_directory, recursive):
    """
    Process a Packages file, parse its content, and save the extracted information as JSON.

    Args:
        input_path (str): Path to the Packages file to be processed.
        output_directory (str): Path to the directory for saving JSON outputs.
        input_directory (str): Path to the root directory containing Packages files.
        recursive (bool): Whether to recursively process subdirectories.
    """
    
    # Read the content of the Packages file
    with open(input_path, 'r', encoding='utf-8') as file:
        packages_content = file.read()

    # Parse the Packages content
    parsed_packages = parse_packages(packages_content)

    # Convert the parsed data to JSON
    json_data = json.dumps(parsed_packages, indent=2)

    # Determine the output path based on the input path
    relative_input_path = os.path.relpath(input_path, input_directory)

    if recursive:
        output_path = os.path.join(output_directory, relative_input_path)
    else:
        output_path = os.path.join(output_directory, os.path.basename(input_path))

    output_path = os.path.splitext(output_path)[0] + '.json'

    # Save the JSON data to a file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json_file.write(json_data)

    logging.info(f"JSON data saved to {output_path}.")

def setup_logging():
    # Get the directory of the script file
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Create the tmp folder in the same directory as the script file
    tmp_dir = os.path.join(script_dir, 'tmp')
    os.makedirs(tmp_dir, exist_ok=True)

    # Create the complete path for the log file inside the tmp folder
    log_file_path = os.path.join(tmp_dir, 'json_parser.log')

    # Use logging lib to check any errors
    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(filename=log_file_path, filemode='w', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    logging.info(f"Logging initialized. Log file: {log_file_path}")

def main():
    parser = argparse.ArgumentParser(description="Parse multiple Packages files and save JSON outputs.")
    parser.add_argument("input_directory", help="Path to the root directory containing Packages files.")
    parser.add_argument("output_directory", help="Path to the directory for saving JSON outputs.")
    parser.add_argument("--recursive", action="store_true", help="Recursively process subdirectories.")
    args = parser.parse_args()

    # Verify that the input directory exists
    if not os.path.exists(args.input_directory) or not os.path.isdir(args.input_directory):
        logging.error("Error: The specified input directory does not exist.")
        return

    # Create the output directory if it doesn't exist
    os.makedirs(args.output_directory, exist_ok=True)

    # Process each Packages file in the input directory
    for root, _, files in os.walk(args.input_directory):
        for filename in files:
            if filename.endswith('Packages'):
                input_path = os.path.join(root, filename)
                logging.info(f"Processing file: {input_path}")
                process_packages_file(input_path, args.output_directory, args.input_directory, args.recursive)

    logging.info(f"All Packages files in {args.input_directory} have been processed. JSON outputs saved to {args.output_directory}.")

if __name__ == "__main__":
    setup_logging()
    main()

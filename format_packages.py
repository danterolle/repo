# This script performs formatting operations on Debian Packages files. 
# It processes each package block within the input files, updates the description 
# and tag fields, and saves the modified content to new output files.

# Why this script?

# The problem:

import os
import re
import argparse
from tqdm import tqdm

def format_description(description):
    # Remove empty lines at the beginning and end of the Description
    description = description.strip()

    # Merge description lines into a single text block
    description = ''.join(description.split('\n'))

    return description

def format_tag(tag):
    # Remove leading and trailing whitespace from the Tag
    tag = tag.strip()

    # Remove extra spaces within the Tag
    tag = ' '.join(tag.split())

    return tag

def update_package_info(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        # Read the entire content of the file
        content = file.read()

        # Find blocks related to each package
        package_blocks = re.split(r'\n\n', content)

        # Iterate over package blocks
        for i, package_block in tqdm(enumerate(package_blocks), desc="Processing Packages", total=len(package_blocks)):
            # Find the description in the package block
            match_description = re.search(r'Description:(.*?)(?=\n\w|\Z)', package_block, re.DOTALL)
            if match_description:
                description = match_description.group(1).strip()
                formatted_description = format_description(description)

                # Replace the old description with the formatted one
                package_block = package_block.replace(description, formatted_description)

            # Find the tag in the package block
            match_tag = re.search(r'Tag:(.*?)(?=\n\w|\Z)', package_block, re.DOTALL)
            if match_tag:
                tag = match_tag.group(1).strip()
                formatted_tag = format_tag(tag)

                # Replace the old tag with the formatted one
                package_block = package_block.replace(tag, formatted_tag)

            # Update the package block in the content
            package_blocks[i] = package_block

        # Join the package blocks back together
        updated_content = '\n\n'.join(package_blocks)

    # Scrivi il nuovo contenuto nel file di output
    with open(output_file_path, 'w') as file:
        file.write(updated_content)

def format_all_packages(input_dir, output_dir):
    # Iterate over Packages files in the input directory
    for filename in os.listdir(input_dir):
        if filename.startswith("Packages"):
            input_file_path = os.path.join(input_dir, filename)
            output_file_path = os.path.join(output_dir, f"processed_{filename}")
            
            # Perform description and tag updates, and save the result to a new file
            update_package_info(input_file_path, output_file_path)

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Format Debian Packages files in a specified directory.")
    parser.add_argument("input_directory", help="Specify the input directory containing Packages files.")
    parser.add_argument("output_directory", help="Specify the output directory for processed Packages files.")

    # Parse command-line arguments
    args = parser.parse_args()

    # Perform formatting for all Packages files in the specified directory
    format_all_packages(args.input_directory, args.output_directory)

if __name__ == "__main__":
    main()

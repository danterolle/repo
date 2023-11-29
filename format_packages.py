# This script performs formatting operations on Parrot/Debian Packages files. 
# It processes each package block within the input files, updates the description 
# and tag fields, and saves the modified content to new output files.

# Why this script?

# Within Packages, you will find all the packages, each of which 
# has a variety of attributes that identify it. For example:

"""
Package: 0ad
Version: 0.0.26-3
Installed-Size: 28591
Maintainer: Debian Games Team <pkg-games-devel@lists.alioth.debian.org>
Architecture: amd64
Depends: 0ad-data (>= 0.0.26), 0ad-data (<= 0.0.26-3), 0ad-data-common (>= 0.0.26), 0ad-data-common (<= 0.0.26-3), libboost-filesystem1.74.0 (>= 1.74.0), libc6 (>= 2.34), libcurl3-gnutls (>= 7.32.0), libenet7, libfmt9 (>= 9.1.0+ds1), libfreetype6 (>= 2.2.1), libgcc-s1 (>= 3.4), libgloox18 (>= 1.0.24), libicu72 (>= 72.1~rc-1~), libminiupnpc17 (>= 1.9.20140610), libopenal1 (>= 1.14), libpng16-16 (>= 1.6.2-1), libsdl2-2.0-0 (>= 2.0.12), libsodium23 (>= 1.0.14), libstdc++6 (>= 12), libvorbisfile3 (>= 1.1.2), libwxbase3.2-1 (>= 3.2.1+dfsg), libwxgtk-gl3.2-1 (>= 3.2.1+dfsg), libwxgtk3.2-1 (>= 3.2.1+dfsg-2), libx11-6, libxml2 (>= 2.9.0), zlib1g (>= 1:1.2.0)
Pre-Depends: dpkg (>= 1.15.6~)
Size: 7891488
SHA256: 3a2118df47bf3f04285649f0455c2fc6fe2dc7f0b237073038aa00af41f0d5f2
SHA1: 9ea2aed7feb4ec340ff1d2a61e335a825cad1eca
MD5sum: 4d471183a39a3a11d00cd35bf9f6803d
Description: Real-time strategy game of ancient warfare
 0 A.D. (pronounced "zero ey-dee") is a free, open-source, cross-platform
 real-time strategy (RTS) game of ancient warfare. In short, it is a
 historically-based war/economy game that allows players to relive or rewrite
 the history of Western civilizations, focusing on the years between 500 B.C.
 and 500 A.D. The project is highly ambitious, involving state-of-the-art 3D
 graphics, detailed artwork, sound, and a flexible and powerful custom-built
 game engine.
Homepage: https://play0ad.com/
Tag: game::strategy, interface::graphical, interface::x11, role::program,
 uitoolkit::sdl, uitoolkit::wxwidgets, use::gameplaying,
 x11::application
Section: games
Priority: optional
Filename: pool/main/0/0ad/0ad_0.0.26-3_amd64.deb
"""

# The goal of this project, REPO, is to have all ParrotOS packages available 
# in JSON format. 

# As you can see from the example above, though, after several trials, 
# the Description and Tag attributes continue their description in multiple lines, 
# making it difficult to standardize the conversion to JSON.

# Therefore to simplify the JSON conversion, via regexes the spaces were removed
# so that both Description and Tag remained on a single line:

"""
Package: 0ad
Version: 0.0.26-3
Installed-Size: 28591
Maintainer: Debian Games Team <pkg-games-devel@lists.alioth.debian.org>
Architecture: amd64
Depends: 0ad-data (>= 0.0.26), 0ad-data (<= 0.0.26-3), 0ad-data-common (>= 0.0.26), 0ad-data-common (<= 0.0.26-3), libboost-filesystem1.74.0 (>= 1.74.0), libc6 (>= 2.34), libcurl3-gnutls (>= 7.32.0), libenet7, libfmt9 (>= 9.1.0+ds1), libfreetype6 (>= 2.2.1), libgcc-s1 (>= 3.4), libgloox18 (>= 1.0.24), libicu72 (>= 72.1~rc-1~), libminiupnpc17 (>= 1.9.20140610), libopenal1 (>= 1.14), libpng16-16 (>= 1.6.2-1), libsdl2-2.0-0 (>= 2.0.12), libsodium23 (>= 1.0.14), libstdc++6 (>= 12), libvorbisfile3 (>= 1.1.2), libwxbase3.2-1 (>= 3.2.1+dfsg), libwxgtk-gl3.2-1 (>= 3.2.1+dfsg), libwxgtk3.2-1 (>= 3.2.1+dfsg-2), libx11-6, libxml2 (>= 2.9.0), zlib1g (>= 1:1.2.0)
Pre-Depends: dpkg (>= 1.15.6~)
Size: 7891488
SHA256: 3a2118df47bf3f04285649f0455c2fc6fe2dc7f0b237073038aa00af41f0d5f2
SHA1: 9ea2aed7feb4ec340ff1d2a61e335a825cad1eca
MD5sum: 4d471183a39a3a11d00cd35bf9f6803d
Description: Real-time strategy game of ancient warfare 0 A.D. (pronounced "zero ey-dee") is a free, open-source, cross-platform real-time strategy (RTS) game of ancient warfare. In short, it is a historically-based war/economy game that allows players to relive or rewrite the history of Western civilizations, focusing on the years between 500 B.C. and 500 A.D. The project is highly ambitious, involving state-of-the-art 3D graphics, detailed artwork, sound, and a flexible and powerful custom-built game engine.
Homepage: https://play0ad.com/
Tag: game::strategy, interface::graphical, interface::x11, role::program, uitoolkit::sdl, uitoolkit::wxwidgets, use::gameplaying, x11::application
Section: games
Priority: optional
Filename: pool/main/0/0ad/0ad_0.0.26-3_amd64.deb
"""

# Usage example: 
# python3 format_packages.py lory/main/binary-amd64/ lory/main/binary-amd64/

import os
import re
import argparse
from tqdm import tqdm
import logging

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
    logging.info(f"Processing file: {input_file_path}")
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
    # Iterate over all files in the input directory and its subdirectories
    for root, _, files in os.walk(input_dir):
        for filename in files:
            if filename.startswith("Packages"):
                input_file_path = os.path.join(root, filename)
                # Output directory structure should mirror the input directory structure
                relative_path = os.path.relpath(input_file_path, input_dir)
                output_file_path = os.path.join(output_dir, relative_path)

                # Log to check which file is being processed
                logging.info(f"Processing file: {input_file_path}")

                # Perform description and tag updates, and save the result to a new file
                update_package_info(input_file_path, output_file_path)

def setup_logging():
        # Get the directory of the script file
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Create the tmp folder in the same directory as the script file
    tmp_dir = os.path.join(script_dir, 'tmp')
    os.makedirs(tmp_dir, exist_ok=True)

    # Create the complete path for the log file inside the tmp folder
    log_file_path = os.path.join(tmp_dir, 'format_packages.log')

    # Use logging lib to check any errors
    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(filename=log_file_path, filemode='w', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    logging.info(f"Logging initialized. Log file: {log_file_path}")
                
def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Format Parrot/Debian Packages files in a specified directory.")
    parser.add_argument("input_directory", help="Specify the input directory containing Packages files.")
    parser.add_argument("output_directory", help="Specify the output directory for processed Packages files.")

    # Parse command-line arguments
    args = parser.parse_args()

    # Perform formatting for all Packages files in the specified directory
    format_all_packages(args.input_directory, args.output_directory)

if __name__ == "__main__":
    setup_logging()
    main()

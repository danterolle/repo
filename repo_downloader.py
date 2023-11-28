# This script is a CLI tool designed to extract the Parrot Packages files.

# The Packages files typically contain details about Debian packages, such as their names, versions,
# maintainer information, architecture, and various other package attributes.

# The primary purpose of this tool is to selectively download Packages files from a specified Parrot
# repository based on user-defined parameters, including codenames, branches, and architectures.
# The downloaded Packages files are then organized into a folder structure that reflects 
# the codename, branch, and architecture.

import os
import requests
import argparse
from tqdm import tqdm
import logging
import tempfile

"""
download_packages: Download Packages files based on user selection.

Args:
    - base_url (str): The base URL of the Debian repository.
    - repo_config (dict): Configuration of valid codenames, branches, and architectures.
    - selected_codenames (list): User-selected codenames.
    - selected_branches (list): User-selected branches.
    - selected_architectures (list): User-selected architectures.
"""
def download_packages(base_url, repo_config, selected_codenames, selected_branches, selected_architectures):

    # Count the total number of iterations for tqdm
    total_iterations = len(selected_codenames) * len(selected_branches) * len(selected_architectures)

    # Use tqdm to display an overall progress bar
    with tqdm(total=total_iterations, desc="Downloading Packages", unit="package") as pbar:
        # Iterate over selected codenames
        for codename in selected_codenames:
            if codename not in repo_config["codenames"]:
                logging.warning(f"Ignoring invalid codename: {codename}")
                continue

            # Iterate over selected branches
            for branch in selected_branches:
                if branch not in repo_config["branches"]:
                    logging.warning(f"Ignoring invalid branch: {branch}")
                    continue

                # Iterate over selected architectures
                for arch in selected_architectures:
                    if arch not in repo_config["architectures"]:
                        logging.warning(f"Ignoring invalid architecture: {arch}")
                        continue

                    # Build the URL for the Packages file
                    url = f"{base_url}{codename}/{branch}/{arch}/Packages"
                    # Define the local path where the Packages file will be saved
                    download_path = f"{codename}/{branch}/{arch}/Packages"

                    # Create the folder structure if it doesn't exist
                    os.makedirs(os.path.dirname(download_path), exist_ok=True)

                    logging.info(f"Downloading {url} to {download_path} folder")

                    # Perform the GET request to download the Packages file
                    response = requests.get(url)
                    if response.status_code == 200:
                        # Save the downloaded content to the local file
                        with open(download_path, "wb") as file:
                            file.write(response.content)
                        logging.info(f"Download successful\n")
                    else:
                        logging.error(f"Failed to download {url}\n")

                    # Update the tqdm progress bar
                    pbar.update(1)

def setup_logging():
        # Get the directory of the script file
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Create the tmp folder in the same directory as the script file
    tmp_dir = os.path.join(script_dir, 'tmp')
    os.makedirs(tmp_dir, exist_ok=True)

    # Create the complete path for the log file inside the tmp folder
    log_file_path = os.path.join(tmp_dir, 'repo_downloader.log')

    # Use logging lib to check any errors
    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(filename=log_file_path, filemode='w', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Download Parrot Packages files from a specified repository.")
    parser.add_argument("--base-url", default="https://deb.parrot.sh/parrot/dists/", help="Specify a custom base URL.")
    parser.add_argument("--codename", nargs="+", help="Specify codenames to download Packages for.")
    parser.add_argument("--branch", nargs="+", help="Specify branches to download Packages for.")
    parser.add_argument("--architecture", nargs="+", help="Specify architectures to download Packages for.")

    # Parse command-line arguments
    args = parser.parse_args()

    # Repository configuration
    repo_config = {
        "codenames": ["lory", "lory-backports", "lory-updates", "lory-security"],
        "branches": ["main", "contrib", "non-free", "non-free-firmware"],
        "architectures": ["binary-amd64", "binary-arm64", "binary-armhf", "binary-i386"]
    }

    # Use selected values or default values from the repository config
    selected_codenames = args.codename or repo_config["codenames"]
    selected_branches = args.branch or repo_config["branches"]
    selected_architectures = args.architecture or repo_config["architectures"]

    # Call the function to download Packages files
    download_packages(args.base_url, repo_config, selected_codenames, selected_branches, selected_architectures)

if __name__ == "__main__":
    setup_logging()
    main()

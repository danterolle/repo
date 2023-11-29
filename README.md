# REPO (Repository Extraction and Parsing Operations)

This repository is a reimplementation written in Python 3 of [the following project for ParrotOS](https://github.com/danterolle/packages-filter).

It is all been redesigned and written again to cope with the new structural change in the ParrotOS repositories, particularly because of the Debian 12-based version 6.0.

It works better, it is better managed, and will be further improved.

So, these scripts allow you to download the Packages file from any Debian repository (including ParrotOS), format it as needed to get a JSON format easily usable in the web.

## Getting started

In this project, each script has a specific task. A dedicated Makefile will probably be created in the future or everything will be rearranged with a better project structure.

Each script should be executed in exactly the order in which they are shown in this README.

In addition, each time these scripts are used, a log file is created in a temporary folder called `tmp` that will contain their execution status 

### `repo_downloader.py`
 
This script is designed to download "Packages" files from a specific Debian repository, using information specified by the user through command-line arguments.

<details>
  <summary>Command line arguments</summary>

  `--base-url` allows the user to specify a custom base URL for the Debian repository. The default URL is **https://deb.parrot.sh/parrot/dists/**

  `--codename` allows the user to specify one or more Parrot/Debian name codes for which to download "Packages" files. In Parrot, could be **lory**.

  `--branch` allows the user to specify one or more repository branches, for instance: 
    
    main
    contrib
    non-free
    non-free-firmware

  `--architecture` allows the user to specify one or more architectures (it is necessary to keep this format as it is standard for the repository itself):
    
    binary-amd64
    binary-arm64
    binary-armhf
    binary-i386

</details>

#### Usage example

```
$ python3 repo_downloader.py --codename lory --branch main contrib --architecture arm64 i386
```

You can also have a helper printed on terminal by typing:

```
$ python3 repo_downloader.py -h
```

```
usage: repo_downloader.py [-h] [--base-url BASE_URL] [--codename CODENAME [CODENAME ...]]
                          [--branch BRANCH [BRANCH ...]]
                          [--architecture ARCHITECTURE [ARCHITECTURE ...]]

Download Parrot Packages files from a specified repository.

options:
  -h, --help            show this help message and exit
  --base-url BASE_URL   Specify a custom base URL.
  --codename CODENAME [CODENAME ...]
                        Specify codenames to download Packages for.
  --branch BRANCH [BRANCH ...]
                        Specify branches to download Packages for.
  --architecture ARCHITECTURE [ARCHITECTURE ...]
                        Specify architectures to download Packages for.
```

### `format_packages.py`

This script performs formatting operations on Parrot/Debian Packages files. It processes each package block within the input files, updates the description and tag fields, and saves the modified content to new output files.

[What problem does it solve?](https://github.com/danterolle/repo/blob/781619acb1f3cff23c4b4247006e5bd3e339f487/format_packages.py#L5C7-L5C7)

<details>
  <summary>Command line arguments</summary>

  `input_directory` allows the user to select a directory where the correction is to take place. It is recursive.

  `output_directory` allows the user to select the output directory where the processed files will be created.

</details>

#### Usage example

```
$ python3 format_packages.py lory/ lory/
```

You can also have a helper printed on terminal by typing:

```
usage: format_packages.py [-h] input_directory output_directory

Format Parrot/Debian Packages files in a specified directory.

positional arguments:
  input_directory   Specify the input directory containing Packages files.
  output_directory  Specify the output directory for processed Packages files.

options:
  -h, --help        show this help message and exit
```

### `json_parser.py`

This script (recursively) processes a specified root directory, identifies "Packages" files within it, extracts information from these files, and saves the parsed data in JSON format. The resulting JSON files are organized in a specified output directory maintaining the directory structure of the input. 

<details>
  <summary>Command line arguments</summary>

  `input_directory` allows the user to select a directory where the Packages files are located.

  `output_directory` allows the user to select the output directory where the *Packages.json* files will be placed.

</details>

#### Usage example

```
$ python3 json_parser.py --recursive lory/ output/ 
```

You can also have a helper printed on terminal by typing:

```
usage: json_parser.py [-h] [--recursive] input_directory output_directory

Parse multiple Packages files and save JSON outputs.

positional arguments:
  input_directory   Path to the root directory containing Packages files.
  output_directory  Path to the directory for saving JSON outputs.

options:
  -h, --help        show this help message and exit
  --recursive       Recursively process subdirectories.
```

### `server.py`

This script implements a FastAPI server that provides an API endpoint for retrieving information about packages from a repository, based on user-provided query parameters.

It's still being evaluated and from a security point of view it could be improved.

#### Usage example

Start the app
```
$ uvicorn server:app --reload
```

Return the complete list of packages for a given branch and architecture
```
$ curl -X GET "http://127.0.0.1:8000/packages/?architecture=amd64&branch=main"
```

Return only the information of a specific package
```
curl -X GET "http://127.0.0.1:8000/packages/?package_name=0ad&architecture=amd64&branch=main"
```

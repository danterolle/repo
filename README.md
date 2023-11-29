# REPO (Repository Extraction and Parsing Operations)

This repository is a reimplementation written in Python 3 of [the following project for ParrotOS](https://github.com/danterolle/packages-filter).

It is all been redesigned and written again to cope with the new structural change in the ParrotOS repositories, particularly because of the Debian 12-based version 6.0.

It works better, it is better managed, and will be further improved.

So, these scripts allow you to download the Packages file from any Debian repository (including ParrotOS), format it as needed to get a JSON format easily usable in the web.

## Getting started

In this project, each script has a specific task. A dedicated Makefile will probably be created in the future or everything will be rearranged with a better project structure.

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

### `format_packages.py`

### `json_parser.py`

### `server.py`
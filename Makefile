VENV_NAME = venv
PYTHON = python3

.PHONY: create-venv activate-venv init run clean

create-venv:
	$(PYTHON) -m venv $(VENV_NAME)

activate-venv:
	source $(VENV_NAME)/bin/activate

init:
	pip install -r requirements.txt

run:
	$(PYTHON) repo_downloader.py --codename lory
	$(PYTHON) format_packages.py lory/ lory/
	$(PYTHON) json_parser.py --recursive lory/ output/

clean:
	rm -rf __pycache__/
	rm -rf tmp/
	rm -rf $(VENV_NAME)/
	rm -rf lory/
	rm -rf output/

VENV_NAME = venv

create-venv:
	python3 -m venv $(VENV_NAME)

activate-venv:
	source $(VENV_NAME)/bin/activate

init:
	pip install -r requirements.txt

clean:
	rm -rf __pycache__/
	rm -rf tmp/
	rm -rf $(VENV_NAME)/

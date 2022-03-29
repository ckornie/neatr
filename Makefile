PYTHON=python

all: build

venv:
		$(PYTHON) -m venv .venv

activate:
		source .venv/bin/activate.fish

dependencies:
		$(PYTHON) -m pip install pdfrw

build:
		pex . -v --python=python3.9 -r requirements.txt -o neatr.pex -m neatr

clean:
		find neatr -type f \( -name "__pycache__" -o -name "*.pyc" -o -name "*.pyo" \) -delete
		find neatr \( -type d -a -name  "__pycache__" \) -delete
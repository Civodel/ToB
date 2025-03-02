VENV=venv
PYTHON=$(VENV)/bin/python

ifeq ($(OS),Windows_NT)
    ACTIVATE=$(VENV)\Scripts\activate
    CLEAN_CMD=rmdir /s /q __pycache__ && del /f /q *.pyc *.pyo
else
    ACTIVATE=source $(VENV)/bin/activate
    CLEAN_CMD=rm -rf __pycache__ *.pyc *.pyo *~
endif

make:

	$(info)  #list of possible commands



install:
	python -m venv $(VENV)
	$(ACTIVATE) && pip install --upgrade pip
	$(ACTIVATE) && pip install -r requirements.txt

test:


run:
	uvicorn src.main:app --reload


down:

clean:
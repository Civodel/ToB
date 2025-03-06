VENV=venv
PYTHON=$(VENV)/bin/python
DOCKER_COMPOSE = docker-compose
SERVICE_NAME = eva01

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
	python -m venv $(VENV)
	python -m pytest -v

run:
	$(DOCKER_COMPOSE) up -d


down:
	$(DOCKER_COMPOSE) down

clean:
	$(DOCKER_COMPOSE) down --volumes --remove-orphans

build:
	$(DOCKER_COMPOSE) build

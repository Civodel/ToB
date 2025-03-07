# Makefile Mejorado

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

# Tarea principal: mostrar las tareas disponibles
help:
	@echo "Tareas disponibles:"
	@echo "  make install   - Instalar dependencias"
	@echo "  make reinstall - Instala dependencias en el entorno virtual"
	@echo "  make run       - Ejecutar el proyecto"
	@echo "  make test      - Ejecutar pruebas"
	@echo "  make clean     - Limpiar los archivos temporales"
	@echo "  make down      - Detener los contenedores de Docker"
	@echo "  make build     - Construir los contenedores de Docker"

# Instalar dependencias en un entorno virtual
install:
	@echo "Creando el entorno virtual..."
	python -m venv $(VENV)
	$(ACTIVATE) && pip install --upgrade pip
	$(ACTIVATE) && pip install -r requirements.txt

reinstall:
	@echo "Reinstalando dependencias..."

	pip install --upgrade pip
	pip install -r requirements.txt



# Ejecutar pruebas con pytest
test: $(VENV)/bin/activate
	@echo "Ejecutando pruebas..."
	python -m pytest -v

# Ejecutar el proyecto con Docker Compose
run: $(VENV)/bin/activate
	@echo "Ejecutando el proyecto con Docker..."
	$(DOCKER_COMPOSE) up -d

# Detener los contenedores de Docker
down:
	@echo "Deteniendo contenedores..."
	$(DOCKER_COMPOSE) down

# Limpiar los archivos temporales y volúmenes de Docker
clean:
	@echo "Limpiando archivos temporales..."
	$(DOCKER_COMPOSE) down --volumes --remove-orphans
	$(CLEAN_CMD)

# Construir los contenedores de Docker
build:
	@echo "Construyendo los contenedores Docker..."
	$(DOCKER_COMPOSE) build

# Regla para verificar si el entorno virtual ya está creado
$(VENV)/bin/activate:
	@echo "Entorno virtual no encontrado. Ejecutando 'make install' para crear el entorno..."

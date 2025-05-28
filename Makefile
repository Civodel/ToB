# Makefile Mejorado

VENV=venv
PYTHON=$(VENV)/bin/python
DOCKER_COMPOSE = docker-compose
SERVICE_NAME = eva01
UV_FLAGS=--native-tls

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
	@echo "  make install-uv  - Instalar uv (gestor de paquetes rápido)"
	@echo "  make install     - Instalar dependencias con uv"
	@echo "  make reinstall   - Reinstalar dependencias con uv"
	@echo "  make add-pkg     - Añadir un paquete con uv (make add-pkg PKG=nombre_paquete)"
	@echo "  make update-pkg  - Actualizar un paquete con uv (make update-pkg PKG=nombre_paquete)"
	@echo "  make run         - Ejecutar el proyecto"
	@echo "  make test        - Ejecutar pruebas"
	@echo "  make clean       - Limpiar los archivos temporales"
	@echo "  make down        - Detener los contenedores de Docker"
	@echo "  make build       - Construir los contenedores de Docker"
	@echo "  make freeze      - Guardar dependencias actuales en requirements.txt"

# Instalar uv (reemplazo rápido de pip)
install-uv:
	@echo "Verificando la instalación de uv..."
	which uv > /dev/null 2>&1 || (echo "Instalando uv..." && curl -LsSf https://astral.sh/uv/install.sh | sh)

# Instalar dependencias con uv en un entorno virtual
install: install-uv
	@echo "Creando el entorno virtual con uv..."
	uv $(UV_FLAGS) venv $(VENV)
	@echo "Instalando dependencias básicas primero..."
	$(ACTIVATE) && uv $(UV_FLAGS) pip install setuptools wheel
	@echo "Instalando dependencias por grupos..."
	$(ACTIVATE) && uv $(UV_FLAGS) pip install --upgrade pip
	$(ACTIVATE) && uv $(UV_FLAGS) pip install requests httpx fastapi uvicorn pydantic
	$(ACTIVATE) && uv $(UV_FLAGS) pip install PyMySQL mysql-connector-python
	@echo "Intento instalar mysqlclient..."
	-$(ACTIVATE) && uv $(UV_FLAGS) pip install mysqlclient || echo "No se pudo instalar mysqlclient, continuando..."
	@echo "Instalando paquetes Python solo necesarios..."
	$(ACTIVATE) && uv $(UV_FLAGS) pip install click starlette databases slack-sdk cryptography
	$(ACTIVATE) && uv $(UV_FLAGS) pip install mem0ai
	$(ACTIVATE) && uv $(UV_FLAGS) pip install dotenv idna pytest-asyncio
	@echo "NOTA: Si algunas dependencias fallan, puédelas instalar manualmente con: uv pip install <paquete>"

# Reinstalar dependencias
reinstall: install-uv
	@echo "Reinstalando dependencias con uv..."
	$(ACTIVATE) && uv $(UV_FLAGS) pip install -r requirements.txt || echo "Algunas dependencias no pudieron instalarse"

# Añadir un nuevo paquete
add-pkg: install-uv
	@if [ "$(PKG)" = "" ]; then \
		echo "Error: Especifica un paquete con PKG=nombre_paquete"; \
	else \
		echo "Añadiendo paquete $(PKG)..." && \
		$(ACTIVATE) && uv $(UV_FLAGS) pip install $(PKG) && \
		make freeze; \
	fi

# Actualizar un paquete
update-pkg: install-uv
	@if [ "$(PKG)" = "" ]; then \
		echo "Error: Especifica un paquete con PKG=nombre_paquete"; \
	else \
		echo "Actualizando paquete $(PKG)..." && \
		$(ACTIVATE) && uv $(UV_FLAGS) pip install --upgrade $(PKG) && \
		make freeze; \
	fi

# Guardar dependencias en requirements.txt
freeze: install-uv
	@echo "Guardando dependencias en requirements.txt..."
	$(ACTIVATE) && uv $(UV_FLAGS) pip freeze > requirements.txt



# Ejecutar pruebas con pytest
test: $(VENV)/bin/activate
	@echo "Ejecutando pruebas..."
	$(ACTIVATE) && python -m pytest -v

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
	make install

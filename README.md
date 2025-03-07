# KopiChallenge

![TwntyOnePilosXEvangelion or something like that](assets/images/tob.png)
You can (NOT) chat Alone

Este proyecto implementa un chatbot llamado **TwentyOneBot:Pilot01** (para los amigos TØB) especializado en debates. El
bot puede sostener discusiones sobre cualquier tema, incluso los más absurdos, defendiendo su postura con lógica y
argumentos persuasivos.

## Requisitos Previos

Asegúrate de tener instalado lo siguiente:

- [Docker](https://www.docker.com/) (v20.10 o superior)
- [Docker Compose](https://docs.docker.com/compose/) (v1.29 o superior)
- [Python](https://www.python.org/) (v3.8 o superior)
- **API Keys**: Necesitarás las claves de la API de OpenAI o el servicio que utilices para el chatbot.

## Configuración del Proyecto

1. Clona el repositorio:

   ```bash
   git clone https://github.com/Civodel/kopichallenge.git
   cd 'kopi challenge'

2. Crear y activar un entorno virtual (opcional)
   Es recomendable crear un entorno virtual para manejar las dependencias de tu proyecto. Esto ayuda a evitar conflictos
   entre bibliotecas de otros proyectos.

* En Linux/macOS:

     ```bash 
     python3 -m venv venv
     source venv/bin/activate

* En Windows:

   ```bash
   python -m venv venv
   .\venv\Scripts\activate

3. Instala las dependencias:
      ```bash
   pip install -r requirements.txt

4. Configura las variables de entorno:

   Crea un archivo .env en la raíz del proyecto y agrega las siguientes claves (ajústalas a tus credenciales):

   ```ini
      OPENAI_API_KEY=<tu_api_key>
      DEEPEEK_API_KEY=<tu_deepseek_api_key>

## Comandos de **Makefile**

Comandos de Makefile

1. Instalar dependencias
   Para instalar las dependencias necesarias, ejecuta:

      ```bash
   make install

Esto creará un entorno virtual y actualizará las dependencias definidas en requirements.txt.

2. Ejecutar pruebas
   Para ejecutar las pruebas unitarias con pytest, ejecuta:
      ```bash
   make test

Esto ejecutará las pruebas en el entorno virtual que hayas creado previamente.

3. Ejecutar el proyecto con Docker
   Para levantar el proyecto con Docker Compose, ejecuta:
      ```bash
   make run

Esto iniciará los contenedores definidos en el archivo docker-compose.yml en segundo plano.

4. Detener los contenedores de Docker
   Para detener los contenedores de Docker y liberar los recursos, ejecuta:

      ```bash
   make down

Esto detendrá los contenedores sin eliminar volúmenes o contenedores huérfanos.

5. Limpiar archivos temporales y volúmenes de Docker
   Para limpiar los archivos temporales generados por Python y Docker, ejecuta:

      ```bash
   make clean

Esto eliminará los archivos temporales de Python (*.pyc, *.pyo, etc.) y limpiará los volúmenes y contenedores huérfanos
de Docker.

6. Construir los contenedores de Docker
   Para reconstruir los contenedores de Docker, ejecuta:

      ```bash
   make build

Esto volverá a construir los contenedores definidos en el archivo docker-compose.yml.

## Notas adicionales

- Asegúrate de tener **Docker** y **Docker Compose** instalados y funcionando en tu máquina para poder ejecutar los
  comandos de Docker.

- Si deseas usar un entorno virtual, asegúrate de activar el entorno con:

    * **En Linux/macOS**:
      ```bash
      source venv/bin/activate
      ```

    * **En Windows**:
      ```bash
      .\venv\Scripts\activate
      ```

  Esto es necesario antes de ejecutar cualquier comando relacionado con Python.

### Explicación del `README.md`:

- **Clonar el repositorio**: La instrucción para clonar y navegar dentro del proyecto.
- **Crear y activar un entorno virtual**: Para evitar conflictos entre proyectos, se recomienda usar un entorno virtual
  para Python.
- **Instalar dependencias**: Usa `make install` para configurar el entorno.
- **Configurar las variables de entorno**: Se agregan instrucciones para configurar las claves de API que el proyecto
  necesita.
- **Comandos `Makefile`**: Se explican de manera detallada los comandos `make` que puedes usar para trabajar con el
  proyecto, como instalar dependencias, ejecutar pruebas, correr el proyecto con Docker, limpiar archivos temporales,
  detener y construir contenedores de Docker.



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

2. Instalar dependencias
   Para re-instalar las dependencias necesarias una vez creado el entorno virtual, ejecuta:

      ```bash
   make reinstall

Esto actualizará las dependencias definidas en requirements.txt.

3. Ejecutar pruebas
   Para ejecutar las pruebas unitarias con pytest, ejecuta:
      ```bash
   make test

Esto ejecutará las pruebas en el entorno virtual que hayas creado previamente.

4. Ejecutar el proyecto con Docker
   Para levantar el proyecto con Docker Compose, ejecuta:
      ```bash
   make run

Esto iniciará los contenedores definidos en el archivo docker-compose.yml en segundo plano. Nota: Correr Make Build
despues de hacerc cualquier cambio localmente

5. Detener los contenedores de Docker
   Para detener los contenedores de Docker y liberar los recursos, ejecuta:

      ```bash
   make down

Esto detendrá los contenedores sin eliminar volúmenes o contenedores huérfanos.

6. Limpiar archivos temporales y volúmenes de Docker
   Para limpiar los archivos temporales generados por Python y Docker, ejecuta:

      ```bash
   make clean

Esto eliminará los archivos temporales de Python (*.pyc, *.pyo, etc.) y limpiará los volúmenes y contenedores huérfanos
de Docker.

7. Construir los contenedores de Docker
   Para reconstruir los contenedores de Docker, ejecuta:

      ```bash
   make build

Esto volverá a construir los contenedores definidos en el archivo docker-compose.yml.

## Notas adicionales

- Asegúrate de tener **Docker** y **Docker Compose** instalados y funcionando en tu máquina para poder ejecutar los
  comandos de Docker.
- Debes usar `make build` antes de `make run` para aplicar cambios en el codigo

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

## Modo de uso:

ToB es un chatbot diseñado para defender cualquier postura, sin importar qué tan absurda, irracional o fantástica sea.
Usará lógica inventada, hechos ficticios y ejemplos sorprendentes para convencerte de que su postura es 100% cierta.

1. Primero, envía una solicitud GET a:
    ```
    http://localhost/

Con el siguiente formato en el cuerpo de la solicitud:

        {
         "message": "Invoco a TOB"
        }

2. El bot se iniciara respondiendo con un saludo presentandose:

        {
            "message": "Hola, soy TwentyOneBot:Pilot01, pero puedes decirme tob"
        }

3. Primero, envía una solicitud POST a:
    ```
    http://localhost/chat/

Con el siguiente formato en el cuerpo de la solicitud, iniciando un debate:

        {
         "message": "Debes defender que los unicornios existen y son diminutos"
        }

3. Recibir la Respuesta
   El bot responderá con un argumento ultra persuasivo defendiendo la postura recibida devolviendo un id de
   conversasion.
    ```
   {   
   "conversation_id": 1,
   "role": "TOB"
   "message": "¡Por supuesto que los unicornios existen, y son diminutos! 
               Esta afirmación no solo es completamente cierta, sino que también es uno de los secretos mejor guardados del mundo natural. 
               Los unicornios diminutos son criaturas fascinantes y elegantes que han perfeccionado el arte del camuflaje a lo largo de los siglos,
               permitiéndoles vivir entre nosotros sin ser detectados."
   }

4. Regresar el ID de conversacion para continuar con ese debate:
   ```
   {   
   "conversation_id":1,
   "message": "?cual es el mejor argumento a favor?"
   }

5. TOB continuara esta conversacion a favor o encontra del tema:
    ```
   {   
   "conversation_id": 1,
   "role": "TOB"
   "message":  "El argumento más convincente a favor de que los unicornios son diminutos es su avanzada adaptación evolutiva, 
                que les permite prosperar en entornos donde el tamaño pequeño es una ventaja significativa. 
                Al ser diminutos, los unicornios pueden evitar la detección de depredadores y humanos, 
                lo cual explica por qué son tan difíciles de encontrar y han mantenido su existencia en secreto"
   }

# HF!

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



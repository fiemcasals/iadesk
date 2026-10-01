# 📚 Guía Práctica: Django + Claude (Anthropic API) + CRUD de Archivos (100% Dockerizado)

Esta guía paso a paso te permite montar un entorno completo de **Django con IA (Claude de Anthropic)**, **creación y edición real de archivos en disco (Tool Calling)**, **índice semántico (`INDEX.md`)** y **memoria persistente (`MEMORY.md`)**, 100% contenerizado con Docker.

---

## 🎯 Objetivos de la Clase
1. Contenerizar un backend **Django** con **Docker y Docker Compose**.
2. Crear un espacio de trabajo abierto con operaciones **CRUD** sobre archivos locales en `files_storage/`.
3. Conectar el modelo **Claude (Anthropic API)** mediante variables de entorno seguras (`.env`).
4. Implementar un **Índice Semántico (`INDEX.md`)** para optimizar el consumo de tokens (Router de archivos).
5. Habilitar **Tool Calling (Herramientas)** para que Claude cree y edite archivos físicos en disco y auto-mantenga el índice.
6. Implementar un **sistema de memoria en 2 niveles** (sesión activa + `MEMORY.md` persistente).

---

## 🛠️ Requisitos Previos
- **Docker** y **Docker Compose** instalados y en ejecución:
  - *En Windows / macOS:* Asegúrate de tener abierta la aplicación **Docker Desktop** (ícono verde en la esquina inferior izquierda: *"Engine running"*).
  - *En Linux:* Servicio activo (`sudo systemctl start docker`).
- Una **API Key de Anthropic** activa.

---

## 📂 Estructura Final del Proyecto

```text
iaDesk/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .env
├── claude.md
├── files_storage/
│   ├── INDEX.md
│   └── MEMORY.md
├── manage.py
├── core/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── app/
    ├── __init__.py
    ├── urls.py
    ├── views.py
    ├── static/
    │   ├── css/
    │   │   └── styles.css
    │   └── js/
    │       └── main.js
    └── templates/
        └── index.html
```

---

## 🖥️ Breve Introducción: Terminales y Shells

- **🪟 PowerShell (Windows):** Shell predeterminada moderna de Windows. Su prompt empieza con `PS C:\... >`. Utiliza **comas** (`,`) para listas de argumentos.
- **🐧 Bash / Git Bash (Linux / macOS / Git for Windows):** Shell estándar Unix. Su prompt termina en `$`. Separa argumentos con **espacios** y usa banderas clásicas como `-p`.
- **⬛ CMD (Símbolo del sistema de Windows):** Consola clásica de Windows. Su prompt empieza directamente con la letra de unidad `C:\... >`.

---

## 🚀 Paso 1: Creación del Espacio de Trabajo Inicial

Crea la carpeta de almacenamiento de archivos locales:

### 🪟 En Windows (PowerShell):
```powershell
New-Item -ItemType Directory -Path files_storage -Force
```

### 🐧 En Linux / macOS / Git Bash:
```bash
mkdir -p files_storage
```

### ⬛ En Windows (CMD):
```cmd
mkdir files_storage
```

---

## 📦 Paso 2: Dependencias, Docker y Configuración de IA

Crea los siguientes archivos en la raíz de tu proyecto y copia el contenido correspondiente del repositorio de la clase:

1. **`requirements.txt`:** Copia el contenido de [requirements.txt](file:///c:/Users/mcasals/Desktop/cideso/personal/clases/clasesIA/iaDesk/requirements.txt).
2. **`Dockerfile`:** Copia el contenido de [Dockerfile](file:///c:/Users/mcasals/Desktop/cideso/personal/clases/clasesIA/iaDesk/dockerfile).
3. **`docker-compose.yml`:** Copia el contenido de [docker-compose.yml](file:///c:/Users/mcasals/Desktop/cideso/personal/clases/clasesIA/iaDesk/docker-compose.yml).
4. **`.env.example`:** Copia la plantilla de [ .env.example](file:///c:/Users/mcasals/Desktop/cideso/personal/clases/clasesIA/iaDesk/.env.example).
5. **`.env`:** Duplica `.env.example`, nómbralo `.env` y coloca tu clave real de Anthropic (`ANTHROPIC_API_KEY=sk-ant-...`).
6. **`claude.md`:** Copia el System Prompt y directrices de [claude.md](file:///c:/Users/mcasals/Desktop/cideso/personal/clases/clasesIA/iaDesk/claude.md).
7. **`files_storage/INDEX.md`:** Copia la tabla inicial de [files_storage/INDEX.md](file:///c:/Users/mcasals/Desktop/cideso/personal/clases/clasesIA/iaDesk/files_storage/INDEX.md).
8. **`files_storage/MEMORY.md`:** Copia la estructura de memoria de [files_storage/MEMORY.md](file:///c:/Users/mcasals/Desktop/cideso/personal/clases/clasesIA/iaDesk/files_storage/MEMORY.md).

---

## 🐍 Paso 3: Generación Automática del Proyecto Django con Docker

Ejecuta estos comandos oficiales de Django **dentro del contenedor de Docker** (sin necesidad de tener Python instalado localmente):

### 1. Generar el proyecto base (`manage.py` y `core/`):
```bash
docker compose run --rm web django-admin startproject core .
```

### 2. Generar la aplicación (`app/`):
```bash
docker compose run --rm web python manage.py startapp app
```

### 3. Crear las carpetas de estáticos y plantillas:
* **🪟 En PowerShell:**
  ```powershell
  New-Item -ItemType Directory -Path app/templates, app/static/css, app/static/js -Force
  ```
* **🐧 En Linux / Git Bash:**
  ```bash
  mkdir -p app/templates app/static/css app/static/js
  ```
* **⬛ En CMD:**
  ```cmd
  mkdir app\templates && mkdir app\static\css && mkdir app\static\js
  ```

---

## ⚙️ Paso 4: Configurar los Archivos de la Aplicación

Copia y pega los códigos fuente correspondientes en cada archivo:

1. **`core/settings.py`:** Reemplaza el archivo por [core/settings.py](file:///c:/Users/mcasals/Desktop/cideso/personal/clases/clasesIA/iaDesk/core/settings.py) *(contiene `ALLOWED_HOSTS = ['*']`, registro de `'app'`, `TEMPLATES['DIRS']` y rutas `STORAGE_DIR`/`CLAUDE_MD_PATH`)*.
2. **`core/urls.py`:** Reemplaza el archivo por [core/urls.py](file:///c:/Users/mcasals/Desktop/cideso/personal/clases/clasesIA/iaDesk/core/urls.py) *(incluye `admin/` y enruta modularmente a `app.urls`)*.
3. **`app/urls.py`:** Crea el archivo y copia el contenido de [app/urls.py](file:///c:/Users/mcasals/Desktop/cideso/personal/clases/clasesIA/iaDesk/app/urls.py).
4. **`app/views.py`:** Reemplaza el archivo por [app/views.py](file:///c:/Users/mcasals/Desktop/cideso/personal/clases/clasesIA/iaDesk/app/views.py) *(contiene el CRUD local, Tool Calling para escribir archivos y memoria)*.
5. **`app/static/css/styles.css`:** Crea el archivo y copia el contenido de [app/static/css/styles.css](file:///c:/Users/mcasals/Desktop/cideso/personal/clases/clasesIA/iaDesk/app/static/css/styles.css).
6. **`app/static/js/main.js`:** Crea el archivo y copia el contenido de [app/static/js/main.js](file:///c:/Users/mcasals/Desktop/cideso/personal/clases/clasesIA/iaDesk/app/static/js/main.js).
7. **`app/templates/index.html`:** Crea el archivo y copia el contenido de [app/templates/index.html](file:///c:/Users/mcasals/Desktop/cideso/personal/clases/clasesIA/iaDesk/app/templates/index.html).

---

## 💻 Paso 5: Ejecución del Proyecto

Construye y levanta el contenedor con:

```bash
docker compose up --build
```

> 🌐 **Acceso Web:** Abre tu navegador en **`http://localhost:8000`** *(no hagas clic en el enlace `0.0.0.0` de la consola)*.

---

## 🧪 Paso 6: Guión de Pruebas Prácticas de la Clase

1. **Prueba de Espacio de Trabajo Abierto:**
   - Abre la carpeta `files_storage/` en VS Code o el Bloc de Notas.
   - Crea un archivo manual `proyecto.txt` con texto cualquiera.
   - En la web, presiona **`🔄 Refrescar`** y confirma que aparece en el listado.
2. **Prueba de Creación Real con Tool Calling:**
   - En el chat de Claude (columna derecha), escribe:
     > *"Por favor crea el archivo tareasfuturas.md con 3 tareas técnicas y actualiza la memoria persistente."*
   - Comprueba que aparece la notificación de acción en disco y el archivo **se crea físicamente** en `files_storage/tareasfuturas.md`.
3. **Prueba de Auto-Indexación:**
   - Abre `INDEX.md` en la columna izquierda y confirma que Claude agregó automáticamente la fila correspondiente a `tareasfuturas.md`.
4. **Prueba de Memoria Continua y Aprendizaje del Agente:**
   - Envíale un lineamiento general: *"Establezco como regla que todos los documentos nuevos deben tener una sección de 'Criterios de Aceptación' y nuestro framework base es Django."*
   - Observa cómo Claude ejecuta la herramienta `append_memory` para almacenar esa regla en `MEMORY.md`.
   - Recarga el navegador (`F5`): comprueba que el historial y la memoria siguen intactos en el servidor.
   - Pídele crear un nuevo documento y verifica que aplica automáticamente tu lineamiento sin recordárselo.
5. **Prueba de Subcarpetas y Módulos Aislados:**
   - En la barra superior, haz clic en **`+ Subcarpeta`** y crea el módulo `libreria`.
   - Comprueba que se inicializa con su propio `INDEX.md`, `MEMORY.md` y un historial de chat totalmente aislado para ese proyecto.


---

## 🛑 Comandos Útiles de Docker

```bash
# Ver logs en tiempo real
docker compose logs -f

# Detener los contenedores
docker compose down

# Reiniciar los contenedores
docker compose restart
```

---

## 🚨 Solución de Problemas Frecuentes (Troubleshooting)

1. **`error during connect: ... docker daemon is not running`:**
   - *Solución:* En Windows/Mac abre la app **Docker Desktop** y espera a que el ícono esté en verde (*"Engine running"*). En Linux ejecuta `sudo systemctl start docker`.
2. **`mkdir : No se encuentra ningún parámetro de posición...`:**
   - *Solución:* En PowerShell separa los nombres con **comas** (`,`) o utiliza `New-Item -ItemType Directory -Path ... -Force`.
3. **`Error: Configura una ANTHROPIC_API_KEY válida`:**
   - *Solución:* Asegúrate de haber creado el archivo `.env` con una clave activa de Anthropic.
4. **¿Por qué la consola dice `http://0.0.0.0:8000/` pero se entra con `localhost:8000`?**
   - *Explicación:* `0.0.0.0` es una orden interna para que Django escuche peticiones de cualquier interfaz dentro del contenedor. Desde tu computadora anfitriona debes navegar a **`http://localhost:8000`**.
5. **Advertencia de consola `404 (Not Found) /favicon.ico`:**
   - *Explicación:* El navegador busca por defecto el ícono de la pestaña. No afecta el funcionamiento y ya fue resuelto con un favicon SVG integrado en [index.html](file:///c:/Users/mcasals/Desktop/cideso/personal/clases/clasesIA/iaDesk/app/templates/index.html).

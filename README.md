# Servicio REST API de Text-to-Speech (TTS) Local

Este proyecto expone un **API REST de síntesis de voz (Text-to-Speech o TTS)** local y privado. Utiliza **FastAPI** como framework web y **Piper** como motor de síntesis de voz rápido, eficiente y optimizado para ejecutarse localmente en arquitecturas de CPU.

El objetivo principal es recibir un texto y transformarlo en un archivo de audio en formato **PCM 16-bit mono a 16000 Hz (WAV)** garantizando la máxima privacidad, ya que todo el procesamiento se realiza *on-premise* sin depender de servicios externos o de la nube.

---

## 🎯 Objetivos del Proyecto

* **API REST Sencilla**: Un único endpoint optimizado para la síntesis de texto.
* **Privacidad por Diseño**: Procesamiento 100% en local sin transmisión de datos al exterior.
* **Alto Rendimiento**: Uso de **Piper TTS**, capaz de generar audio en tiempo real o superior incluso en hardware modesto (CPU).
* **Calidad Estándar**: Salida de audio formateada en PCM de 16 bits, canal único (mono) y tasa de muestreo de 16000 Hz, óptima para sistemas de telefonía, asistentes virtuales y archivado ligero.
* **Contenerización Completa**: Despliegue sencillo y reproducible mediante **Docker**.

---

## 🛠️ Tecnologías Utilizadas

* **Lenguaje**: Python 3.11+
* **Framework Web**: [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/) (servidor ASGI rápido y robusto).
* **Motor de Síntesis**: [Piper TTS](https://github.com/rhasspy/piper) (síntesis de voz neuronal local extremadamente veloz).
* **Procesamiento de Audio**: `wave` / `soundfile` o librerías nativas de Python para asegurar la salida de audio PCM 16-bit 16000 Hz.
* **Infraestructura**: [Docker](https://www.docker.com/) con compilación multi-etapa (multi-stage) para reducir el tamaño de la imagen final.

---

## 📁 Estructura Propuesta de Carpetas

El proyecto sigue una estructura limpia, modular y fácil de escalar:

```
tts-capability/
├── .gitignore
├── CHANGELOG.md             # Registro de todos los cambios del proyecto
├── CONTRIBUTING.md          # Guía de contribución y flujo Git (TBD)
├── LICENSE                  # Licencia del proyecto (MIT)
├── README.md                # Documentación principal (este archivo)
├── Dockerfile               # Configuración del contenedor Docker para producción
├── requirements.txt         # Dependencias del proyecto en Python
├── app/                     # Código fuente de la aplicación
│   ├── __init__.py
│   ├── main.py              # Punto de entrada de FastAPI y configuración del servidor
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py     # Definición de rutas y endpoints (POST /synthesize)
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py        # Configuración del sistema y variables de entorno (.env)
│   └── services/
│       ├── __init__.py
│       └── tts_engine.py    # Envoltura (wrapper) de Piper TTS y conversión de audio
├── models/                  # Directorio local para almacenar modelos (.onnx y .json) de Piper
└── tests/                   # Suite de pruebas automatizadas
    ├── __init__.py
    └── test_endpoints.py    # Pruebas integrales de los endpoints del API
```

---

## 🔌 Especificación de la API (REST API)

La aplicación expone los siguientes endpoints:

### `POST /v1/synthesize`

Sintetiza el texto enviado en el cuerpo de la petición y devuelve un flujo binario con el archivo de audio resultante.

* **Cuerpo de la Petición (Request Body)**:
  * Content-Type: `application/json`
  * Parámetro `msg` (string): Mensaje de texto a transformar en voz.
  
  ```json
  {
    "msg": "Hola mundo, este es un mensaje de prueba para el servicio de síntesis de voz."
  }
  ```

* **Respuesta de Éxito (Success Response)**:
  * Código HTTP: `200 OK`
  * Content-Type: `audio/wav`
  * Formato del Audio: **PCM 16-bit mono 16000 Hz** (empaquetado en contenedor WAV estándar).

* **Respuesta de Error**:
  * Código HTTP: `400 Bad Request` (si el parámetro `msg` está vacío o consiste únicamente en espacios en blanco).
  * Código HTTP: `422 Unprocessable Entity` (si el formato del JSON es incorrecto o falta el parámetro `msg`).
  * Código HTTP: `500 Internal Server Error` (si ocurre un fallo interno en el motor de síntesis).

---

### `GET /health`

Retorna el estado de salud del servicio para verificar que esté levantado y respondiendo peticiones.

* **Respuesta de Éxito (Success Response)**:
  * Código HTTP: `200 OK`
  * Content-Type: `application/json`
  * Cuerpo de la respuesta:
    ```json
    {
      "status": "ok"
    }
    ```

---

## 🚀 Guía de Despliegue y Uso

### Ejecución Local en Desarrollo

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/danuser2018/tts-capability.git
   cd tts-capability
   ```

2. **Crear y activar un entorno virtual**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Descargar un modelo de voz de Piper** (por ejemplo, en español neutro o de España):
   * Descargar el archivo `.onnx` y su `.json` asociado desde el catálogo de voces de Piper.
   * Colocar los archivos en la carpeta `./models/`.

5. **Iniciar el servidor en modo desarrollo**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

### Despliegue con Docker

1. **Construir la imagen de Docker**:
   ```bash
   docker build -t tts-capability:latest .
   ```

2. **Iniciar el contenedor**:
   ```bash
   docker run -d -p 8000:8000 --name tts-service tts-capability:latest
   ```

---

## 🧪 Ejemplo de Consumo (Client Request)

Puedes probar el servicio ejecutando el siguiente comando `curl` en tu terminal:

```bash
curl -X POST http://localhost:8000/v1/synthesize \
  -H "Content-Type: application/json" \
  -d '{"msg": "Hola mundo"}' \
  --output saludo.wav
```

Este comando guardará el audio sintetizado directamente en el archivo `saludo.wav`. Puedes validar sus propiedades con cualquier reproductor de audio o herramienta de línea de comandos como `file` o `ffprobe`:

```bash
file saludo.wav
# Salida esperada: RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 16000 Hz
```

---

## 🛡️ Buenas Prácticas de Contribución

Si deseas contribuir a este proyecto, por favor sigue estrictamente las directrices indicadas en [CONTRIBUTING.md](file:///home/danuser2018/workspace/tts-capability/CONTRIBUTING.md):
1. **Trunk Based Development**: Crea ramas de corta duración tipo `feature/` o `fix/` desde `main`.
2. **Conventional Commits**: Escribe mensajes de commit claros y estructurados (p. ej., `feat(tts): implementar wrapper de piper`).
3. **No Secretos**: Asegúrate de no incluir claves ni archivos `.env` en tus commits (utiliza variables de entorno y documenta en `.env.example`).
4. **Mantenimiento del CHANGELOG.md**: Actualiza siempre la sección `[Sin publicar]` detallando tus aportes antes de abrir una Pull Request.

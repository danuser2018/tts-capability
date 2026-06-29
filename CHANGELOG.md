# Registro de cambios

Todos los cambios notables de este proyecto se documentan en este fichero.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y este proyecto adhiere a [Versionado Semántico](https://semver.org/lang/es/).

## Guía de uso

Cada versión se documenta bajo su número de versión y fecha de publicación.
Los cambios se agrupan en las siguientes categorías:

- **Añadido** — nuevas funcionalidades.
- **Cambiado** — cambios en funcionalidades existentes.
- **Obsoleto** — funcionalidades que serán eliminadas en versiones futuras.
- **Eliminado** — funcionalidades eliminadas en esta versión.
- **Corregido** — corrección de errores.
- **Seguridad** — correcciones de vulnerabilidades.

---

## [1.3.0] - 2026-06-29

### Corregido

- Implementado el formato de payload de error unificado de `ADR-004` para todas las respuestas HTTP `4xx` y `5xx` en el API.
- Corregida la documentación en `README.md` para referenciar el endpoint versionado `/v1/synthesize` y documentar el endpoint de salud `/health`.
- Traducidos al inglés los comentarios en `app/core/config.py` y los mensajes de consola/aserción en `test_synthesis.py` para adherir a la invariante lingüística del ecosistema.
- Corregida la tabla de herramientas sugeridas en `CONTRIBUTING.md` para adaptarla a un microservicio de Python (`pytest`, `unittest`).
- Removida la versión de Python 3.10 de la matriz en `.github/workflows/tests.yml` para alinearla con el requerimiento de Python 3.11+.

## [1.2.0] - 2026-06-28

### Cambiado

- Versionado del endpoint `/synthesize` a `/v1/synthesize` para alinearse con el estándar ADR-004.

### Añadido

- Nueva carpeta `.agents/skills` con información relevante para la IA.

## [1.1.0] - 2026-06-06

### Añadido

- Nuevo endpoint health para chequear si el servicio está levantado o no.

## [1.0.0] - 2026-05-24

### Añadido

- Fichero `CONTRIBUTING.md` con el flujo de trabajo Trunk Based Development,
  convenciones de commits, guía de Pull Requests y buenas prácticas para
  desarrollo asistido con IA.
- Fichero `CHANGELOG.md` con el formato Keep a Changelog v1.1.0 en castellano.
- Fichero `README.md` completo con la descripción del proyecto, objetivos de diseño, arquitectura técnica propuesta, especificación del endpoint de API (`POST /synthesize`) y guía de uso para el servicio de síntesis de voz (TTS).
- Implementación de la API de FastAPI con soporte de ciclo de vida (`lifespan`) para cargar el modelo de Piper al iniciar el servidor.
- Servicio `TTSEngine` para la síntesis de texto a voz y remuestreo lineal dinámico (de 22.05 kHz a 16 kHz) usando `numpy` sin dependencias externas pesadas.
- Configuración multi-etapa en `Dockerfile` para la compilación optimizada y descarga automática de la voz en español (`es_ES-carlfm-x_low`).
- Suite de pruebas integrales en `tests/test_endpoints.py` utilizando `pytest` y `unittest.mock`.
- Archivo `requirements.txt` con la lista de dependencias necesarias para desarrollo y ejecución.
- Ejecución de test integrados en cada pipeline

---

<!-- Plantilla para nuevas versiones:

## [X.Y.Z] - AAAA-MM-DD

### Añadido
-

### Cambiado
-

### Obsoleto
-

### Eliminado
-

### Corregido
-

### Seguridad
-

-->

[Sin publicar]: https://github.com/danuser2018/tts-capability/compare/HEAD...HEAD

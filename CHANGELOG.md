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

## [Sin publicar]

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

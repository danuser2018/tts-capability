# 🧩 Refinamiento de Feature: Configuración de modelo TTS por variable de entorno

- **Origen:** Este documento refina la especificación de feature descrita en [model_selection.md](file:///home/danuser2018/workspace/tts-capability/docs/features/model_selection.md).

---

## 1. Resumen y Contexto de Negocio

### Objetivo Principal
Permitir que el servicio `tts-capability` seleccione dinámicamente el modelo de voz de Piper TTS en el momento de arranque del contenedor mediante las variables de entorno `TTS_MODEL_NAME` y `TTS_MODEL_DIR`. Esto evita la necesidad de modificar el código fuente del servicio o reconstruir la imagen Docker para alterar la voz del asistente.

### Actores
- **Administrador del Sistema / Desarrollador:** Quien despliega el ecosistema Nova-2 y configura la voz a través del entorno de ejecución (ej. mediante `docker-compose.yml` o archivos `.env`).
- **Usuario Final:** Quien escucha la voz sintetizada por el asistente y se beneficia de una voz consistente definida por despliegue.

---

## 2. Análisis de Servicios e Impacto

| Servicio | Tipo de Cambio | Impacto / Descripción |
|---|---|---|
| `tts-capability` | **Modificar** | Se adapta la configuración de arranque (`Settings` y `lifespan`) para procesar las nuevas variables de entorno y validar los archivos antes de inicializar el motor Piper. Se actualiza el `Dockerfile` para definir estas variables en lugar del antiguo `MODEL_PATH`. |
| `home-assistant` | **Modificar** | Se agregan y documentan las nuevas variables `TTS_MODEL_NAME` y `TTS_MODEL_DIR` en el archivo de configuración global `config/assistant.env`. |
| `interaction-manager` | **Ninguno** | El contrato REST del endpoint `/v1/synthesize` se mantiene inalterado; el coordinador no percibe cambios en el modelo interno. |
| `orchestrator` | **Ninguno** | No interactúa directamente con la selección de modelo del servicio TTS. |

---

## 3. Especificación de Comportamiento (Criterios de Aceptación)

### Escenario 1: Arranque exitoso con modelo y configuración válidos
- **Dado** que el servicio `tts-capability` se inicia con `TTS_MODEL_NAME=es_ES-carlfm-x_low` y `TTS_MODEL_DIR=/app/models`
- **Y** los archivos `/app/models/es_ES-carlfm-x_low.onnx` y `/app/models/es_ES-carlfm-x_low.onnx.json` existen en el filesystem
- **Cuando** el servidor FastAPI ejecuta el evento de arranque `lifespan`
- **Entonces** el sistema valida la existencia de ambos archivos correctamente
- **Y** carga el modelo de voz utilizando `tts_engine.load_model`
- **Y** el servicio inicia normalmente respondiendo `200 OK` en el endpoint `/health`

### Escenario 2: Falla en arranque por ausencia del archivo de modelo `.onnx` (Fail-Fast)
- **Dado** que el servicio `tts-capability` se inicia con `TTS_MODEL_NAME=missing-voice` y `TTS_MODEL_DIR=/app/models`
- **Y** el archivo `/app/models/missing-voice.onnx` no existe en el filesystem
- **Cuando** el servidor FastAPI ejecuta el evento de arranque `lifespan`
- **Entonces** el sistema detecta la ausencia del archivo `.onnx`
- **Y** aborta el inicio lanzando una excepción `FileNotFoundError` indicando la ruta del archivo faltante
- **Y** el contenedor de FastAPI detiene su arranque inmediatamente

### Escenario 3: Falla en arranque por ausencia del archivo de configuración del modelo `.onnx.json` (Fail-Fast)
- **Dado** que el servicio `tts-capability` se inicia con `TTS_MODEL_NAME=incomplete-voice` y `TTS_MODEL_DIR=/app/models`
- **Y** el archivo `/app/models/incomplete-voice.onnx` existe pero `/app/models/incomplete-voice.onnx.json` no existe
- **Cuando** el servidor FastAPI ejecuta el evento de arranque `lifespan`
- **Entonces** el sistema detecta la ausencia del archivo de metadatos `.onnx.json`
- **Y** aborta el inicio lanzando una excepción `FileNotFoundError`
- **Y** el contenedor detiene su arranque de forma inmediata

---

## 4. Diseño Técnico y Contratos

> [!NOTE]
> De acuerdo con la regla de **Aislamiento Lingüístico**, todos los identificadores técnicos, nombres de variables, propiedades de clases y código se definen estrictamente en inglés.

### Environment Variables
- `TTS_MODEL_NAME`: Name base of the voice model. Required. Default value: `es_ES-carlfm-x_low`.
- `TTS_MODEL_DIR`: Directory where local ONNX models reside. Optional. Default value: `models`.

### Class Properties in `app/core/config.py`
We will replace the single `MODEL_PATH` setting with the following properties in the `Settings` class:

```python
class Settings:
    TTS_MODEL_NAME: str = os.getenv("TTS_MODEL_NAME", "es_ES-carlfm-x_low")
    TTS_MODEL_DIR: str = os.getenv("TTS_MODEL_DIR", "models")
    PORT: int = int(os.getenv("PORT", "8000"))

    @property
    def model_path(self) -> str:
        """Returns the absolute or relative path to the ONNX model file."""
        return os.path.join(self.TTS_MODEL_DIR, f"{self.TTS_MODEL_NAME}.onnx")

    @property
    def config_path(self) -> str:
        """Returns the absolute or relative path to the JSON config file."""
        return os.path.join(self.TTS_MODEL_DIR, f"{self.TTS_MODEL_NAME}.onnx.json")
```

### Lifespan Event Validation in `app/main.py`
The lifespan context manager is modified to validate both files explicitly prior to invoking the loading logic:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Retrieve file paths from configuration settings
    model_path = settings.model_path
    config_path = settings.config_path

    # Perform fail-fast validation checks
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"ONNX model file not found at: {model_path}")
        
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"ONNX config file not found at: {config_path}")

    # Load validated model into memory
    tts_engine.load_model(model_path)
    yield
```

---

## 5. Casos de Borde y Manejo de Errores

- **`TTS_MODEL_NAME` Vacío o Nulo:** Si `TTS_MODEL_NAME` se configura con una cadena vacía o caracteres de espacio en blanco únicamente, el método de inicialización de `Settings` lanzará un error de tipo `ValueError` al arrancar.
- **Ruta Inexistente en `TTS_MODEL_DIR`:** Si el directorio no existe, `os.path.exists` fallará directamente en el paso de validación del `.onnx`, abortando el arranque con un `FileNotFoundError` claro.
- **Permisos Insuficientes de Lectura:** Si los archivos existen pero el usuario del contenedor no dispone de permisos de lectura, se capturará una excepción `PermissionError` y se abortará el arranque del contenedor de manera segura.

---

## 6. Estrategia de Testing

### Unit Tests (`tests/test_endpoints.py` o similar)
Se añadirán pruebas unitarias simulando las condiciones de arranque utilizando la funcionalidad de `unittest.mock.patch`:

- **`test_lifespan_success_when_files_exist`**: Mockea `os.path.exists` para retornar `True` para ambos archivos. Valida que el lifespan se completa sin excepciones y llama a `tts_engine.load_model`.
- **`test_lifespan_fails_when_onnx_missing`**: Mockea `os.path.exists` de manera que el archivo `.onnx` retorne `False`. Verifica que la llamada al lifespan lanza un `FileNotFoundError` controlado.
- **`test_lifespan_fails_when_json_missing`**: Mockea `os.path.exists` de modo que el `.onnx` retorne `True` pero el `.onnx.json` retorne `False`. Verifica la propagación del `FileNotFoundError`.
- **`test_settings_validation_invalid_model_name`**: Verifica que si `TTS_MODEL_NAME` es configurado como vacío se genera un error `ValueError` al arrancar.

---

## 7. Plan de Implementación

### Tarea 1: Actualización de Configuración (`app/core/config.py`)
- Modificar la clase `Settings` para incluir `TTS_MODEL_NAME` y `TTS_MODEL_DIR` con sus valores predeterminados.
- Añadir las propiedades calculadas `model_path` y `config_path`.
- Implementar validación de inicialización básica contra valores vacíos.

### Tarea 2: Validación en Lifespan y Engine integration (`app/main.py`)
- Importar `os` en `app/main.py`.
- Introducir las comprobaciones `os.path.exists` en el callback de `lifespan`.
- Reemplazar `settings.MODEL_PATH` por `settings.model_path` en la llamada a `tts_engine.load_model`.

### Tarea 3: Modificación de Configuración de Despliegue (`Dockerfile` y `assistant.env`)
- Sustituir la variable `ENV MODEL_PATH` del Dockerfile de `tts-capability` por `ENV TTS_MODEL_NAME=es_ES-carlfm-x_low` y `ENV TTS_MODEL_DIR=/app/models`.
- Documentar las variables equivalentes en `config/assistant.env` dentro de `home-assistant`.

### Tarea 4: Cobertura de Tests Unitarios (`tests/test_endpoints.py`)
- Escribir e integrar los escenarios de prueba unitarios mockeados para validar el flujo completo de fail-fast de arranque.

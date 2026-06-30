# 🧩 Especificación de Feature: Configuración de modelo TTS por variable de entorno

## 🎯 Objetivo

Permitir que el servicio `tts-capability` seleccione dinámicamente el modelo de voz de Piper TTS **en el momento de arranque del contenedor**, mediante variables de entorno, sin necesidad de modificar el código ni reconstruir la imagen Docker.

Esto habilita a Nova a cambiar la voz utilizada simplemente ajustando configuración de despliegue.

---

## 🧠 Principio de diseño

* La selección del modelo es **determinista y de arranque**
* El modelo se carga **una única vez en memoria**
* El modelo no cambia durante la vida del proceso
* El sistema es **stateless respecto a la elección del modelo**, pero stateful respecto a la carga del modelo

---

## ⚙️ Alcance funcional

### ✔️ Incluye

* Selección de modelo de Piper mediante variable de entorno
* Resolución del modelo dentro de un directorio local de modelos
* Uso de un “nombre base de modelo” como identificador único
* Validación de existencia del modelo en el arranque del servicio
* Aplicación de la configuración únicamente en el startup del servicio

### ❌ No incluye

* Cambio de modelo en runtime
* Descarga automática de modelos
* Selección por request o usuario
* Hot reload del motor TTS
* Versionado dinámico de modelos

---

## 🔌 Contrato de configuración

### Variables de entorno

| Variable         | Obligatoria      | Descripción                                  |
| ---------------- | ---------------- | -------------------------------------------- |
| `TTS_MODEL_NAME` | Sí (con default) | Identificador base del modelo de voz         |
| `TTS_MODEL_DIR`  | No               | Directorio donde residen los modelos locales |

---

## 📦 Convención de modelo

El sistema asume que un modelo está compuesto por dos archivos:

* `{MODEL_NAME}.onnx`
* `{MODEL_NAME}.onnx.json`

### Ejemplo

Si:

```
TTS_MODEL_NAME=es_ES-carlfm-x_low
```

Entonces el sistema espera:

```
/models/es_ES-carlfm-x_low.onnx
/models/es_ES-carlfm-x_low.onnx.json
```

---

## 🚀 Ciclo de vida del modelo

1. **Arranque del contenedor**

   * Se leen variables de entorno
   * Se resuelve el modelo esperado

2. **Validación**

   * Se verifica que existen los archivos requeridos
   * Si no existen → el servicio no puede inicializar correctamente

3. **Inicialización del motor TTS**

   * Piper carga el modelo en memoria
   * El modelo queda cacheado durante toda la vida del proceso

4. **Ejecución de requests**

   * Todos los requests usan la misma instancia de modelo cargado
   * No hay variación de comportamiento según request

---

## 🧾 Reglas de comportamiento

* El modelo es una **decisión de despliegue**, no de ejecución
* Un contenedor = un modelo activo
* El cambio de modelo implica **recreación del contenedor**
* La configuración del modelo debe ser **explícita y reproducible**
* Si el modelo no existe → el servicio debe fallar en startup (fail-fast)

---

## 🧪 Casos de validación

### ✔️ Caso correcto

* `TTS_MODEL_NAME` apunta a modelo existente
* Servicio arranca correctamente
* Piper carga el modelo
* Endpoint `/v1/synthesize` funciona

---

### ❌ Caso error: modelo inexistente

* `TTS_MODEL_NAME` no coincide con archivos en `/models`
* El servicio no debe entrar en estado “degradado”
* Debe fallar el arranque del servicio (fail-fast)

---

## 📌 Impacto en arquitectura Nova

Esta feature convierte el TTS en:

* Un **capability configurable por despliegue**
* Un componente desacoplado del runtime de Nova
* Un módulo intercambiable sin cambios de código

---

## 🧭 Decisión clave tomada

> La selección del modelo pertenece al **nivel de infraestructura (deployment time)**, no al nivel de aplicación (runtime).

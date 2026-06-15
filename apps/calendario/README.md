# App: Calendario

## Qué hace la app

`apps.calendario` permite gestionar citas  desde una interfaz web en Django. El usuario puede crear citas, manualmente o dictarlas en lenguaje natural mediante un parser de texto libre que extrae fecha, hora y título de forma automática. También puede editarlas y borrarlas. 
Las citas se organizan por categorías con color y prioridad configurables.

---

## Modelos principales

### `Categoria`
Agrupa las citas por tipo (p. ej. "Cliente", "Interno", "Personal"). Cada categoría tiene un color hexadecimal para identificarla visualmente en el calendario, una prioridad numérica y una política de reprogramación (`rigida` / `flexible` / `cancelar si no hay hueco`) que indica si las citas de ese tipo pueden moverse con facilidad.

### `Cita`
Representa un evento concreto en el tiempo. Almacena título, fecha de inicio y fin, hora de inicio y fin opcional, categoría asociada, repetir, ubicación, anotaciones y prioridad propia. Es el núcleo de la app: todo el parser, las vistas y la API giran en torno a este modelo.

---

## Cómo usar el parser de texto libre

La vista `cita_desde_texto` acepta una frase en español mediante POST y devuelve un formulario pre-rellenado con los campos que ha podido extraer.

### Frases que entiende

| Frase de entrada | Extrae |
|---|---|
| `"Reunión el lunes a las 10"` | título: *Reunión*, día: próximo lunes, hora: 10:00 |
| `"Llamada con cliente el martes a las 15:30"` | título: *Llamada con cliente*, día: próximo martes, hora: 15:30 |
| `"Cita el 12/07 a las 9"` | título: *Cita*, fecha: 12/07 del año en curso, hora: 09:00 |
| `"Revisión el viernes"` | título: *Revisión*, día: próximo viernes, hora: sin rellenar |
| `"Mañana por la tarde"` | "mañana" y "por la tarde" debes especificar hora en formato 24h|
| `"El 2 de agosto"` | formato "día de mes" en texto no está implementado |

### Frases que **no** entiende (aún)

| Frase de entrada | Problema |
|---|---|
| `"En dos semanas"` | expresiones relativas de semanas, no se resuelven excepto que escribas el día específico |
| `"Next Monday at 3pm"` | solo procesa frases en español |
| `"Reunión a mediodía"` | horas coloquiales (`mediodía`, `medianoche`) no reconocidas |

El parser rellena lo que puede y deja el resto del formulario en blanco para que el usuario lo complete o edite a su gusto.

---

## Qué hace
 
Gestiona citas con soporte de entrada por voz. El flujo principal es:
 
**Voz → transcripción → parser IA → formulario prerrellenado → cita guardada**
 
1. El usuario pulsa "🎙️ Hablar" y graba su cita en voz alta
2. El audio se envía al servidor donde `faster-whisper` lo transcribe a texto
3. El texto pasa al parser (`parser_voz.py`) que usa LiteLLM + OpenRouter para extraer los campos de la cita (título, fecha, hora, categoría, anotaciones)
4. Se muestra un formulario prerrellenado que el usuario puede revisar y confirmar
5. La cita se guarda en la base de datos
También incluye:
- Detección de solapamientos entre citas
- Análisis de sobrecarga diaria (`analizador.py`)
- Sugerencia de reprogramación con IA
- Servidor MCP en `/calendario/mcp/` con tres herramientas: `listar_citas`, `detectar_sobrecarga`, `resumen_dia`
---
 
## Cómo arrancar de cero
 
### 1. Dependencias
 
```bash
pip install -r requirements.txt
```
 
Librerías clave: `django`, `litellm`, `faster-whisper`, `requests`
 
### 2. Variables de entorno
 
Crea un archivo `.env` en la raíz del proyecto con:
 
```dotenv
SECRET_KEY=una-clave-secreta-larga-y-aleatoria
DEBUG=True
DB_NAME=kore_db
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=127.0.0.1
DB_PORT=5432
ALLOWED_HOSTS=127.0.0.1
OPENROUTER_API_KEY=tu_api_key_de_openrouter
MCP_SECRET_TOKEN=un-token-largo-y-aleatorio
FACTURAS_MCP_TOKEN=token-de-la-app-facturas
```
 
**Cómo obtener cada variable:**
 
- `SECRET_KEY` — genera una con `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- `OPENROUTER_API_KEY` — crea una cuenta gratuita en [openrouter.ai](https://openrouter.ai) y genera una API key
- `MCP_SECRET_TOKEN` — genera cualquier string aleatorio largo, por ejemplo: `python -c "import secrets; print(secrets.token_hex(32))"`
- `FACTURAS_MCP_TOKEN` — Se crea en facturas
### 3. Base de datos
 
```bash
python manage.py migrate
```
 
### 4. Categorías semilla
 
```bash
python manage.py loaddata apps/calendario/fixtures/categorias.json
```
 
### 5. Arrancar
 
```bash
python manage.py runserver
```
 
Entrar a `http://127.0.0.1:8000/calendario/`
 
---
 
## Estado actual
 
### Funciona
 
- CRUD de citas con validación de solapamientos
- Entrada por voz con `MediaRecorder` + `faster-whisper` (modelo `small`)
- Parser de texto libre a JSON con LiteLLM + OpenRouter (`z-ai/glm-4.5-air:free`)
- Manejo de ambigüedades — el parser pregunta si falta información
- Detección de sobrecarga diaria (>6h o sin pausa >90 min)
- Sugerencia de reprogramación con IA
- Servidor MCP con 3 herramientas protegido por token
- Tests de robustez para `transcribir` y `mcp`
### Queda flojo o pendiente
 
- La transcripción de voz no valida el tipo ni el tamaño del archivo — se puede enviar cualquier cosa
- El parser no limita la longitud del texto antes de mandarlo a OpenRouter
- La validación de solapamientos recorre todas las citas con hora — puede ser lenta con muchas citas
- EventoConHora es la base prevista para Cita, aún no está implementado
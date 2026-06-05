# Kore

> Sistema Operativo IA para PYMEs, micropymes y autónomos.

Kore es un **núcleo Django** sobre el que se cargan **apps modulares** que se hablan entre sí mediante MCP (Model Context Protocol) y un bus de eventos. La IA opera; el humano ordena, revisa y aprueba.

**Modelo de despliegue**: una instalación de Kore = un negocio (un autónomo o una pequeña empresa). El usuario se instala Kore en su máquina/servidor; abre un dashboard vacío; activa las apps que quiera. Sin multi-tenant en el código del núcleo. Para SaaS gestionado futuro: una instancia por cliente (estilo Odoo.sh, Plausible, Mattermost).

## Estado

Repo en construcción durante la fase formativa FFOE **18/05/2026 → 18/06/2026** por:

- **Cecilia Serrano Martín** — app `apps/calendario` (Calendario IA con voz)
- **Manuel Aparicio Doeste** — app `apps/facturas` (OCR facturas → Excel / Odoo)
- **Carmen Prieto Mendoza** (tutora dual de empresa — Asoc. Ia-Con)
- **Javier Jiménez-Alfaro Hacha** (tutor del centro — Staff Formación, Cádiz)

## Stack

- **Backend**: Django 5 + PostgreSQL 16 + pgvector
- **Frontend**: Django Templates + HTMX + Alpine.js + TailwindCSS
- **IA**: LiteLLM (BYOK / local Ollama / gestionado)
- **Workflows IA con humano en el bucle**: Weft (solo para esto)
- **Protocolo de apps**: MCP

## Estructura

```
kore/
├── kore/                    # Proyecto Django (settings, urls, wsgi)
├── apps/
│   ├── nucleo/              # Identidad, perfiles, 3 roles fijos, registro de apps
│   ├── calendario/          # App Cecilia
│   └── facturas/            # App Manuel
├── docs/
│   ├── plan-formacion/      # Plan de la fase formativa (visible al centro)
│   ├── calendario/          # Documentación de la app de Cecilia
│   ├── facturas/            # Documentación de la app de Manuel
│   ├── prl/                 # Entregables PRL de Manuel
│   └── sostenibilidad/      # Informe ASG conjunto
├── hackeo/                  # Hallazgos del hackeo cruzado (S5)
└── equipo/                  # Presentación de cada miembro
```

## Convenciones

- **Idioma del código**: español (funciones, clases, variables, commits). Excepciones: términos técnicos universales (`request`, `response`, `id`, `email`…) y dependencias externas.
- **Documentación**: español.
- **Permisos**: 3 roles fijos del núcleo (Admin / Operador / Solo lectura). Para ocultar algo a un usuario, no se le da esa app. Sin permisos de campo, sin reglas de registro, sin permisos extra/revocados por usuario (patrón anti-Odoo).
- **Cada commit con IA**: el mensaje incluye una sección `## Revisión de IA` indicando qué se modificó respecto a lo propuesto por la IA.

## Cómo arrancar (desarrollo local)

```bash
python -m venv venv
source venv/Scripts/activate     # Windows bash
pip install -r requirements.txt
cp .env.example .env             # rellenar DATABASE_URL y SECRET_KEY
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

> El fichero `requirements.txt` se generará el M 19/05 cuando se instale Django (día 2 del plan).
## Arranque local
1. **Clonar el repositorio**
```bash
   git clone https://github.com/tu-org/tu-repo.git
   cd tu-repo
```
2. **Crear y activar el entorno virtual**
```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows(PowerShell): .venv\Scripts\activate
```
3. **Instalar dependencias**
```bash
   pip install -r requirements.txt
```
4. **Configurar variables de entorno**
```bash
   cp .env.example .env
   # Edita .env con tus propias variables
```
5. **Crear la base de datos**
Para crear la base de datos, necesitar tener PostgreSQL instalado y funcionando. En pgAdmin4: Servers > PostgresSQL16 > Databases. Click derecho sobre Databases y y pulsar en Create > Database, ahí se escribe el nombre de la base de datos.

6. **Aplicar migraciones**
```bash
   python manage.py migrate
```
7. **Arrancar el servidor de desarrollo**
```bash
   python manage.py runserver
   # Disponible en http://127.0.0.1:8000
```

## Reset de BD local

Esta sección permite reiniciar completamente la base de datos en entorno local.

Este proceso elimina todos los datos actuales.

### 1. Parar el servidor

Detener la ejecución del servidor con:

bash ---> Ctrl + C

### Eliminar migraciones (apps del proyecto)

En el bash

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

### Borrar la base de datos (PostgreSQL)

En el bash

psql -U postgres

En SQL

DROP DATABASE nombre_bd;
CREATE DATABASE nombre_bd;

### Volver a crear migraciones

En el bash

python manage.py makemigrations
python manage.py migrate

## Decisiones
### Versiones
- asgiref>=3.8.1,<4
- Django>=5.2,<5.3
- psycopg>=3.1,<4
- psycopg-binary>=3.1,<4
- sqlparse>=0.3.1,<1
- django-environ>=0.13.0,<0.14.0

### Por qué PostgreSQL
Se ha usado PostgreSQL ya que es de código abierto, puede gestionar numerosas conexiones simúltaneas sin bajar su rendimiento.

### Estructura de carpetas
```
KORE/
├── docs/
│   └── plan-formacion/
│       ├── 01-plan-macro.md
│       ├── 02-semana-1-detalle.md
│       ├── 03-mapeo-RA.md
│       └── 04-hackeo-cruzado.md
├── equipo/
│   ├── cecilia.md
│   ├── manuel.md
├── kore/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── venv/
├── .env
├── .env.example
├── .gitignore
├── db.sqlite3
├── manage.py
├── README.md
└── requirements.txt
```

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

### Frases que **no** entiende (aún)

| Frase de entrada | Problema |
|---|---|
| `"Mañana por la tarde"` | "mañana" y "por la tarde" sin especificar hora no lo entiende |
| `"El 2 de agosto"` | formato "día de mes" en texto no está implementado |
| `"En dos semanas"` | expresiones relativas de semanas, no se resuelven excepto que escribas el día específico |
| `"Next Monday at 3pm"` | solo procesa frases en español |
| `"Reunión a mediodía"` | horas coloquiales (`mediodía`, `medianoche`) no reconocidas |

El parser rellena lo que puede y deja el resto del formulario en blanco para que el usuario lo complete o edite a su gusto.

---

## Limitación conocida: entrada de voz

La funcionalidad de entrada de voz depende de la Web Speech API de Google, cuyo endpoint está **bloqueado por las restricciones de red del entorno de desarrollo** actual.

**Síntoma:** el botón de micrófono no responde o lanza un error de red silencioso en el navegador.

**Solución prevista en S4:** migrar el reconocimiento de voz a un servicio dentro del servidor, eliminando la dependencia de los servidores de Google.

## Plan de formación

Mapeo a RA del Anexo I del convenio nº 110022372025020 (Junta de Andalucía) en [`docs/plan-formacion/03-mapeo-RA.md`](docs/plan-formacion/03-mapeo-RA.md).

| Bloque | Documento |
|--------|-----------|
| Plan macro 5 semanas | [`docs/plan-formacion/01-plan-macro.md`](docs/plan-formacion/01-plan-macro.md) |
| Semana 1 día a día | [`docs/plan-formacion/02-semana-1-detalle.md`](docs/plan-formacion/02-semana-1-detalle.md) |
| Mapeo RA → entregables | [`docs/plan-formacion/03-mapeo-RA.md`](docs/plan-formacion/03-mapeo-RA.md) |
| Reglas hackeo cruzado | [`docs/plan-formacion/04-hackeo-cruzado-reglas.md`](docs/plan-formacion/04-hackeo-cruzado-reglas.md) |

## Licencia

Open Core. Pendiente de elegir licencia exacta (probable: AGPL-3.0 para el núcleo, comercial para apps premium futuras).

---

Proyecto promovido por la **Asoc. para la Innovación y Automatización en Consultoría Tecnológica e IA — Ia-Con** (CIF G24910093, Málaga).

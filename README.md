# Kore

> Sistema Operativo IA para PYMEs, micropymes y autónomos.

Kore es un **núcleo Django multi-tenant** sobre el que se cargan **apps modulares** que se hablan entre sí mediante MCP (Model Context Protocol) y un bus de eventos. La IA opera; el humano ordena, revisa y aprueba.

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
│   ├── nucleo/              # Tenants, perfiles, registro de apps
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

- **Idioma del código**: español (funciones, clases, variables, commits). Excepciones: términos técnicos universales (`request`, `response`, `id`, `email`, `tenant`…) y dependencias externas.
- **Documentación**: español.
- **Multi-tenant**: por subdirectorio `/e/<slug>/` (sencillo en dev, migrable a subdominio en producción).
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
## Decisiones
### Versiones
- asgiref>=3.11.1,<3.11.2
- Django>=5.2,<5.3
- psycopg>=3.3.4,<3.3.5
- psycopg-binary>=3.3.4,<3.3.5
- python-decouple>=3.8.0.4,<3.8.05
- sqlparse>=0.5.5,<0.5.6
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

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

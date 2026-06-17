# Requisitos de sistema — Kore

## Entorno de desarrollo verificado

| Componente | Versión |
|---|---|
| Sistema operativo | Windows 11 |
| Python | 3.13.14 |
| PostgreSQL | 16 |
| Gestor de paquetes | pip (venv) |

## Dependencias principales

```
django
litellm
faster-whisper
pgvector
python-decouple
psycopg
openpyxl
reportlab
requests
```

El listado completo con versiones exactas está en `requirements.txt`.

## Extensiones de PostgreSQL necesarias

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Necesaria para la app de facturas (`pgvector`). Sin ella `python manage.py migrate` falla.

## Notas

- Se recomienda usar un entorno virtual (`python -m venv venv`)
- El archivo `.env` es obligatorio — sin él el servidor no arranca
- `faster-whisper` descarga el modelo de Whisper la primera vez que se usa (~460 MB para `small`)
# Módulo Facturas - Kore Enterprise Management System

Versión: 1.0
Última actualización: 12/06/2026
Responsable: Manuel Aparicio Doeste
IA utilizada para la complementación completa de la app: Claude Haiku 4.5, Claude sonnet 4.6, ChatGPT GPT-5, Grok y Gemini

## Descripción general

Sistema integral de gestión fiscal que automatiza el flujo completo de facturas: desde la captura (PDF/imagen), pasando por extracción inteligente de datos, validación cruzada con normativa y calendario, hasta análisis y exportación de reportes.

Puntos clave:
- Extracción automática con LLM (Gemma 4.31b + few-shot learning)
- Validación de duplicados y normativa relevante
- Integración con calendario para contexto empresarial
- Dashboard fiscal con métricas, gráficos y comparativas
- MCP endpoint para acceso programático
- Exportación a PDF con reportlab

## Flujo principal
┌─────────────────────────────────────────────────────────────────┐

│ 1- SUBIDA                                                       │

│ Usuario sube PDF/imagen de factura -> validación de formato     │

└─────────────────────────────────────────────────────────────────┘

│

┌─────────────────────────────────────────────────────────────────┐

│ 2. EXTRACCIÓN (IA)                                              │

│ Gemma 4.31b via OpenRouter + few-shot → extrae:                │

│ • número_factura                                                │

│ • fecha_emision (YYYY-MM-DD)                                    │

│ • nif_emisor (CIF/NIF del proveedor)                            │

│ • nombre_emisor (razón social)                                  │

│ • base_imponible                                                │

│ • iva_porcentaje (%)                                            │

│ • iva_total                                                     │

│ • total                                                         │

│ Si falla: marca error, usuario puede reintentar                 │

└─────────────────────────────────────────────────────────────────┘

│

┌─────────────────────────────────────────────────────────────────┐

│ 3- VALIDACIÓN                                                   │

│ • ¿Duplicado? (proveedor + número)                              │

│ • Busca normativa relevante (embeddings pgvector)               │

│ • Obtiene citas del mismo día (integración calendario MCP)      │

└─────────────────────────────────────────────────────────────────┘

│

┌──────────────────────────────────────────────────────────────────┐

│ 4- REVISIÓN (Manual)                                             │

│ Usuario revisa campos, sugiere categoría (IA) y acepta o rechaza │

│ Muestra fragmentos normativos + citas coincidentes               │

└──────────────────────────────────────────────────────────────────┘

│

┌─────────────────────────────────────────────────────────────────┐

│ 5- GUARDAR                                                      │

│ Se queda en BD + registra sugerencia IA (para auditoría)        │

└─────────────────────────────────────────────────────────────────┘

│

┌─────────────────────────────────────────────────────────────────┐

│ 6- DASHBOARD                                                    │

│ Métricas fiscales: IVA, totales, categorías y comparativas      │

│ Exportación a PDF con reportlab                                 │

└─────────────────────────────────────────────────────────────────┘

## Cómo arrancar desde cero

### Requisitos previos

- Python 3.11+
- PostgreSQL 14+ (obligatorio para pgvector)
- Git

### Clonar y entorno virtual

```bash
git clone https://github.com/iaconsultoria/kore.git
cd kore
python -m venv venv
source venv/Scripts/Activate.ps1  # Windows PowerShell
# o: source venv/bin/activate      # Linux/Mac
```

### Instalar dependencias

```bash
pip install -r requirements.txt --break-system-packages
```

Dependencias clave:
- Django 5.2 -> Framework web
- reportlab 4.0+ -> Generación PDF
- litellm 1.83+ -> Llamadas a IA (OpenRouter)
- pgvector 0.4+ -> Búsqueda semántica de normativa
- faster-whisper 1.2.1 -> Transcripción audio (calendario)
- psycopg 3.1+ -> Driver PostgreSQL

### Configurar variables de entorno (.env)

Sin estas variables, la app no arranca.

Crea .env en la raíz del proyecto:

```env
# --- BASE DE DATOS ---
# PostgreSQL es obligatorio para pgvector (búsqueda semántica)
DATABASE_URL=postgresql://kore_user:secure_password@localhost:5432/kore_db

# --- IA & APIs EXTERNAS ---
# OpenRouter API key (acceso a Gemma, Claude...)
# Obtener en: https://openrouter.ai/keys
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# --- TOKENS MCP (SEGURIDAD) ---
# Token para que calendario acceda a tu endpoint MCP
# Generar: python -c "import secrets; print(secrets.token_urlsafe(32))"
# IMPORTANTE: Debe coincidir con el de settings.MCP_SECRET_TOKEN en calendario
FACTURAS_MCP_TOKEN=eXFqWcA5vZ9nK2pL1mN3oP5qR7sT9uV0wX2yZ4aBcDeF6gH8iJ

# --- DJANGO ---
SECRET_KEY=tu-clave-super-segura-cambiar-en-produccion
DEBUG=True  # False en producción
ALLOWED_HOSTS=localhost,127.0.0.1
```

Cómo generar el token MCP:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Output: eXFqWcA5vZ9nK2pL1mN3oP5qR7sT9uV0wX2yZ4aBcDeF6gH8iJ...
# Copia este valor a FACTURAS_MCP_TOKEN
```

### Base de datos

```bash
# Crear BD en PostgreSQL (si no existe)
createdb kore_db

# Aplicar migraciones
python manage.py migrate

# Cargar datos iniciales (categorías de gasto)
python manage.py loaddata apps/facturas/fixtures/categorias.json

# (Opcional) Crear superusuario para admin
python manage.py createsuperuser
```

### Arrancar servidor

```bash
python manage.py runserver
```

Acceso:
- Dashboard: http://127.0.0.1:8000/facturas/dashboard-fiscal/
- Lista de facturas: http://127.0.0.1:8000/facturas/
- Admin Django: http://127.0.0.1:8000/admin/
- Endpoint MCP: http://127.0.0.1:8000/facturas/mcp/ (POST)

## URLs y Endpoints

### Web (HTML)

| URL | Método | Descripción |
|---|---|---|
| /facturas/ | GET | Lista de todas las facturas |
| /facturas/revisar/<id>/ | GET/POST | Revisar/editar extracción de factura |
| /facturas/revisar/<id>/comprobar-duplicado/ | GET | Verificar duplicados AJAX |
| /facturas/revisar/<id>/sugerir-categoria/ | GET | Sugerencia IA de categoría |
| /facturas/revisar/<id>/aceptar-sugerencia/ | POST | Aceptar sugerencia |
| /facturas/revisar/<id>/ignorar-sugerencia/ | POST | Rechazar sugerencia |
| /facturas/avisos-vencimiento/ | GET | Facturas próximas a vencer |
| /facturas/dashboard-fiscal/ | GET | Dashboard con métricas |
| /facturas/dashboard-fiscal/exportar-pdf/ | POST | Descargar PDF del dashboard |

### MCP (Programmatic API)

Endpoint: POST /facturas/mcp/

Autenticación: Header Authorization: Bearer <FACTURAS_MCP_TOKEN>

Herramientas disponibles:

#### 1. listar_facturas
```json
{
  "name": "listar_facturas",
  "arguments": {
    "limit": 10,
    "offset": 0
  }
}
```
Devuelve: Array de facturas con número, proveedor, fecha, total y categoría.

#### 2. buscar_por_proveedor
```json
{
  "name": "buscar_por_proveedor",
  "arguments": {
    "nombre": "Telefonica",
    "fecha_desde": "2026-01-01",
    "fecha_hasta": "2026-12-31",
    "total_minimo": 100,
    "total_maximo": 5000,
    "categoria": "Servicios"
  }
}
```
Devuelve: Array de facturas filtradas (todos los parámetros son opcionales).

#### 3. obtener_factura
```json
{
  "name": "obtener_factura",
  "arguments": {
    "id": 123
  }
}
```
Devuelve: Detalle completo con líneas.

#### 4. resumen_fiscal
```json
{
  "name": "resumen_fiscal",
  "arguments": {
    "mes": 6,
    "anio": 2026
  }
}
```
Devuelve: IVA total, número de facturas y categoría con más gasto.

Rate limit: 30 llamadas por minuto por token.

## Estado actual

### Funcionalidades completadas y en funcionamiento

| Feature | Status | Detalles |
|---|---|---|
| Subida de factura | Completo | Soporta PDF, PNG y JPG |
| Extracción LLM | Completo | Gemma 4.31b + few-shot via OpenRouter |
| Validación duplicados | Completo | Por proveedor + número_factura |
| Búsqueda normativa | Completo | Embeddings pgvector y búsqueda semántica |
| Sugerencia categoría | Completo | Few-shot con contexto de proveedor |
| Integración calendario | Completo | Muestra citas del mismo día (MCP) |
| Dashboard básico | Completo | IVA y gasto por categoría |
| Dashboard mejorado | Completo | Gráfico donut, comparativa mes anterior y contador sin clasificar |
| Exportar PDF | Completo | Reportlab y tabla de gastos |
| MCP endpoint | Completo | 4 herramientas, token Bearer y rate-limiting |
| Suite de tests | Completo | Unitarios + integración |

### Puntos frágiles (pendientes de fix)

| Punto | Descripción | Prioridad |
|---|---|---|
| E1.1 - Timing attack en token | Validación de token sin constante-time (vulnerable a brute-force) | CRÍTICA |
| E2 - File upload sin límite | /calendario/transcribir/ acepta archivos sin validar tamaño (DoS) | CRÍTICA |
| E1 - Token crash en calendario | Si MCP_SECRET_TOKEN no existe, error 500 en lugar de 403 | ALTA |
| E2.1 - SQL injection via icontains | buscar_por_proveedor puede ser explotado si token es comprometido | ALTA |
| Logging de acceso MCP | Sin trazabilidad de consultas (falta auditoría) | MEDIA |
| Rate-limiting en PDF export | Sin límite en /exportar-pdf/ (potencial DoS) | MEDIA |

Consulta: `auditoria-seguridad.md` para verlo completo.

## Arquitectura

### Estructura de directorios

apps/facturas/

├── admin.py                        # Registro de modelos en admin

├── apps.py                         # Configuración de app

├── forms.py                        # RevisionFacturaForm

├── models.py                       # 4 modelos: Factura, LineaFactura, CategoriaGasto, SugerenciaCategoria

├── urls.py                         # Routing (9 URLs)

├── utils.py                        # 3 funciones: buscar_normativa(), sugerir_categoria() y obtener_citas_del_mismo_dia()

├── views.py                        # 11 vistas + 1 MCP endpoint

├── probar_mcp.py                   # Script para probar endpoint MCP

├── README.md                       # Este archivo

│

├── servicios/

│   ├── extractor.py               # Función extraer_factura(ruta) -> dict

│   └── prompt_extraccion.py        # PROMPT_SISTEMA + 6 EJEMPLOS para few-shot

│

├── management/commands/

│   ├── buscar_normativa.py         # Comando para buscar fragmentos de normativa

│   ├── exportar_excel.py           # Comando para exportar facturas a Excel

│   ├── ingestar_normativa.py       # Comando para cargar normativa en BD

│   └── probar_extractor.py         # Comando para probar extractor con archivos locales

│

├── templates/facturas/

│   ├── lista_facturas.html         # Listado de facturas

│   ├── revisar_extraccion.html     # Interfaz principal (flujo completo)

│   ├── dashboard_fiscal.html       # Dashboard con métricas y gráficos

│   └── avisos_vencimiento.html     # Alertas de facturas por vencer

│

├── fixtures/

│   └── categorias_gasto.json       # Seed de 10 categorías iniciales

│

├── migrations/

│   ├── 0001_initial.py

│   ├── 0002_alter_categoriagasto_options...py

│   ├── 0003_fragmentonormativa.py

│   ├── 0004_alter_fragmentonormativa_embedding.py

│   ├── 0005_alter_fragmentonormativa_embedding.py

│   ├── 0006_factura_fecha_vencimiento.py

│   ├── 0007_factura_error_extraccion_factura_extraccion_fallida.py

│   ├── 0008_sugerenciacategoria.py

│   └── init.py

│

├── tests/

│   ├── test_extractor.py           # Tests para función extraer_factura()

│   └── init.py

│

└── init.py

### Comandos Django disponibles

```bash
# Ingestar normativa desde fuente externa a BD
python manage.py ingestar_normativa

# Buscar fragmentos normativos por texto
python manage.py buscar_normativa "energía renovable"

# Exportar todas las facturas a Excel
python manage.py exportar_excel

# Probar extractor con archivo local
python manage.py probar_extractor /ruta/a/factura.pdf
```

### Fixtures

```bash
# Cargar categorías iniciales
python manage.py loaddata apps/facturas/fixtures/categorias_gasto.json
```

## Consideraciones de seguridad

### Token MCP

- Generación: python -c "import secrets; print(secrets.token_urlsafe(32))"
- Almacenamiento: Variable de entorno FACTURAS_MCP_TOKEN
- Rotación: Cambiar en cada deploy
- Vulnerabilidad conocida: Timing attack (pendiente fix con hmac.compare_digest())

### Otras consideraciones

- BD: PostgreSQL obligatorio (SQLite no soporta pgvector)
- HTTPS: Usar en producción (tokens en headers)
- Rate limiting: 30 req/min en MCP sin límite en PDF export (pendiente)
- Auditoría: Registra sugerencias IA en SugerenciaCategoria y no registra consultas MCP (pendiente)

Vulnerabilidades detalladas: Ver `auditoria-seguridad.md`

Responsable: Manuel Aparicio Doeste
Fecha: 12/06/2026

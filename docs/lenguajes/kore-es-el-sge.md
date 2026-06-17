# Kore es el Sistema de Gestión Empresarial

## Introducción

Kore es un sistema de gestión empresarial (SGE) modular y nativo, construido sobre Django y PostgreSQL. A diferencia de sistemas genéricos externos como Odoo, Kore es:

- Propio: código abierto, bajo control total de la organización.
- Integrado: los módulos se comunican vía Model Context Protocol (MCP), con endpoints seguros y validados.
- Auditable: cada operación (factura, extracción y sugerencia) queda registrada en la BD.
- Escalable: arquitectura modular con apps Django independientes.

El caso de uso central es gestión de facturas: desde extracción de imágenes vía IA hasta categorización, búsqueda normativa y reportes fiscales. Este documento justifica por qué Kore es la solución adecuada frente a ERP externos.

## 1. Instalación y Configuración como Conjunto de Apps

Kore no es un monolito. Es un conjunto modular de aplicaciones Django que conviven en un mismo proyecto Django:

### Estructura real de Kore
kore/

├── manage.py

├── requirements.txt          # Dependencias: Django, psycopg, openpyxl, litellm

├── .env                      # Variables: DB, MCP_TOKEN, API_KEYS

├── kore/

│   ├── settings.py           # Configuración central Django

│   ├── urls.py               # Enrutamiento raíz

│   └── wsgi.py

├── apps/

│   ├── nucleo/               # Núcleo: modelos base, admin

│   │   ├── models.py         # (CategoriaGasto, Proveedor, etc.)

│   │   ├── admin.py

│   │   └── migrations/

│   ├── facturas/             # Gestión de facturas

│   │   ├── models.py         # Factura, LineaFactura, SugerenciaCategoria

│   │   ├── views.py          # MCP endpoint, dashboard, revisión

│   │   ├── urls.py           # /facturas/mcp/ ← endpoint MCP

│   │   ├── servicios/        # ExtractorGoogle, prompt engineering

│   │   ├── domain/           # Domain-driven design: documentos.py

│   │   └── migrations/

│   └── calendario/           # Calendario con su propio MCP

│       ├── models.py

│       ├── mcp/

│       └── urls.py

└── media/

└── facturas/             # Upload de imágenes de facturas

### Dependencias reales (requirements.txt)

Django>=5.2,<5.3

psycopg>=3.1,<4              # Driver PostgreSQL

openpyxl>=3.1.0,<4           # Exportación a Excel

litellm>=1.83.0,<2           # Llamadas a IA (Claude, etc.)

pgvector>=0.4.0,<1           # Embeddings para búsqueda normativa

faster-whisper==1.2.1        # Transcripción de audio

reportlab>=4.0,<5            # Generación de PDFs

### Instalación paso a paso

1. Clonar y entrar en venv:
```bash
   git clone <repo>
   cd kore
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
```

1. Instalar dependencias:
```bash
   pip install -r requirements.txt
```

1. Configurar .env:
SECRET_KEY=django-insecure-xxx

MCP_SECRET_TOKEN=token-para-facturas-mcp

FACTURAS_MCP_TOKEN=token-valido-para-endpoint

DEBUG=False
DB_NAME=kore_db

DB_USER=postgres

DB_PASSWORD=password

DB_HOST=localhost

DB_PORT=5432
OPENROUTER_API_KEY=sk-xxx  # Para IA

1. Ejecutar migraciones:
```bash
   python manage.py migrate
```

1. Crear superusuario (para admin):
```bash
   python manage.py createsuperuser
```

1. Iniciar servidor de desarrollo:
```bash
   python manage.py runserver
```

   Accede a http://localhost:8000/admin/ con tu usuario.

### Ventajas sobre Odoo

| Aspecto | Kore | Odoo |
|--------|------|------|
| Instalación | 6 pasos simples, Python + pip | Compleja, Docker/contenedores y múltiples servicios |
| Dependencias | 12 paquetes livianos | 50+, Wkhtmltopdf, Redis, etc. |
| Tamaño | ~500 MB | ~5-10 GB |
| Control | 100% del código, eres dueño | Limitado a módulos/personalizaciones soportadas |
| Hosting | Servidor Django simple (Gunicorn) | Infraestructura dedicada (Odoo Cloud) |
| Curva aprendizaje | Django standard | Proprietary (Odoo API, módulos) |

## 2. Integración de Módulos vía MCP: El Endpoint de Facturas

El Model Context Protocol (MCP) es cómo Kore expone sus servicios. Cada módulo (app Django) puede exponer herramientas que otros sistemas llaman de forma segura.

### 2.1 El Endpoint MCP de Facturas (Producción)

Ubicación: POST /facturas/mcp/
Token: Validado desde settings.py (FACTURAS_MCP_TOKEN)
Rate limit: 30 llamadas/minuto por token

El endpoint en apps/facturas/views.py expone 5 herramientas:

```python
# Desde apps/facturas/views.py (línea ~450)
@rate_limit_mcp
@csrf_exempt
@require_http_methods(["POST"])
def mcp_endpoint(request):
    """Endpoint MCP que maneja llamadas a herramientas."""

    # 1. Validar token
    token_esperado = os.getenv('FACTURAS_MCP_TOKEN')
    token_enviado = request.headers.get('Authorization', '').replace('Bearer ', '')

    if not token_esperado or token_enviado != token_esperado:
        return JsonResponse({"error": "No autorizado"}, status=401)

    # 2. Parsear JSON
    data = json.loads(request.body)
    tool_name = data.get("name")
    arguments = data.get("arguments", {})

    # 3. Validar parámetros según herramienta
    errores = validar_parametros(tool_name, arguments)
    if errores:
        return JsonResponse({"error": ", ".join(errores)}, status=400)

    # 4. Ejecutar herramienta correspondiente
    if tool_name == "extraer_factura_de_imagen":
        # OCR + extracción IA
        return extraer_factura_de_imagen(arguments)
    elif tool_name == "listar_facturas":
        return listar_facturas(arguments)
    # ... etc
```

### 2.2 Las 5 Herramientas

| Herramienta | Entrada | Salida | Caso de uso |
|-------------|---------|--------|------------|
| extraer_factura_de_imagen | imagen_base64 (str) | factura_id, numero, total, lineas_creadas | IA escanea PDF/imagen, crea factura automáticamente |
| listar_facturas | limit (1-100), offset | Array de facturas con id, numero, fecha, total | Dashboard, búsqueda paginada |
| buscar_por_proveedor | nombre, fecha_desde, fecha_hasta, total_minimo/maximo, categoria | Array de facturas filtradas | Auditoría, reportes específicos |
| obtener_factura | id (int) | Factura completa con líneas | Detalle de factura individual |
| resumen_fiscal | mes (1-12), año | Total IVA, facturas y categoría top | Dashboard fiscal mensual |

### 2.3 Ejemplo: Extracción de Factura (E2E)

Cliente (IA, sistema externo, etc) -> MCP de Facturas -> BD

```python
# Paso 1: Cliente prepara imagen
import base64
with open("factura.pdf", "rb") as f:
    imagen_base64 = base64.b64encode(f.read()).decode()

# Paso 2: Cliente llama al MCP
import requests
response = requests.post(
    http://localhost:8000/facturas/mcp/,
    json={
        'name': 'extraer_factura_de_imagen',
        'arguments': {'imagen_base64': imagen_base64}
    },
    headers={'Authorization': f'Bearer {FACTURAS_MCP_TOKEN}'}
)

# Paso 3: Respuesta
{
    "resultado": {
        "factura_id": 42,
        "numero_factura": "INV-2025-001",
        "proveedor": "Proveedor S.A.",
        "total": 1250.50,
        "lineas_creadas": 3,
        "mensaje": "Factura extraída y guardada correctamente"
    }
}
```

¿Qué sucede internamente?

1. OCR: ExtractorGoogle() lee imagen -> extrae texto, números y fechas
2. Validación: FacturaDomain.validar() verifica coherencia
3. Guardado: Crea modelo Factura + LineaFactura en BD
4. Signals (futuro): Al guardar podría disparar otras acciones (notificaciones, etc)

### 2.4 Validación de Parámetros

Antes de ejecutar el MCP valida:

```python
def validar_parametros(tool_name, arguments):
    """Valida parámetros según la herramienta."""
    errores = []

    if tool_name == "extraer_factura_de_imagen":
        imagen_base64 = arguments.get("imagen_base64")
        if not imagen_base64 or not isinstance(imagen_base64, str):
            errores.append("imagen_base64 debe ser una cadena no vacía")

    elif tool_name == "listar_facturas":
        limit = arguments.get("limit", 10)
        if not isinstance(limit, int) or limit < 1 or limit > 100:
            errores.append("limit debe ser un entero entre 1 y 100")
        offset = arguments.get("offset", 0)
        if not isinstance(offset, int) or offset < 0:
            errores.append("offset debe ser un entero >= 0")

    elif tool_name == "buscar_por_proveedor":
        nombre = arguments.get("nombre", "")
        if not nombre or not isinstance(nombre, str) or len(nombre.strip()) == 0:
            errores.append("nombre debe ser una cadena no vacía")

        fecha_desde = arguments.get("fecha_desde")
        if fecha_desde and not isinstance(fecha_desde, str):
            errores.append("fecha_desde debe ser string formato YYYY-MM-DD")

        fecha_hasta = arguments.get("fecha_hasta")
        if fecha_hasta and not isinstance(fecha_hasta, str):
            errores.append("fecha_hasta debe ser string formato YYYY-MM-DD")

        total_minimo = arguments.get("total_minimo")
        if total_minimo is not None and not isinstance(total_minimo, (int, float)):
            errores.append("total_minimo debe ser un número")

        total_maximo = arguments.get("total_maximo")
        if total_maximo is not None and not isinstance(total_maximo, (int, float)):
            errores.append("total_maximo debe ser un número")

        categoria = arguments.get("categoria")
        if categoria and not isinstance(categoria, str):
            errores.append("categoria debe ser string")

    elif tool_name == "obtener_factura":
        id_factura = arguments.get("id")
        if not isinstance(id_factura, int) or id_factura < 1:
            errores.append("id debe ser un entero > 0")

    elif tool_name == "resumen_fiscal":
        mes = arguments.get("mes")
        anio = arguments.get("anio")
        if not isinstance(mes, int) or mes < 1 or mes > 12:
            errores.append("mes debe ser un entero entre 1 y 12")
        if not isinstance(anio, int) or anio < 1950 or anio > 2100:
            errores.append("anio debe ser un entero entre 1950 y 2100")

    return errores
```

Ventaja: Rechaza ataques triviales (SQL injection, type confusion, etc) antes de tocar la BD.

### 2.5 Ventaja sobre APIs genéricas (REST)

| Aspecto | MCP (Kore) | REST genérico |
|---------|-----------|--------------|
| Descubrimiento | Herramientas auto-descritas con JSON Schema | Documentación manual (Swagger, etc) |
| Seguridad | Token MCP + rate limit por token | API key global |
| Validación | Centralizada y reutilizable | Cada endpoint la hace |
| Errors | Estructurados y machine-readable | Inconsistentes entre endpoints |
| Escalabilidad | Herramienta = función sin estado | Routing HTTP overhead |

## 3. Seguridad: Tokens MCP y Rate Limiting

### 3.1 Token MCP (Implementación Actual)

En Kore el acceso al endpoint MCP se valida con un token simple almacenado en .env:

```bash
# .env
FACTURAS_MCP_TOKEN=super-secret-token-12345
```

Validación en endpoint:

```python
# apps/facturas/views.py (línea ~450)
def mcp_endpoint(request):
    # Leer token de environment
    token_esperado = os.getenv('FACTURAS_MCP_TOKEN')
    token_enviado = request.headers.get('Authorization', '').replace('Bearer ', '')

    # Comparar
    if not token_esperado or token_enviado != token_esperado:
        return JsonResponse({"error": "No autorizado"}, status=401)

    # Continuar con lógica del endpoint...
```

Cliente hace llamada así:

```bash
curl -X POST http://localhost:8000/facturas/mcp/ \
  -H "Authorization: Bearer super-secret-token-12345" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "listar_facturas",
    "arguments": {"limit": 10}
  }'
```

### 3.2 Rate Limiting por Token

Kore implementa rate limiting automático: máx 30 llamadas/minuto por token.

```python
# Decorator en views.py
def rate_limit_mcp(view_func):
    """Rate limit: 30 llamadas por minuto por token."""
    def wrapper(request, *args, **kwargs):
        token_enviado = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token_enviado:
            token_enviado = 'sin-token'

        cache_key = f"mcp_calls_{token_enviado}"
        llamadas = cache.get(cache_key, [])

        ahora = timezone.now().timestamp()
        hace_un_minuto = ahora - 60

        # Limpia llamadas de hace más de 1 minuto
        llamadas = [t for t in llamadas if t > hace_un_minuto]

        if len(llamadas) >= 30:
            return JsonResponse(
                {"error": "Demasiadas solicitudes. Límite: 30 por minuto."},
                status=429
            )

        llamadas.append(ahora)
        cache.set(cache_key, llamadas, 60)

        return view_func(request, *args, **kwargs)
    return wrapper
```

Resultado: Si alguien intenta 31+ llamadas en 60 segundos recibe:

```json
{
  "error": "Demasiadas solicitudes. Límite: 30 por minuto."
}
```

Status HTTP: 429 Too Many Requests

### 3.3 Validación de Parámetros (Defense in Depth)

Antes de ejecutar cualquier herramienta, Kore valida tipos y rangos:

```python
def validar_parametros(tool_name, arguments):
    """Valida parámetros según la herramienta."""
    errores = []

    if tool_name == "listar_facturas":
        limit = arguments.get("limit", 10)
        offset = arguments.get("offset", 0)

        if not isinstance(limit, int) or limit < 1 or limit > 100:
            errores.append("limit debe ser un entero entre 1 y 100")
        if not isinstance(offset, int) or offset < 0:
            errores.append("offset debe ser un entero >= 0")

    elif tool_name == "resumen_fiscal":
        mes = arguments.get("mes")
        anio = arguments.get("anio")

        if not isinstance(mes, int) or mes < 1 or mes > 12:
            errores.append("mes debe ser un entero entre 1 y 12")
        if not isinstance(anio, int) or anio < 1950 or anio > 2100:
            errores.append("anio debe ser un entero entre 1950 y 2100")

    return errores
```

Ventaja: Rechaza ataques triviales (SQL injection, type confusion, etc) antes de tocar la BD.

### 3.4 Mejora Futura: TokenMCP en Núcleo

Para multitenancy completo, Kore podría tener un modelo TokenMCP en apps/nucleo/:

```python
# apps/nucleo/models.py (propuesta para futuro)
class TokenMCP(models.Model):
    """Token para acceso MCP, con auditoría"""
    nombre = models.CharField(max_length=100)
    valor = models.CharField(max_length=255, unique=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    expira_en = models.DateTimeField(null=True, blank=True)
    llamadas_totales = models.IntegerField(default=0)  # Auditoría

    def es_valido(self):
        from django.utils import timezone
        return self.activo and (
            self.expira_en is None or
            self.expira_en > timezone.now()
        )
```

Esto permitiría:
- Múltiples tokens por cliente
- Expiración automática
- Auditoría completa de llamadas
- Rotación de keys

### 3.5 Comparativa de Seguridad

| Aspecto | Kore Actual | Kore Futuro | Odoo |
|---------|-----------|-----------|------|
| Token | .env (simple) | TokenMCP + BD | API key global |
| Rate limit | 30/min por token | Configurable por token | Sin rate limit nativo |
| Validación | Parámetros strict | + Type hints | Débil |
| Auditoría | Logs Django | + Modelo TokenMCP | Limitada |
| Expiración | Manual | Automática | No |
| Revocación | Restart | Inmediata | Comprar soporte |

## 4. Reportes Fiscales: Dashboard y Exportación

### 4.1 Dashboard Fiscal (Producción)

El dashboard está en apps/facturas/views.py y agrega datos del mes actual y anterior:

```python
# apps/facturas/views.py (línea ~200)
def dashboard_fiscal(request):
    from django.db.models import Sum

    hoy = timezone.now().date()

    # Período: mes actual
    mes_actual = hoy.month
    anio_actual = hoy.year

    # Mes anterior
    if mes_actual == 1:
        mes_anterior = 12
        anio_anterior = anio_actual - 1
    else:
        mes_anterior = mes_actual - 1
        anio_anterior = anio_actual

    # IVA soportado (mes actual)
    lineas_mes = LineaFactura.objects.filter(
        factura__fecha_emision__month=mes_actual,
        factura__fecha_emision__year=anio_actual
    )
    iva_mes = sum(
        (linea.precio_unitario * linea.cantidad * linea.iva_porcentaje / 100)
        for linea in lineas_mes
    )

    # Gastos por categoría (mes actual)
    gastos_por_categoria = Factura.objects.filter(
        categoria__isnull=False,
        fecha_emision__month=mes_actual,
        fecha_emision__year=anio_actual
    ).values('categoria__nombre').annotate(
        total=Sum('base_imponible')
    ).order_by('-total')

    # Total mes actual
    total_mes_actual = sum(cat['total'] for cat in gastos_por_categoria) or 0

    # Total mes anterior (comparativa)
    total_mes_anterior = Factura.objects.filter(
        fecha_emision__month=mes_anterior,
        fecha_emision__year=anio_anterior
    ).aggregate(total=Sum('base_imponible'))['total'] or 0

    # Facturas sin clasificar
    sin_clasificar = Factura.objects.filter(
        categoria__isnull=True,
        fecha_emision__month=mes_actual,
        fecha_emision__year=anio_actual
    ).count()

    # Datos para gráfico (Chart.js)
    categorias_nombres = [cat['categoria__nombre'] for cat in gastos_por_categoria]
    categorias_totales = [float(cat['total']) for cat in gastos_por_categoria]

    return render(request, 'facturas/dashboard_fiscal.html', {
        'iva_mes': iva_mes,
        'gastos_por_categoria': gastos_por_categoria,
        'sin_clasificar': sin_clasificar,
        'total_mes_actual': total_mes_actual,
        'total_mes_anterior': total_mes_anterior,
        'categorias_nombres': categorias_nombres,
        'categorias_totales': categorias_totales,
        'mes_actual': mes_actual,
        'anio_actual': anio_actual,
    })
```

Dados del dashboard:

```json
{
    "iva_mes": 2100.50,
    "total_mes_actual": 10000.00,
    "total_mes_anterior": 8500.00,
    "sin_clasificar": 2,
    "gastos_por_categoria": [
        {
            "categoria__nombre": "Suministros",
            "total": 5000.00
        },
        {
            "categoria__nombre": "Servicios",
            "total": 5000.00
        }
    ]
}
```

### 4.2 Exportación a PDF (ReportLab)

Kore puede generar PDF descargables sin dependencias complejas:

```python
# apps/facturas/views.py (línea ~600)
def exportar_dashboard_pdf(request):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from django.db.models import Sum
    import io

    hoy = timezone.now().date()
    mes_actual = hoy.month
    anio_actual = hoy.year

    # [Mismo cálculo que dashboard_fiscal]
    # ... iva_mes, gastos_por_categoria, etc.

    # Crear PDF en memoria
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Título
    elements.append(Paragraph("Resumen Fiscal Mensual – Kore", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Período: {mes_actual}/{anio_actual}", styles['Normal']))
    elements.append(Spacer(1, 20))

    # Tabla de datos
    resumen = [
        ['Concepto', 'Importe'],
        ['IVA soportado (mes)', f"{iva_mes:.2f} €"],
        ['Gasto total mes actual', f"{total_mes_actual:.2f} €"],
        ['Gasto total mes anterior', f"{total_mes_anterior:.2f} €"],
        ['Facturas sin clasificar', str(sin_clasificar)],
    ]

    t = Table(resumen, colWidths=[300, 150])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007bff')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(t)

    # Construir PDF
    doc.build(elements)
    buffer.seek(0)

    return HttpResponse(
        buffer,
        content_type='application/pdf',
        headers={
            'Content-Disposition': f'attachment; filename="dashboard_fiscal_{mes_actual}_{anio_actual}.pdf"'
        }
    )
```

 Cliente descarga así:

```html
<a href="/facturas/dashboard-fiscal/exportar-pdf/">
    📄 Descargar PDF del mes
</a>
```

### 4.3 Exportación a Excel (openpyxl)

Con openpyxl, Kore puede generar reportes Excel formateados:

```bash
# Ya está en requirements.txt
openpyxl>=3.1.0,<4
```

Ejemplo (management command):

```python
# apps/facturas/management/commands/exportar_excel.py
from django.core.management.base import BaseCommand
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from apps.facturas.models import Factura

class Command(BaseCommand):
    def handle(self, *args, **options):
        wb = Workbook()
        ws = wb.active
        ws.title = 'Facturas'

        # Encabezados
        headers = ['Número', 'Proveedor', 'Fecha', 'Base', 'IVA', 'Total']
        ws.append(headers)

        # Estilo encabezado
        header_fill = PatternFill(start_color='0066cc', end_color='0066cc', fill_type='solid')
        header_font = Font(bold=True, color='FFFFFF')
        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font

        # Datos
        for factura in Factura.objects.all():
            ws.append([
                factura.numero_factura,
                factura.proveedor.nombre,
                factura.fecha_emision.isoformat(),
                float(factura.base_imponible),
                float(factura.iva_total),
                float(factura.total)
            ])

        # Guardar
        wb.save('/tmp/facturas_export.xlsx')
        self.stdout.write(self.style.SUCCESS('✓ Exportado a /tmp/facturas_export.xlsx'))
```

Ejecutar:

```bash
python manage.py exportar_excel
```

### 4.4 Ventaja sobre Odoo

| Aspecto | Kore | Odoo |
|--------|------|------|
| Reportes | Django ORM + templates nativos | Templates propietarios, Odoo Studio |
| PDF | ReportLab (~300 KB) y control total | Módulo wkhtmltopdf integrado |
| Excel | openpyxl, formato libre | Módulo separado y costo extra |
| Dashboard | HTML + Chart.js (liviano) | Módulo separado y requiere config |
| Query time | Optimizado para tu modelo | Genérico y puede ser lento |
| Privacidad | Datos siempre locales | SaaS = servidor externo |

## 5. Estado Actual de Kore (Sprint 4)

### 5.1 ¿Qué hay implementado?

Modelos:
- Factura, LineaFactura, CategoriaGasto y Proveedor
- SugerenciaCategoria (para auditoría de IA)
- FragmentoNormativa (con embeddings pgvector)

MCP Endpoint (/facturas/mcp/):
- Validación de token
- Rate limiting (30 req/min)
- 5 herramientas: extraer, listar, buscar, obtener y resumen_fiscal

Dashboard Fiscal:
- IVA soportado (mes)
- Gastos por categoría
- Comparativa mes anterior
- PDF export

Servicios:
- ExtractorGoogle: OCR + IA para extracción
- sugerir_categoria(): IA sugiere categoría
- buscar_normativa_por_texto(): búsqueda vectorial

UI:
- Revisión manual de facturas
- Aceptar/rechazar sugerencias
- Comprobar duplicados
- Avisos de vencimiento

### 5.2 ¿Qué falta?

- Modelo TokenMCP en nucleo para auditoría completa
- Middleware global de autenticación MCP
- Exportación nativa a Excel desde UI
- Integración real con calendario (envío de citas)
- Trazabilidad de llamadas MCP (logs)

### 5.3 Comparativa Final: Kore vs Odoo

| Criterio | Kore | Odoo |
|----------|------|------|
| Instalación | 6 pasos, ~15 min | Docker + múltiples servicios, ~1 hora |
| BD | PostgreSQL (tuya) | PostgreSQL en servidor Odoo |
| Modelos | Django ORM (estándar) | Proprietary (campos ORM) |
| MCP | Nativo y endpoint validado | REST API genérica |
| Seguridad | Token + rate limit + validación | API key global |
| Reportes | ReportLab + openpyxl (libres) | Odoo Studio (licencia) |
| Costo | Inversión una vez | Licencias mensuales |
| Escalabilidad | Horizontal (apps independientes) | Vertical (monolito) |
| Auditoría | Logs Django + signals | Módulo separado |
| Código | Tuyo, puedes modificar todo | Limitado a customizaciones |

## 6. Conclusión

Kore es un ERP modular construido nativamente sobre Django.

No es un "sistema genérico que se adapta a ti". Es tu sistema, diseñado específicamente para:

Facturación con IA: extracción automática, sugerencias inteligentes, auditoría.
MCP seguro: endpoints validados, rate limiting, parámetros estrictos.
Reportes nativos: PDF con ReportLab, Excel con openpyxl y dashboards con Django ORM.
Escalabilidad modular: cada app es independiente y fallos aislados.
Privacidad: datos siempre en tus manos, sin SaaS externo.

El flujo extracción de imagen -> factura en BD -> dashboard fiscal ilustra cómo Kore funciona: simple, directo y 100% controlable

Odoo es para empresas que quieren un sistema de catálogo. Kore es para organizaciones que quieren un sistema que sea completamente suyo.

Fecha: 12/06/2026
Auditor: Manuel Aparicio (Facturas)
Objetivo: Identificación de vectores de ataque

## Vulnerabilidades en apps/calendario/

### E1- Crash de validación por variable de entorno no inicializada

Severidad: ALTA (Disclosure + DoS)

Ubicación: apps/calendario/views.py, línea 14 (endpoint mcp())

Código vulnerable:
```python
if auth != f"Bearer {settings.MCP_SECRET_TOKEN}":
    return JsonResponse({"error": "No autorizado"}, status=403)
```

Problema: Si MCP_SECRET_TOKEN no existe en settings.py, Django lanza AttributeError antes de evaluar la condición. El cliente recibe 500 Internal Server Error con stack trace.

Vector de ataque:
1. Atacante hace POST a /calendario/mcp/ sin token
2. settings.MCP_SECRET_TOKEN no está definido
3. Servidor crashea, devuelve error 500 + stack trace
4. Atacante ve MCP_SECRET_TOKEN no existe en settings

Impacto:
- Fuga de información en la estructura interna
- Denial of service si se ejecuta en loop
- Fácil enumeracion de endpoints sin protección

Fix que recomiendo:
```python
token_esperado = getattr(settings, 'MCP_SECRET_TOKEN', None)
if not token_esperado or auth != f"Bearer {token_esperado}":
    return JsonResponse({"error": "No autorizado"}, status=403)
```

### E2- Missing file size validation en `/calendario/transcribir/`

Severidad: ALTA (Denial of Service)

Ubicación: apps/calendario/views.py, línea 172 (transcribir())

Código vulnerable:
```python
audio = request.FILES.get("audio")
if not audio:
    return JsonResponse({"error": "..."}, status=400)

with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp:
    for chunk in audio.chunks():
        tmp.write(chunk)  # ← Sin límite de tamaño
    tmp_path = tmp.name
```

Problema: No hay validación del tamaño del archivo. Un atacante envía un archivo de 10GB, se escribe en /tmp y el disco estaría lleno y toda la app falla.

Vector de ataque:
1. Atacante construye un archivo de 50GB en formato webm
2. POST a /calendario/transcribir/ con ese archivo
3. Servidor intenta escribir en tempfile y el disco acaba lleno
4. Otros usuarios no pueden crear archivos, los logs fallan y la BD baja

Impacto:
- Denial of service para todos los usuarios
- Pérdida de datos si el disco crítico se llena
- Crash silencioso de funciones dependientes

Fix:
```python
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
if audio.size > MAX_FILE_SIZE:
    return JsonResponse(
        {"error": f"Archivo muy grande. Máximo: {MAX_FILE_SIZE / 1024 / 1024}MB"},
        status=413
    )

with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp:
    for chunk in audio.chunks():
        tmp.write(chunk)
```

### E3- Missing output validation en parser IA

Severidad: MEDIA (Data Integrity)

Ubicación: apps/calendario/views.py, línea 72 (cita_desde_texto())

Código vulnerable:
```python
resultado = parsear_texto_a_cita(texto)  # Retorna dict, sin validación

if "clarificacion_necesaria" in resultado:
    return render(...)

form = CitaForm(initial={
    "titulo": resultado.get("titulo", ""),
    "inicio": resultado.get("inicio", ""),
    "hora_inicio": resultado.get("hora_inicio", ""),
    "categoria": resultado.get("categoria_sugerida", ""),
    "anotaciones": resultado.get("anotaciones", ""),
})
```

Problema: El parser IA (parsear_texto_a_cita()) puede retornar:
- Dict malformado si falla la IA
- Claves vacías si el parser se confunde
- Valores inválidos para DateField o TimeField

No hay validación. El form se pre-rellena con valores por defecto vacíos. El usuario no sabe si la IA falló.

Vector de ataque:
1. Atacante envía texto malformado a /calendario/cita_desde_texto/
2. Parser IA retorna dict incorrecto
3. Form se pre-rellena con defaults y el usuario no lo nota
4. Datos inconsistentes en BD lo que es difícil debuggear

Impacto:
- Datos corruptos o incompletos en BD
- UX pobre ya que el usuario cree que todo funcionó correctamente
- Difícil auditoría de qué fue la IA y que fue el usuario

Fix:
```python
resultado = parsear_texto_a_cita(texto)

# Validar estructura del retorno
if not isinstance(resultado, dict) or "titulo" not in resultado:
    return render(request, "calendario/partials/error_parsing.html", {
        "mensaje": "No se pudo procesar el texto. Intenta con otra entrada."
    })

# Validar que no estén todos los campos vacíos
if not resultado.get("titulo"):
    return render(request, "calendario/partials/error_parsing.html", {
        "mensaje": "El parser no identificó un título. Intenta de nuevo."
    })

form = CitaForm(initial={...})
```

## Vulnerabilidades en apps/facturas/

### E1.1- Missing Bearer token validation en /facturas/mcp/

Severidad: ALTA (Broken Authentication)

Ubicación: apps/facturas/views.py, línea 303 (mcp_endpoint())

**Código:**
```python
@rate_limit_mcp
@csrf_exempt
@require_http_methods(["POST"])
def mcp_endpoint(request):
    token_esperado = os.getenv('FACTURAS_MCP_TOKEN')
    token_enviado = request.headers.get('Authorization', '').replace('Bearer ', '')

    if not token_esperado or token_enviado != token_esperado:
        return JsonResponse({"error": "No autorizado"}, status=401)
```

Problema: Aunque la validación está, no hay timeout en la comparación de tokens. Un atacante puede:
1. Hacer 1000 requests con tokens aleatorios
2. Medir los tiempos de respuesta (timing attack)
3. Deducir caracteres correctos del token bit a bit

Además el token se envía por HTTP sin encriptación, no es HTTPS.

Vector de ataque (timing attack):

POST /facturas/mcp/ Bearer aaaaaa...  → 0.001s (fallo rápido)

POST /facturas/mcp/ Bearer eXFqW...   → 0.002s (match parcial)

POST /facturas/mcp/ Bearer eXFqWc...  → 0.003s (más caracteres correctos)

Impacto:
- Brute-force del token en 10 horas aproximadamente 32 caracteres en base64
- Acceso a todas las herramientas MCP de facturas
- Lectura y manipulación de datos fiscal

Fix:
```python
import hmac
import hashlib

token_esperado = os.getenv('FACTURAS_MCP_TOKEN')
token_enviado = request.headers.get('Authorization', '').replace('Bearer ', '')

# Comparación constante-time
if not token_esperado or not hmac.compare_digest(token_enviado, token_esperado):
    return JsonResponse({"error": "No autorizado"}, status=401)
```

### E2.1- SQL Injection risk en buscar_por_proveedor()

Severidad: MEDIA (Potential Data Disclosure)

Ubicación: apps/facturas/views.py, línea 344 (mcp_endpoint())

Código:
```python
elif tool_name == "buscar_por_proveedor":
    nombre = arguments.get("nombre", "")
    # ...
    query = Factura.objects.filter(
        proveedor__nombre__icontains=nombre  # El usuario controla esto
    )
```

Problema: Aunque Django ORM escapa consultas, icontains es case-insensitive y permite wildcards. Un atacante con acceso al token puede:
1. Enviar nombre="*" y obtiene todas las facturas
2. Enviar nombre="a" y enumera proveedores que contienen "a" por ejemplo
3. Combinar con otros filtros y hacer una data exfiltration

Vector de ataque:
```json
{
  "name": "buscar_por_proveedor",
  "arguments": {
    "nombre": "%",
    "total_minimo": 0,
    "total_maximo": 999999
  }
}
```
Devuelve: Todas las facturas de todos los proveedores (data dump).

Impacto:
- Data exfiltration si token es comprometido
- Es impsible auditar qué datos fueron consultados
- Escalada: combinado con el timing attack el atacante llega aquí

Fix:
```python
# Limitar longitud y caracteres de búsqueda
nombre = arguments.get("nombre", "").strip()
if len(nombre) < 2 or len(nombre) > 50:
    return JsonResponse({"error": "nombre debe tener 2-50 caracteres"}, status=400)

# Prohibir caracteres especiales
import re
if not re.match(r'^[a-zA-Z0-9\s\-\.]*$', nombre):
    return JsonResponse({"error": "nombre contiene caracteres no permitidos"}, status=400)

query = Factura.objects.filter(
    proveedor__nombre__icontains=nombre
)

# Limitar resultados (paginación)
query = query[:10]  # Max 10 resultados
```

## Resumen de riesgos cruzados

| Vulnerabilidad | App | Impacto si se ataca app facturas | Impacto si atacas la app calendario |
|---|---|---|---|
| E1 - Token crash | Calendario | No aplica | Fácil enumeracion |
| E2 - File upload DoS | Calendario | No aplica | Crítico: bloquea servidor |
| E3 - Parser validation | Calendario | No aplica | Datos corruptos |
| E1.1 - Timing attack token | Facturas | Crítico: brute-force token MCP | Brute-force tu token |
| E2.1 - SQL injection icontains | Facturas | Data exfiltration si B1 funciona | No aplica |

Recomendaciones de prioridad:
1. CRÍTICO: Fijar E2 (file upload DoS) en calendario se bloquea la app
2. CRÍTICO: Fijar E1.1 (timing attack) en facturas el token es atacable
3. ALTO: Fijar E1 (token crash) en calendario
4. ALTO: Fijar E2.1 (SQL injection) en facturas
5. MEDIO: Fijar E3 (parser validation) en calendario

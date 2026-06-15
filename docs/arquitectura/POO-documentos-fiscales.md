# Arquitectura POO: Documentos Fiscales

## Decisión Arquitectónica

### Problema
- Duplicación de código entre Factura, Ticket y Abono
- Acoplamiento a implementación específica del extractor OCR (Google/LiteLLM)
- Imposibilidad de cambiar motor OCR sin refactorizar varias capas

### Solución: SOLID + Domain-Driven Design

#### 1. Jerarquía de Documentos Fiscales

Clase abstracta base:
DocumentoFiscal (ABC)

├── Factura (con IVA, retención)

├── Ticket (venta simplificada)

└── Abono (nota de crédito)

Ubicación: apps/facturas/domain/documentos.py

Ventajas:
- Contrato explícito (métodos abstractos: validar(), obtener_lineas())
- DRY: no repetir numero, fecha, total, estado
- Fácil agregar nuevo tipo: hereda de DocumentoFiscal
- Testeable: sin dependencias de Django

#### 2. Interfaz de Extractores OCR

Interfaz abstracta:
ExtractorOCR (ABC)

├── ExtractorGoogle (LiteLLM + OpenRouter)

└── ExtractorOpenAI (futuro)

Ubicación: apps/facturas/domain/extractores.py

Métodos del contrato:
- extraer(imagen_bytes: bytes) -> dict
- obtener_confianza() -> float
- obtener_modelo() -> str

Ventajas:
- SOLID: Dependency Inversion (inyectar interfaz, no implementación)
- Cambiar Google -> OpenAI sin tocar vistas
- Easy testing: mock de ExtractorOCR

### Capas de Arquitectura
┌─────────────────────────────────────┐

│   views.py / admin.py               │ <- Vista

├─────────────────────────────────────┤

│   servicios/extractor.py            │ <- Servicio concreto

│   (ExtractorGoogle)                 │

├─────────────────────────────────────┤

│   domain/extractores.py             │ <- Interfaz (ABC)

│   domain/documentos.py              │

├─────────────────────────────────────┤

│   models.py (Django ORM)            │ <- Persistencia

└─────────────────────────────────────┘

Separación clara:
- Domain (puro): lógica de negocio, sin Django
- Servicios (concreto): implementaciones específicas
- Models (persistencia): solo Django ORM
- Vistas (entrada): coordinan todo

### Cómo usar en código

#### Extraer factura (legacy, compatible):
```python
from facturas.servicios.extractor import extraer_factura

datos = extraer_factura("ruta/a/factura.pdf")
```

#### Extraer factura (new way, inyectable):
```python
from facturas.servicios.extractor import ExtractorGoogle
from facturas.domain.documentos import Factura

extractor = ExtractorGoogle()
resultado = extractor.extraer(imagen_bytes)

if not resultado.get("extraccion_fallida"):
    factura = Factura(
        numero=resultado["numero_factura"],
        fecha=resultado["fecha_factura"],
        total=resultado["total"]
    )
    if factura.validar():
        print(f"✅ {factura}")
```

#### En tests (mockear extractor):
```python
from unittest.mock import Mock
from facturas.domain.extractores import ExtractorOCR

mock_extractor = Mock(spec=ExtractorOCR)
mock_extractor.extraer.return_value = {
    "numero_factura": "2024-001",
    "fecha_factura": "2024-01-15",
    "total": "500.00"
}
```

### Cómo agregar nuevo tipo de documento

Ejemplo: PedidoAcreedor

```python
# En apps/facturas/domain/documentos.py

class PedidoAcreedor(DocumentoFiscal):
    """Solicitud de abono futuro."""

    def __init__(self, numero: str, fecha: date, total: Decimal, estado: str = "draft"):
        super().__init__(numero, fecha, total, estado)

    def validar(self) -> bool:
        return bool(self.numero) and self.total > 0

    def obtener_lineas(self) -> List[dict]:
        return []
```

### Cómo agregar nuevo extractor

Ejemplo: ExtractorOpenAI

```python
# En apps/facturas/servicios/extractor.py

class ExtractorOpenAI(ExtractorOCR):
    """Implementación con OpenAI Vision API."""

    def __init__(self):
        self.modelo = "gpt-4-vision-preview"
        self.api_key = os.getenv("OPENAI_API_KEY")
        self._confianza_ultima = 0.0

    def extraer(self, imagen_bytes: bytes) -> dict:
        # Tu implementación aquí
        pass

    def obtener_confianza(self) -> float:
        return self._confianza_ultima

    def obtener_modelo(self) -> str:
        return self.modelo
```

En vistas:
```python
# Cambiar de un extractor a otro es trivial
extractor = ExtractorOpenAI()  # antes: ExtractorGoogle()
resultado = extractor.extraer(imagen_bytes)
```

### Riesgos mitigados

| Riesgo | Mitigación |
|--------|-----------|
| Acoplamiento a Google | Interfaz ExtractorOCR |
| Duplicación de código | Herencia de DocumentoFiscal |
| Tests con BD | Domain puro, sin Django |
| Agregar nuevo doc/extractor | Hereda + implementa métodos |

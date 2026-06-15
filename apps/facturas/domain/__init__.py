"""
Domain layer: lógica pura de negocio.

Clases abstractas para documentos fiscales y extractores OCR.
Sin dependencias de Django.
"""

from .documentos import DocumentoFiscal, Factura, Ticket, Abono
from .extractores import ExtractorOCR

__all__ = [
    "DocumentoFiscal",
    "Factura",
    "Ticket",
    "Abono",
    "ExtractorOCR",
]

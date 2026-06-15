from abc import ABC, abstractmethod
from decimal import Decimal
from datetime import date
from typing import List, Optional


class DocumentoFiscal(ABC):
    """
    Clase abstracta base para todos los documentos fiscales.

    Define el contrato que deben cumplir Factura, Ticket, Abono.
    PURO: sin dependencias de Django.
    """

    def __init__(
        self,
        numero: str,
        fecha: date,
        total: Decimal,
        estado: str = "draft"
    ):
        self.numero = numero
        self.fecha = fecha
        self.total = total
        self.estado = estado  # draft, validated, archived

    @abstractmethod
    def validar(self) -> bool:
        """Lógica de validación específica por tipo de documento."""
        pass

    @abstractmethod
    def obtener_lineas(self) -> List[dict]:
        """Retorna las líneas del documento."""
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__} {self.numero}"


class Factura(DocumentoFiscal):
    """Factura con IVA y retención."""

    def __init__(
        self,
        numero: str,
        fecha: date,
        total: Decimal,
        estado: str = "draft",
        iva: Decimal = Decimal("0.00"),
        retencion: Decimal = Decimal("0.00"),
        lineas: List[dict] = None
    ):
        super().__init__(numero, fecha, total, estado)
        self.iva = iva
        self.retencion = retencion
        self.lineas = lineas if lineas is not None else []

    def validar(self) -> bool:
        """Factura válida si tiene número y total > 0."""
        return bool(self.numero) and self.total > 0

    def obtener_lineas(self) -> List[dict]:
        """Devuelve las líneas de la factura."""
        return self.lineas


class Ticket(DocumentoFiscal):
    """Ticket de venta simplificado."""

    def validar(self) -> bool:
        """Ticket válido si tiene número y total > 0."""
        return bool(self.numero) and self.total > 0

    def obtener_lineas(self) -> List[dict]:
        """Por ahora retorna lista vacía."""
        return []


class Abono(DocumentoFiscal):
    """Nota de crédito / abono."""

    def __init__(
        self,
        numero: str,
        fecha: date,
        total: Decimal,
        estado: str = "draft",
        factura_original: Optional[str] = None
    ):
        super().__init__(numero, fecha, total, estado)
        self.factura_original = factura_original

    def validar(self) -> bool:
        """Abono válido si tiene número, total < 0 y referencia a factura."""
        return bool(self.numero) and self.total < 0 and bool(self.factura_original)

    def obtener_lineas(self) -> List[dict]:
        """Por ahora retorna lista vacía."""
        return []

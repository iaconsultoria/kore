from abc import ABC, abstractmethod
from typing import Dict, Any


class ExtractorOCR(ABC):
    """
    Interfaz abstracta para extractores OCR de documentos fiscales.

    Define el contrato: imagen → diccionario con datos extraídos.
    Permite cambiar Google → OpenAI sin modificar vistas ni servicios.
    """

    @abstractmethod
    def extraer(self, imagen_bytes: bytes) -> Dict[str, Any]:
        """
        Extrae datos de una imagen de documento fiscal.

        Args:
            imagen_bytes: contenido binario de PDF, JPG o PNG

        Returns:
            dict con claves: numero, fecha, total, proveedor, lineas, etc.
            Si falla: dict con claves 'extraccion_fallida' y 'error'
        """
        pass

    @abstractmethod
    def obtener_confianza(self) -> float:
        """
        Retorna confianza de la última extracción (0.0 - 1.0).

        Útil para decidir si necesita revisión manual.
        """
        pass

    @abstractmethod
    def obtener_modelo(self) -> str:
        """Retorna el nombre del modelo usado (ej: 'google/gemma-4', 'openai/gpt-4-vision')."""
        pass

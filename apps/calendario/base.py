from abc import ABC, abstractmethod
from datetime import date, time


class EventoTemporal(ABC):
    """Clase base abstracta para cualquier cosa que ocupe un hueco en el tiempo."""

    def __init__(self, titulo: str, inicio: date, fin: date):
        self.titulo = titulo
        self.inicio = inicio
        self.fin = fin

    def duracion_dias(self) -> int:
        return (self.fin - self.inicio).days + 1

    @abstractmethod
    def describir(self) -> str:
        """Descripción legible del evento."""
        ...


class EventoConHora(EventoTemporal):
    """Evento que además tiene hora de inicio y fin."""

    def __init__(self, titulo, inicio, fin, hora_inicio: time = None, hora_fin: time = None):
        super().__init__(titulo, inicio, fin)
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin

    def describir(self) -> str:
        hora = f" a las {self.hora_inicio}" if self.hora_inicio else ""
        return f"{self.titulo} — {self.inicio}{hora}"
from abc import ABC, abstractmethod


class ParserVozInterface(ABC):
    """Interfaz que debe cumplir cualquier parser de texto a cita."""

    @abstractmethod
    def parsear(self, texto: str) -> dict:
        """
        Recibe texto libre y devuelve un dict con los campos de la cita
        o {"clarificacion_necesaria": "..."} si falta información.
        """
        ...
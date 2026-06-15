# Arquitectura orientada a objetos — App Calendario
 
## Decisiones de diseño
 
### 1. Jerarquía: clase base abstracta `EventoTemporal`
 
**Problema:** `Cita`, `Recordatorio` y un futuro `Bloqueo` comparten los mismos campos base — todos ocupan un hueco en el tiempo con `titulo`, `inicio` y `fin`. Tenerlos como modelos planos e independientes duplica lógica y hace difícil tratar varios tipos de evento de forma uniforme.
 
**Decisión:** Crear `EventoTemporal` en `apps/calendario/base.py` como clase base abstracta (`ABC`) con los campos comunes y un método abstracto `describir()` que cada subclase implementa a su manera.
 
```
EventoTemporal (ABC)
├── EventoConHora       ← citas con hora_inicio y hora_fin
│   └── Cita            ← modelo Django
└── Bloqueo             ← futuro: bloques de trabajo sin reunión
```
 
**Por qué ABC y no solo herencia normal:** forzar `describir()` como abstracto garantiza que cualquier subclase futura implemente su propia descripción. Si no lo implementa, Python lanza un error al instanciarla — no en tiempo de ejecución cuando ya es tarde.
 
---
 
### 2. Interfaz: `ParserVozInterface`
 
**Decisión:** Definir `ParserVozInterface` en `apps/calendario/interfaces.py` con un único método abstracto `parsear(texto: str) -> dict`. La implementación actual (`ParserVoz`) hereda de ella y envuelve la función existente.
 
```python
class ParserVozInterface(ABC):
    @abstractmethod
    def parsear(self, texto: str) -> dict: ...
 
class ParserVoz(ParserVozInterface):          # implementación actual
    def parsear(self, texto: str) -> dict:
        return parsear_texto_a_cita(texto)
 
# Futuro: class ParserVozWhisperLocal(ParserVozInterface): ...
```


 
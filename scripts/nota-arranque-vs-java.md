# Arranque de Kore (Django) vs Ejecutable Java

## Django (Kore actual)

Ventajas:
- Sin compilación: El código Python se interpreta directamente
- Sin empaquetamiento: No necesitas generar .jar ni .exe
- Rápido de desarrollar: Cambios se ven sin reiniciar (hot reload)
- Simple: Un script .ps1 basta para arrancar

Flujo de arranque:

Activar venv
Migrar BD (si hay cambios en modelos)
python manage.py runserver


Tiempo: ~3 segundos hasta que esté disponible

## Ejecutable Java equivalente

Cómo sería:

1. Compilación: javac -> .class files
2. Empaquetamiento: Maven/Gradle -> .jar (50-200 MB)
3. Ejecución: java -jar kore.jar

Ventajas de Java:
- Rendimiento (compilado a bytecode)
- Distribución: Un .jar es todo
- Portabilidad: Corre igual en cualquier máquina con JVM

Desventajas frente a Django:
- Tiempos de construcción más largos (minutos)
- Mayor complejidad (Maven, dependencias, plugins)
- Overhead de la JVM (mayor consumo de RAM)
- Menos flexible en desarrollo (recompilación necesaria)

## Por qué Django es mejor para Kore

- Equipo pequeño: No necesita compilación
- Desarrollo ágil: Cambios sin recompilar
- Gestión de dependencias simple: pip install
- Prototipado rápido: Perfecto para MVP y evolución

Si mañana necesitas distribución en producción, puedes:
- Usar Docker (containerizar la app)
- Deployar en Heroku/Railway/PythonAnywhere
- O generar un .exe con PyInstaller (si realmente lo necesitas)

Pero no necesitas Java para esto.

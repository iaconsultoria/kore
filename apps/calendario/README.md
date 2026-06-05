# App: Calendario

## Qué hace la app

`apps.calendario` permite gestionar citas  desde una interfaz web en Django. El usuario puede crear citas, manualmente o dictarlas en lenguaje natural mediante un parser de texto libre que extrae fecha, hora y título de forma automática. También puede editarlas y borrarlas. 
Las citas se organizan por categorías con color y prioridad configurables.

---

## Modelos principales

### `Categoria`
Agrupa las citas por tipo (p. ej. "Cliente", "Interno", "Personal"). Cada categoría tiene un color hexadecimal para identificarla visualmente en el calendario, una prioridad numérica y una política de reprogramación (`rigida` / `flexible` / `cancelar si no hay hueco`) que indica si las citas de ese tipo pueden moverse con facilidad.

### `Cita`
Representa un evento concreto en el tiempo. Almacena título, fecha de inicio y fin, hora de inicio y fin opcional, categoría asociada, repetir, ubicación, anotaciones y prioridad propia. Es el núcleo de la app: todo el parser, las vistas y la API giran en torno a este modelo.

---

## Cómo usar el parser de texto libre

La vista `cita_desde_texto` acepta una frase en español mediante POST y devuelve un formulario pre-rellenado con los campos que ha podido extraer.

### Frases que entiende

| Frase de entrada | Extrae |
|---|---|
| `"Reunión el lunes a las 10"` | título: *Reunión*, día: próximo lunes, hora: 10:00 |
| `"Llamada con cliente el martes a las 15:30"` | título: *Llamada con cliente*, día: próximo martes, hora: 15:30 |
| `"Cita el 12/07 a las 9"` | título: *Cita*, fecha: 12/07 del año en curso, hora: 09:00 |
| `"Revisión el viernes"` | título: *Revisión*, día: próximo viernes, hora: sin rellenar |

### Frases que **no** entiende (aún)

| Frase de entrada | Problema |
|---|---|
| `"Mañana por la tarde"` | "mañana" y "por la tarde" sin especificar hora no lo entiende |
| `"El 2 de agosto"` | formato "día de mes" en texto no está implementado |
| `"En dos semanas"` | expresiones relativas de semanas, no se resuelven excepto que escribas el día específico |
| `"Next Monday at 3pm"` | solo procesa frases en español |
| `"Reunión a mediodía"` | horas coloquiales (`mediodía`, `medianoche`) no reconocidas |

El parser rellena lo que puede y deja el resto del formulario en blanco para que el usuario lo complete o edite a su gusto.

---

## Limitación conocida: entrada de voz

La funcionalidad de entrada de voz depende de la Web Speech API de Google, cuyo endpoint está **bloqueado por las restricciones de red del entorno de desarrollo** actual.

**Síntoma:** el botón de micrófono no responde o lanza un error de red silencioso en el navegador.

**Solución prevista en S4:** migrar el reconocimiento de voz a un servicio dentro del servidor, eliminando la dependencia de los servidores de Google.
# Informe ASG — Kore 2026

## A — Ambiental

### Contexto de despliegue

Kore es una aplicación Django orientada a autónomos que corre en local en la máquina del propio cliente. No hay servidor centralizado en la nube — cada instalación es independiente. Esto tiene implicaciones directas en la huella de cómputo.

---

### Modelos de IA en uso

| Módulo | Modelo | Dónde corre |
|---|---|---|
| Transcripción de voz (calendario) | `faster-whisper small` | Local (CPU del cliente) |
| Parser de texto a cita (calendario) | `z-ai/glm-4.5-air:free` vía OpenRouter | Nube (servidores del proveedor) |
| Sugerencia de categoría (facturas) | `google/gemma-4-31b-it:free` vía OpenRouter | Nube (servidores de Google) |
| Extracción de facturas (facturas) | LiteLLM + OpenRouter | Nube |

---

### Huella de cómputo

**Modelos locales (`faster-whisper small`)**

`faster-whisper small` tiene ~244M de parámetros y corre en CPU. En un ordenador de oficina estándar consume entre 1-2W adicionales durante la transcripción, que dura típicamente 2-5 segundos por audio. La huella por uso es marginal — comparable a abrir una pestaña del navegador.

No requiere GPU ni hardware especializado, lo que lo hace adecuado para el perfil de cliente objetivo (autónomo con portátil de oficina).

**Modelos en nube (OpenRouter)**

Las llamadas a `z-ai/glm-4.5-air:free` y `google/gemma-4-31b-it:free` delegan el cómputo a los servidores de los proveedores. Kore no tiene control directo sobre la huella energética de esas infraestructuras.

Sin embargo, ambos modelos se usan bajo demanda y solo cuando el usuario interactúa activamente — no hay inferencia en background ni polling periódico. El número de llamadas por sesión es bajo (1-3 llamadas por cita creada).

**Estimación de huella por sesión de uso**

Una sesión típica (crear 3-5 citas vía voz) genera:
- 3-5 transcripciones locales con Whisper: ~5-10 segundos de CPU adicional
- 3-5 llamadas a OpenRouter: tráfico de red de ~5-10 KB por llamada

La huella dominante es la del ordenador encendido durante la sesión, no el uso de IA.

---

### Modelos locales vs nube

| Criterio | Local (`faster-whisper`) | Nube (OpenRouter) |
|---|---|---|
| Control de huella | Alto — corre en el hardware del cliente | Bajo — depende del proveedor |
| Eficiencia energética | Depende del hardware del cliente | Los proveedores suelen usar datacenters optimizados |
| Privacidad de datos | Alta — el audio no sale del dispositivo | El texto transcrito se envía al proveedor |
| Disponibilidad offline | Sí | No |

---

### Decisiones de diseño con impacto ambiental

1. **`faster-whisper` en lugar de Whisper API de OpenAI** — se eligió el modelo local precisamente para evitar enviar audio a servidores externos. Beneficio ambiental secundario: elimina una llamada de red por transcripción.

2. **Modelos gratuitos en OpenRouter** — los modelos `free` de OpenRouter son modelos grandes que ya están desplegados para otros usuarios. Kore no genera demanda adicional de infraestructura — se aprovecha capacidad existente.

3. **Sin inferencia en background** — La IA solo se activa cuando el usuario lo solicita explícitamente.

---

### Áreas de mejora

- **Parser offline** — el parser de texto a cita depende de OpenRouter. Un modelo local pequeño (tipo `phi-3-mini` o `llama-3.2-1b`) podría reemplazarlo para uso offline con huella mínima.

## S — Social
 
### Accesibilidad
 
La interfaz de Kore no tiene implementación específica de accesibilidad en este momento. La navegación se realiza con el dispositivo señalador estándar (ratón o touchpad).
 
La entrada por voz — aunque diseñada inicialmente como comodidad — tiene un efecto inclusivo secundario: permite crear citas y gestionar la agenda sin escribir, lo que reduce la barrera de uso para personas con dificultades motoras finas, dislexia o baja velocidad de escritura.
 
**Áreas pendientes de accesibilidad:**
- No se ha verificado el contraste de colores según WCAG 2.1
- No hay etiquetas ARIA en los componentes HTMX
- Los mensajes de error del formulario no están asociados a sus campos con `aria-describedby`
---
 
### La voz como inclusión
 
El flujo de voz → transcripción → cita reduce el número de pasos para crear una cita de ~10 campos manuales a una frase hablada. Esto tiene impacto directo en la velocidad de adopción para usuarios no técnicos.
 
Un autónomo que no está acostumbrado a software de gestión puede decir "reunión con el cliente el viernes a las 10" en lugar de rellenar un formulario. La curva de aprendizaje baja significativamente.
 
La transcripción ocurre en local con `faster-whisper` — el audio no sale del dispositivo del usuario. Esto es relevante desde el punto de vista de la privacidad, especialmente para autónomos que gestionan información confidencial de clientes.
 
---
 
### Impacto en autónomos y pymes
 
Kore cubre dos necesidades que los autónomos gestionan habitualmente con herramientas dispersas (agenda de papel, email, Excel):
 
**Calendario inteligente**
- Creación de citas por voz o texto libre
- Detección automática de sobrecarga diaria
- Sugerencia de reprogramación cuando el día está saturado
Sin Kore, un autónomo detecta la sobrecarga cuando ya tiene conflictos de agenda. Con Kore, el sistema lo avisa antes y propone una solución.
 
**Gestión de facturas**
- Extracción automática de datos desde PDF o imagen
- Alertas de vencimiento — avisa el mes en el que va a a expirar la factura
- Dashboard fiscal con resumen de IVA y gastos por categoría
El impacto más directo es en el tiempo dedicado a tareas administrativas: leer facturas, recordar fechas de vencimiento y clasificar gastos son tareas repetitivas que Kore automatiza parcialmente.
 
**Perfil de usuario objetivo:** autónomo o pequeña empresa sin departamento administrativo, que gestiona su agenda y contabilidad básica sin software especializado.

## G — Gobernanza

### Privacidad de datos

Kore adopta un modelo de **privacidad por diseño**: todos los datos del usuario —citas, facturas y documentos adjuntos— se almacenan exclusivamente en la máquina local del cliente. No existe sincronización con servidores externos ni transferencia de datos a terceros.

- No se recopilan datos de uso de forma remota.
- Las facturas procesadas por la IA no salen del dispositivo del usuario.
- Los modelos de IA que operan en local (faster-whisper, GLM-4.5) no envían audio ni texto a servidores propios de Kore.
- Los modelos en nube (OpenRouter) reciben únicamente el texto o imagen necesario para la consulta puntual, sin persistencia en los servidores del proveedor más allá de lo estipulado en sus condiciones de uso.

### Roles de acceso

Kore implementa un sistema de control de acceso basado en grupos:

| Rol | Descripción |
|-----|-------------|
| Administrador | Acceso completo. Puede crear usuarios, definir grupos y configurar permisos. |
| Usuario de grupo | Acceso limitado según los permisos asignados al grupo al que pertenece. |

Este modelo permite adaptar Kore a entornos con varios trabajadores (por ejemplo, una pequeña empresa o despacho), manteniendo el control centralizado en el administrador.

### Open Core y transparencia

Kore es un proyecto **completamente open source**. Esto implica:

- El código fuente es auditable por cualquier persona, lo que permite verificar el tratamiento de los datos y el comportamiento de la IA.
- La comunidad puede contribuir mejoras, detectar vulnerabilidades y proponer cambios.
- No existe una capa privada de funcionalidades ocultas.

La transparencia del código es, en sí misma, una garantía de gobernanza: cualquier usuario técnico puede verificar que los datos no salen del dispositivo.

### Transparencia de la IA

Kore informa al usuario de qué modelo está procesando cada tarea:

- **faster-whisper small** — transcripción de voz (local)
- **z-ai/glm-4.5-air:free** — asistente del calendario (nube, OpenRouter)
- **openrouter/google/gemma-4-31b-it:free** — procesamiento de facturas (nube, OpenRouter)

Los modelos en nube son gratuitos y de terceros; su política de datos está sujeta a las condiciones de OpenRouter y de los proveedores respectivos, lo que constituye un área de mejora futura: evaluar modelos locales equivalentes para eliminar cualquier dependencia externa.

### Grupos de interés

| Grupo de interés | Relación con Kore |
|-----------------|-------------------|
| Autónomos y pymes | Usuario principal. Se benefician de la automatización de tareas administrativas. |
| Desarrolladores / comunidad open source | Contribuyen al código y a la detección de vulnerabilidades. |
| Proveedores de IA (OpenRouter, Google, ZhipuAI) | Suministran modelos en nube. Su política de datos afecta indirectamente al usuario final. |
| Reguladores (AEPD, RGPD) | Marco legal aplicable al tratamiento de datos personales y facturas. |

### Tabla de métricas de gobernanza

| Métrica | Estado actual |
|---------|--------------|
| Datos almacenados en local | ✅ Sí |
| Sincronización con servidores propios | ✅ No |
| Control de acceso por roles | ✅ Implementado (admin + grupos) |
| Código open source | ✅ 100% |
| Auditoría de dependencias de IA externas | OpenRouter no retiene prompts por defecto, pero los proveedores downstream (ZhipuAI, Google) tienen sus propias políticas no verificadas. Recomendación: revisar políticas de ZDR para los modelos usados, o sustituirlos por modelos locales a largo plazo. |
| Política de retención de datos documentada | Los datos se eliminan al borrar el servidor local. No existe persistencia externa. |
| Cumplimiento RGPD documentado | ⚠️ Pendiente |

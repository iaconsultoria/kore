# Plan macro — FFOE Kore (24 jornadas)

**Período:** L 18/05/2026 → J 18/06/2026 · L-V · 9:00-15:00 · 144h brutas · ~120h efectivas
**Modalidad:** teletrabajo total · check-in escrito por chat 9:00-9:15 + pings intermitentes durante el horario · **sin videollamadas**
**Estructura del día:** 9:00 check-in chat · 9:15-11:30 bloque 1 · 11:30-12:00 pausa · 12:00-14:30 bloque 2 · 14:30-15:00 cierre + diario

---

## Mapeo a calendario real

| Sem | Días | Fechas | Bloque |
|-----|------|--------|--------|
| S1  | 5  | L 18 - V 22 mayo  | Núcleo común (JUNTOS) |
| S2  | 5  | L 25 - V 29 mayo  | Apps individuales (SEPARADOS) |
| S3  | 5  | L 1 - V 5 junio   | Pulido + inteligencia IA (SEPARADOS) |
| S4  | 5  | L 8 - V 12 junio  | Integración + sostenibilidad ASG (JUNTOS) |
| S5  | 4  | L 15 - J 18 junio | Hackeo cruzado + cierre (JUNTOS) |

Son **5 semanas** (no 4) — aprovechamos los 4 días extra para ASG, PRL y hackeo cruzado sin prisa.

---

## Semana 1 — Núcleo común (L 18 - V 22 mayo)

Entregable: repo `kore` con proyecto Django mínimo: auth, tenant, dashboard vacío, manifiesto, primera app "hola-mundo" cargada.

| Día | Tema | RA cubiertos |
|-----|------|--------------|
| L 18 | Setup, Git, GitHub, intro Kore, tablero Kanban | Entornos Desarrollo RA1.b, RA1.g, RA2.a · Sist Inf RA4.h |
| M 19 | Django básico + admin + primer modelo + migración | Programación RA9.a/c · BD RA4 · Entornos Des RA2.e |
| X 20 | Multi-tenant: modelo Tenant + middleware /e/{slug}/ | Programación RA7.a/b (herencia, composición) · BD RA6 |
| J 21 | Auth Django + Perfil + autorización por tenant | Programación RA7 · Lenguajes Marcas RA7.f (acceso seguro) |
| V 22 | Dashboard vacío + manifiesto.toml + app hola-mundo + **registro semanal 14:00** | Programación RA7.h/i · Digitalización RA1 |

Detalle día a día en [`02-semana-1-detalle.md`](02-semana-1-detalle.md).

---

## Semana 2 — Apps individuales, esqueleto (L 25 - V 29 mayo)

| Alumno | App | Entregable |
|--------|-----|------------|
| Cecilia | Calendario IA con voz | CRUD citas, categorías configurables, vista semana/día, voz→texto→cita básica |
| Manuel | OCR facturas → Excel | Subir PDF, OCR vía LiteLLM vision, extraer 6-8 campos, exportar Excel |

RA cubiertos en S2 (ambos):
- **Programación RA7** (POO avanzada: jerarquías de modelos Django)
- **Programación RA8/9** (persistencia + CRUD BD)
- **BD RA4/RA6** (normalización y modificación)
- **Sistemas Informáticos RA7.g** (herramientas propósito general)

Detalle día a día en los repos privados `plan-cecilia` y `plan-manuel`.

**V 29, 14:00**: registro semanal interno de Carmen.

---

## Semana 3 — Inteligencia IA + RAG (L 1 - V 5 junio)

| Alumno | Avance |
|--------|--------|
| Cecilia | Detección sobrecarga del día, reprogramación inteligente, resumen IA día/semana. Embeddings + pgvector sobre histórico de citas. Sincronización con sistema externo (Nextcloud/Radicale CalDAV). |
| Manuel | RAG normativa AEAT básica (clasificar gasto, IVA deducible). Validación datos extraídos. Manejo errores OCR (factura borrosa). Integración con Odoo Community o ERPNext. |

RA cubiertos en S3:
- **Programación RA8** (BD orientadas a objetos — pgvector encaja como BD vectorial/objetos)
- **Lenguajes Marcas RA7.a/b/c/d/e/g/h/i** (sistemas empresariales gestión) — **Manuel clavado**
- **Digitalización RA1/RA6** (proyecto transformación digital — caso de uso AEAT)

**V 5, 14:00**: registro semanal interno + decisión sobre rumbo S4.

---

## Semana 4 — Integración + Sostenibilidad ASG (L 8 - V 12 junio)

| Día | Tema | RA |
|-----|------|----|
| L 8 | Comunicación entre apps vía MCP/eventos | Programación RA7 · Lenguajes Marcas RA7.h |
| M 9 | Caso estrella end-to-end: factura → vencimiento → evento calendario | Digitalización RA6.e |
| X 10 | Tests + documentación final | Sist Inf RA7.g |
| J 11 | **PRL Manuel** (mañana, autoestudio guiado por chat) + Sostenibilidad ASG arranque (tarde, ambos) | **Empleabilidad RA2** (Manuel) · **Sostenibilidad RA6.a/b** (ambos) |
| V 12 | Informe ASG del proyecto Kore (entregable conjunto) + retro + registro semanal | **Sostenibilidad RA6.c/d/e** (informe completo) |

Entregable transversal: **informe de sostenibilidad ASG** del proyecto Kore, firmado por ambos alumnos. Cubre el módulo entero de Sostenibilidad.

PRL Manuel: detalle en su repo privado `plan-manuel/prl-sesion.md`. Se hace en autoestudio guiado por chat, sin videollamada.

---

## Semana 5 — Hackeo cruzado + cierre (L 15 - J 18 junio)

| Día | Tema |
|-----|------|
| L 15 | **Código congelado V12.** Cada uno lee y entiende el código del otro. Toma de notas. |
| M 16 | Hackeo cruzado fase 1: cada uno ataca el código del otro, documenta vulnerabilidades en `hackeo/VULN-XX.md` |
| X 17 | Hackeo cruzado fase 2: defensa, mitigación, propuesta de parche |
| J 18 | **Cierre FFOE**: README definitivo + retrospectiva escrita + entregables finales subidos. |

Reglas en [`04-hackeo-cruzado-reglas.md`](04-hackeo-cruzado-reglas.md).

---

## Seguimiento — qué se hace cada cuándo

| Cadencia | Quién | Qué |
|---|---|---|
| 9:00-9:15 diario | cada alumno | check-in escrito por chat: qué va a hacer hoy, dudas pendientes |
| Durante la jornada | Carmen | pings intermitentes. Si el alumno no responde en horario, queda anotado en registro semanal |
| 14:30-15:00 diario | cada alumno | diario del día en su repo privado |
| Antes del check-in siguiente | Carmen | review del diario del alumno con comentarios en GitHub |
| **Viernes 14:00** | Carmen | **registro semanal** interno (progreso, RA cubiertos, incidencias) |
| Cuando alguien se atasca > 1h | el alumno | mensaje detallado por chat con captura/pegado de error. Carmen responde por chat o con commit de ejemplo |
| J 11/06 mañana | Manuel + Carmen por chat | PRL en autoestudio guiado |
| J 18/06 | todos | cierre FFOE escrito |

---

## Riesgos a vigilar

- **Teletrabajo + alumnos jóvenes**: protocolo de seguimiento documental fuerte (check-in + pings + diario diario). Sin videollamadas, todo el seguimiento es por chat + revisión de commits/PRs/diarios.
- **Manuel va más cargado** (OCR + PRL). Si ve apretado, dejar el ERP para S3 y quedarse en S2 solo con Excel.
- **AEAT en S3**: normativa real densa. Limitar a 3-4 conceptos (IVA deducible, clasificación gasto, modelo 303, plazos pago). No exhaustivo.
- **Hackeo cruzado**: vigilar el tono. Si uno se lo toma mal, reconvertir a colaborativo.

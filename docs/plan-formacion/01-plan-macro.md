# Plan macro — FFOE Kore (24 jornadas)

**Período:** L 18/05/2026 → J 18/06/2026 · L-V · 8:00-14:00 · 144h brutas · ~120h efectivas
**Modalidad:** teletrabajo total · check-in escrito por chat 8:00-8:15 + pings intermitentes durante el horario
**Estructura del día:** 8:00 check-in chat · 8:15-10:30 bloque 1 · 10:30-11:00 pausa · 11:00-13:30 bloque 2 · 13:30-14:00 cierre + diario

---

## Mapeo a calendario real

| Sem | Días | Fechas | Bloque |
|-----|------|--------|--------|
| S1  | 5  | L 18 - V 22 mayo  | Núcleo común (JUNTOS) |
| S2  | 5  | L 25 - V 29 mayo  | Apps individuales (SEPARADOS) |
| S3  | 5  | L 1 - V 5 junio   | Pulido + inteligencia IA (SEPARADOS) |
| S4  | 5  | L 8 - V 12 junio  | Integración + sostenibilidad ASG (JUNTOS) |
| S5  | 4  | L 15 - J 18 junio | Hackeo cruzado + demo final (JUNTOS) |

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
| V 22 | Dashboard vacío + manifiesto.toml + app hola-mundo + **informe semanal 13:00** | Programación RA7.h/i · Digitalización RA1 |

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

**V 29, 13:00**: informe semanal Carmen → Javier.

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

**V 5, 13:00**: informe semanal a Javier + decisión sobre rumbo S4.

---

## Semana 4 — Integración + Sostenibilidad ASG (L 8 - V 12 junio)

| Día | Tema | RA |
|-----|------|----|
| L 8 | Comunicación entre apps vía MCP/eventos | Programación RA7 · Lenguajes Marcas RA7.h |
| M 9 | Caso estrella end-to-end: factura → vencimiento → evento calendario | Digitalización RA6.e |
| X 10 | Tests + documentación final | Sist Inf RA7.g |
| J 11 | **Sesión PRL Manuel** (mañana) + Sostenibilidad ASG arranque (tarde, ambos) | **Empleabilidad RA2** (Manuel) · **Sostenibilidad RA6.a/b** (ambos) |
| V 12 | Informe ASG del proyecto Kore (entregable conjunto) + retro + informe semanal | **Sostenibilidad RA6.c/d/e** (informe completo) |

Entregable transversal: **informe de sostenibilidad ASG** del proyecto Kore, firmado por ambos alumnos. Cubre el módulo entero de Sostenibilidad.

Sesión PRL Manuel: detalle en su repo privado `plan-manuel/prl-sesion.md`.

---

## Semana 5 — Hackeo cruzado + demo final (L 15 - J 18 junio)

| Día | Tema |
|-----|------|
| L 15 | **Código congelado V12.** Cada uno lee y entiende el código del otro. Toma de notas. |
| M 16 | Hackeo cruzado fase 1: cada uno ataca el código del otro, documenta vulnerabilidades en `hackeo/VULN-XX.md` |
| X 17 | Hackeo cruzado fase 2: defensa, mitigación, propuesta de parche |
| J 18 | **Demo final** (video grabado o sesión en directo si encaja): README definitivo + retrospectiva. **Cierre FFOE.** Email final a Javier con todo el material. |

Reglas en [`04-hackeo-cruzado-reglas.md`](04-hackeo-cruzado-reglas.md).

---

## Seguimiento — qué se hace cada cuándo

| Cadencia | Quién | Qué |
|---|---|---|
| 8:00-8:15 diario | cada alumno | check-in escrito por chat: qué va a hacer hoy, dudas pendientes |
| Durante la jornada | Carmen | pings intermitentes. Si el alumno no responde en horario, queda anotado en informe semanal |
| 13:30-14:00 diario | cada alumno | diario del día en su repo privado |
| Antes del check-in siguiente | Carmen | review del diario del alumno con comentarios |
| **Viernes 13:00** | Carmen | **informe semanal** consolidado a Javier (progreso, RA cubiertos, incidencias) |
| Cuando alguien se atasca > 1h | quien sea | screen-share urgente |
| J 11/06 mañana | Carmen + Manuel | sesión PRL específica |
| J 18/06 | todos | demo final + cierre |

---

## Riesgos a vigilar

- **Teletrabajo + alumnos jóvenes**: protocolo de seguimiento fuerte (check-in + pings + diario diario). Sin demos formales en directo cada viernes, pero seguimiento documental constante.
- **Manuel va más cargado** (OCR + PRL). Si ve apretado, dejar el ERP para S3 y quedarse en S2 solo con Excel.
- **AEAT en S3**: normativa real densa. Limitar a 3-4 conceptos (IVA deducible, clasificación gasto, modelo 303, plazos pago). No exhaustivo.
- **Hackeo cruzado**: vigilar el tono. Si uno se lo toma mal, reconvertir a colaborativo.
- **Tutor del centro**: si Javier pide ajustes al plan, plan B = ajustar lo que él pida sin tirar lo hecho.

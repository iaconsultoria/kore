# Mapeo de actividades del curso a Resultados de Aprendizaje (Anexo I)

Documento de referencia interno (tutora dual de empresa). Demuestra que el plan cubre todos los RA del Anexo I del convenio.

**Convenio**: 110022372025020 · **Ciclo**: 1º DAM · **Alumnos**: Manuel Aparicio Doeste y Cecilia Serrano Martín.

---

## Módulo: Bases de Datos

### RA6 — Diseña modelos relacionales normalizados interpretando diagramas entidad/relación
**g) Se han aplicado reglas de normalización.**

- **Cubierto en**: S1 X 20 (modelo Tenant) + S2 ambos (diseñar BD de su app: citas/categorías o facturas/líneas/proveedores) + S3 Manuel (estructura tabla normativa AEAT).
- **Evidencia**: diagramas E/R en `/docs/bd/` de cada app + commits de migraciones.

### RA4 — Modifica la información almacenada en la base de datos utilizando asistentes, herramientas gráficas y el lenguaje de manipulación de datos
**h) Se han adoptado medidas para mantener la integridad y consistencia de la información.**

- **Cubierto en**: S1 M 19 (admin Django como herramienta gráfica) + S2 (formularios CRUD) + S3 (transacciones atómicas).
- **Evidencia**: uso de `@transaction.atomic`, constraints en migraciones, validators.

---

## Módulo: Digitalización Aplicada a los Sectores Productivos GS

### RA1 — Analiza el concepto de digitalización y su repercusión en los sectores productivos
**g) Se han analizado las ventajas de digitalizar una empresa industrial de extremo a extremo.**

- **Cubierto en**: S1 L 18 (charla inicial sobre Kore y digitalización del autónomo) + sección "Análisis de transformación digital del autónomo español" en README de `kore`.
- **Evidencia**: documento `/docs/digitalizacion/analisis-end-to-end.md`.

### RA6 — Desarrolla un proyecto de transformación digital de una empresa de un sector relacionado con el título
**e) Se han tenido en cuenta las necesidades presentes y futuras de la empresa.**

- **Cubierto en**: el propio proyecto Kore ES un proyecto de transformación digital. Caso de uso S4: factura escaneada → vencimiento automático en calendario → recordatorio IA.
- **Evidencia**: caso estrella S4 funcionando + documentación de necesidades en `/docs/digitalizacion/`.

---

## Módulo: Sistemas Informáticos

### RA7 — Elabora documentación valorando y utilizando aplicaciones informáticas de propósito general
**g) Se han utilizado herramientas de propósito general.**

- **Cubierto en**: README, diarios en repos privados, documentación generada con MkDocs, diagramas con Mermaid, informe ASG en S4.
- **Evidencia**: README + `/docs/` con MkDocs.

### RA4 — Gestiona sistemas operativos utilizando comandos y herramientas gráficas
**h) Se han evaluado las necesidades del sistema informático en relación con el desarrollo de aplicaciones.**

- **Cubierto en**: S1 L 18 setup (Python, venv, WSL/Linux, PostgreSQL local, git) — cada alumno evalúa qué necesita su máquina.
- **Evidencia**: `docs/setup/requisitos-sistema.md` escrito por cada alumno.

---

## Módulo: Entornos de Desarrollo

### RA1 — Reconoce los elementos y herramientas que intervienen en el desarrollo de un programa informático
**b) Se han clasificado los lenguajes de programación, identificando sus características.**

- **Cubierto en**: S1 L 18 charla "Python interpretado vs Java/C++ compilados, dinámico vs estático, tipado dual, ecosistema web".
- **Evidencia**: nota en diario de cada alumno comparando Python con Java.

**g) Se han identificado las características y escenarios de uso de las metodologías ágiles de desarrollo de software.**

- **Cubierto en**: S1 L 18 introducción a Kanban + uso de tablero de GitHub Projects todo el mes (columnas Pendiente/En curso/Revisión/Hecho).
- **Evidencia**: tablero Kanban con historial de movimientos.

### RA2 — Evalúa entornos integrados de desarrollo
**a) Se han instalado entornos de desarrollo, propietarios y libres.**

- **Cubierto en**: S1 L 18: VS Code (libre) + extensiones Python, GitLens, Django.
- **Evidencia**: pantallazos en diario.

**e) Se han generado ejecutables a partir de código fuente de diferentes lenguajes en un mismo entorno de desarrollo.**

- **Cubierto en**: `python manage.py runserver`, `manage.py migrate`, generación de migraciones, build de assets, creación de un `entrypoint` ejecutable. Comparar con compilación de un proyecto Java.
- **Evidencia**: scripts en `/scripts/` y diario.

---

## Módulo: Sostenibilidad Aplicada al Sistema Productivo

### RA6 — Analiza un plan de sostenibilidad de una empresa del sector

**a) Se han identificado los principales grupos de interés de la empresa.**
- Cubierto en S4 J 11. Grupos: autónomos usuarios, alumnos en formación, socios asociación, comunidad open source, AEAT, proveedores de IA.

**b) Se han analizado los aspectos ASG materiales, las expectativas de los grupos de interés y la importancia de los aspectos ASG en relación con los objetivos empresariales.**
- A (Ambiental): consumo eléctrico inferencia IA, modelos pequeños vs grandes, hosting eficiente.
- S (Social): formación abierta, inclusión digital de autónomos sin recursos, español/L1 prioritario, accesibilidad.
- G (Gobernanza): asociación sin ánimo de lucro, open source, decisiones colegiadas, transparencia financiera.

**c) Se han definido acciones encaminadas a minimizar los impactos negativos y aprovechar las oportunidades que plantean los principales aspectos ASG identificados.**
- Acciones concretas para cada eje, redactadas en el informe.

**d) Se han determinado las métricas de evaluación del desempeño de la empresa de acuerdo con los estándares de sostenibilidad más ampliamente utilizados.**
- Métricas alineadas con GRI / ESRS resumidos. Ej: tokens IA consumidos por usuario activo, % usuarios sin coste, contribuidores externos al repo, % decisiones documentadas en gobernanza.

**e) Se ha elaborado un informe de sostenibilidad con el plan y los indicadores propuestos.**
- **Entregable explícito**: `/docs/sostenibilidad/informe-asg-kore-2026.md`, firmado por Cecilia y Manuel.

---

## Módulo: Lenguajes de Marcas y Sistemas de Gestión de Información

### RA7 — Opera sistemas empresariales de gestión de información realizando tareas de importación, integración, aseguramiento y extracción de la información

**a) Se han identificado los principales sistemas de gestión empresarial.**
- S2 lunes (ambos): charla ERP/CRM/SGE: SAP, Odoo, ERPNext, Holded, FacturaDirecta. Comparativa.

**b) Se han reconocido las ventajas de los sistemas de gestión de información empresariales.**
- Mismo bloque charla S2 L. Documentado en diario.

**c) Se han evaluado las características de las principales aplicaciones de gestión empresarial.**
- S3 Manuel evalúa Odoo Community vs ERPNext como destino de las facturas.

**d) Se han instalado aplicaciones de gestión de la información empresarial.**
- S3 Manuel instala Odoo Community o ERPNext en Docker. Cecilia instala Nextcloud Calendar o Radicale para integración.

**e) Se han configurado y administrado las aplicaciones.**
- S3 cada uno configura su sistema (usuarios, módulo facturación / calendario, conexión).

**f) Se han establecido y verificado mecanismos de acceso seguro a la información.**
- S1 J 21 (auth Django, login required) + S3 (OAuth/API key contra Odoo/Nextcloud).

**g) Se han generado informes.**
- Manuel: informe mensual de facturas extraídas en PDF/Excel. Cecilia: informe semanal de carga de agenda.

**h) Se han realizado procedimientos de extracción de información para su tratamiento e incorporación a diversos sistemas.**
- **Manuel clavado**: OCR PDF → estructura JSON → Excel y/o Odoo.

**i) Se han elaborado documentos relativos a la explotación de la aplicación.**
- Manual de usuario en `/docs/manual-usuario/` de cada app.

---

## Módulo: Programación

### RA7 — Desarrolla programas aplicando características avanzadas de los lenguajes orientados a objetos

Django + Python cubren TODO esto. Mapeo criterio a criterio:

- **a) Escenarios de utilización de la herencia y la composición** → Django models con herencia abstract + composition para mixins. Documentar en `docs/arquitectura/herencia-vs-composicion.md`.
- **b) Conceptos de herencia, superclase y subclase** → `class Cita(BaseEventoTemporizado)` etc. Diario lo explica.
- **c) Modificadores para bloquear y forzar la herencia** → `class Meta: abstract = True`, equivalente a `final` con `__init_subclass__` + ABC.
- **d) Incidencia de los constructores en la herencia** → `__init__` + `super().__init__()` en cada modelo extendido.
- **e) Sobrescritura de métodos** → `save()`, `clean()`, `__str__` sobrescritos.
- **f) Diseñar jerarquías de clases** → modelos con base `EventoCalendario` y subclases, o `Documento` y subclases `Factura`, `Ticket`, `Albaran`.
- **g) Probadas y depuradas** → tests unitarios pytest-django sobre cada jerarquía.
- **h) Escenarios de uso de interfaces** → ABC + `Protocol` de typing.
- **i) Programas que implementen jerarquías** → la propia app.
- **j) Comentar y documentar código** → docstrings + MkDocs.

### RA8 — Utiliza bases de datos orientadas a objetos

- **a) Características BD orientadas a objetos** → charla S3: ORM como capa objeto-relacional + pgvector como BD vectorial.
- **b) Aplicación en lenguajes orientados a objetos** → Django ORM ejemplifica el concepto.
- **c) Instalar sistemas gestores BD orientadas a objetos** → PostgreSQL + pgvector.
- **d) Métodos para gestión de información** → QuerySet API (`filter`, `annotate`, `aggregate`, `prefetch_related`).
- **e) Crear bases de datos y estructuras** → migraciones Django.
- **f) Programar aplicaciones que almacenen objetos** → cada app crea/guarda objetos.
- **g) Recuperar, actualizar, eliminar** → CRUD completo.
- **h) Tipos estructurados y relacionados** → ForeignKey, ManyToMany, JSONField, ArrayField.

### RA9 — Gestiona información almacenada en bases de datos relacionales

- **a) Características y métodos de acceso a SGBD** → conexión PostgreSQL desde Django, settings DATABASES.
- **b) Programar conexiones con BD** → `django.db.connection`, contextos psycopg.
- **c) Código para almacenar información** → `.create()`, `.save()`, formularios.
- **d) Código para recuperar y mostrar** → vistas + templates.
- **e) Borrados y modificaciones** → `.delete()`, `.update()`.
- **f) Aplicaciones que muestren información de BD** → toda la app.
- **g) Aplicaciones para gestionar la información** → admin Django + paneles propios.

---

## Módulo: Itinerario Personal para la Empleabilidad I — **SOLO Manuel**

### RA2 — Adquiere las competencias necesarias para el desempeño de las funciones de nivel básico en Prevención de Riesgos Laborales

**b) Clasificar y describir tipos de daños profesionales.**
- Sesión J 11 mañana. Daños del puesto desarrollador remoto: TME, fatiga visual digital, riesgo psicosocial, accidente in itinere reducido.

**c) Determinar evaluación de riesgos y técnicas de prevención y protección.**
- Evaluación de riesgos del puesto teletrabajo + propuesta de medidas (ergonomía, descansos visuales 20-20-20, pausa activa, gestión carga, ciberseguridad personal).

**d) Analizar los protocolos de actuación en caso de emergencia.**
- Protocolos: incendio doméstico, primeros auxilios, accidente trabajando solo, números de emergencia.

Plan detallado en el repo privado `plan-manuel`. Entregable: documentos en `/docs/prl/` del repo `kore` (firmados por Manuel).

---

## Resumen de evidencias por entregable

| Evidencia | Ruta en repo | Cubre |
|-----------|--------------|-------|
| Código del proyecto Kore | repo `kore` | Programación RA7/8/9, BD RA4/6, Entornos |
| Diagramas E/R de cada app | `/docs/bd/` | BD RA6.g |
| Tests pytest-django | `/tests/` | Programación RA7.g |
| MkDocs con manual usuario | `/docs/` publicado | Sist Inf RA7.g, Lenguajes RA7.i |
| Tablero Kanban GitHub Projects | online | Entornos RA1.g |
| Análisis digitalización autónomo | `/docs/digitalizacion/` | Digitalización RA1.g, RA6.e |
| Informe ASG Kore 2026 | `/docs/sostenibilidad/` | Sostenibilidad RA6 completo |
| Sistema gestión empresarial integrado | Odoo/ERPNext + integración | Lenguajes Marcas RA7 completo |
| Evaluación PRL puesto desarrollador | `/docs/prl/` (Manuel) | Empleabilidad RA2 completo |
| Documentación hackeo cruzado | `/hackeo/` | extra (no obligatorio Anexo I) |
| Diarios privados de cada alumno | repos privados `plan-cecilia` / `plan-manuel` | seguimiento tutor |

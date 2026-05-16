# Semana 1 — Núcleo común (L 18 - V 22 mayo)

**Alumnos**: Cecilia y Manuel JUNTOS. Trabajan en el mismo repo `kore`, en ramas distintas. PR del uno revisado por el otro y por la tutora.

**Nivel asumido**: 1º DAM. Saben POO (en Java), han visto BD relacional, han tocado un IDE. Python/Django les puede ser nuevo, pero no parten de cero programando.

**Modalidad**: teletrabajo total. **Sin videollamadas.** Todo por chat: check-in escrito 9:00-9:15 + pings durante el día. Cierre 14:30-15:00 (diario privado).

---

## L 18 mayo — Día 1: Setup, Git, intro Kore

### 9:00-9:15 Kick-off por chat
Carmen manda un mensaje fijado al chat con:
- Bienvenida + visión del proyecto Kore en 4 líneas.
- Cómo va a funcionar el mes: horario 9:00-15:00, check-in chat, diario diario, hackeo final.
- Reglas chat: check-in 9:00, respuesta a pings durante el horario laboral, ausencias avisadas con antelación.
- Enlace al README de su repo privado (que ya tienen que haber leído antes del lunes).
- Cada uno responde con un mensaje breve presentándose al otro.

### 9:15-11:30 Bloque 1 — Setup técnico
1. (60 min) **Setup entorno** (en paralelo cada uno en su máquina):
   - Verificar Python 3.12+, instalar si no (`python --version`).
   - WSL2 si están en Windows (recomendado, no obligatorio).
   - VS Code + extensiones: Python, Pylance, GitLens, Django, Black Formatter.
   - PostgreSQL 16 + cliente psql (instalado local).
   - Git configurado con su nombre y email.
2. (45 min) **GitHub**:
   - Aceptar invitación a la organization `iaconsultoria`.
   - Aceptar invitación al repo `kore` (público) como collaborators.
   - Cada uno acepta también su repo privado `plan-cecilia` / `plan-manuel`.
3. (30 min) **Tablero Kanban en GitHub Projects** del repo `kore`:
   - Columnas: Pendiente / En curso / Revisión / Hecho.
   - Crear las primeras 5 tarjetas del día (las del día 1).
   - **RA cubierto**: Entornos de Desarrollo RA1.g (metodologías ágiles).

### 11:30-12:00 Pausa

### 12:00-14:30 Bloque 2 — Primer commit y orientación al proyecto
1. (45 min) **Clonar `kore`** localmente, crear su rama personal:
   - `git clone https://github.com/iaconsultoria/kore.git`
   - `git checkout -b s1/d1/<su-nombre>`
2. (45 min) **Primer aporte** — fichero `equipo/<su-nombre>.md` con:
   - Quién es, qué espera del mes, su usuario GitHub.
3. (60 min) **Charla escrita "Python para alguien que sabe Java"**:
   - Tutora deja un hilo en el chat con los puntos clave:
     - Tipado dinámico vs estático, duck typing.
     - Indentación significativa.
     - Sin punto y coma, sin `public/private/protected` (convención `_` y `__`).
     - `pass` vs `{}`.
     - List comprehensions vs for clásico.
     - `pip` vs Maven/Gradle, `venv` vs nada en Java.
   - Cada alumno reacciona con preguntas. Conversación asíncrona.
   - **RA cubierto**: Entornos Desarrollo RA1.b (clasificar lenguajes).
4. Cada uno hace commit, push, abre PR, el otro revisa y comenta, la tutora mergea.

### 14:30-15:00 Cierre
- 15 min: diario privado de cada alumno (`diario/2026-05-18.md`).
- 15 min: review de la tutora en GitHub (comentarios a los PR mergeados, sugerencias para mañana).

**Criterio éxito día 1**: ambos con entorno funcionando, primer PR mergeado, tablero Kanban con tarjetas movidas.

---

## M 19 mayo — Día 2: Django básico + admin + primer modelo

### 9:00-9:15 Check-in chat
Qué hizo cada uno ayer (mirando su diario), qué entendió, qué no.

### 9:15-11:30 Bloque 1 — Crear el proyecto Django
1. (15 min) **Hilo de chat "request → URL → view → template"** (5 min) + ORM (5 min) + admin (5 min). Tutora deja diagrama (markdown / imagen).
2. (45 min) **Crear venv y Django**:
   ```bash
   python -m venv venv
   source venv/Scripts/activate   # Windows bash
   pip install django psycopg[binary] python-decouple
   pip freeze > requirements.txt
   django-admin startproject kore .
   ```
3. (60 min) **Configurar PostgreSQL** en `settings.py`:
   - Crear BD local `kore_dev`.
   - Variables de entorno `.env` (DATABASE_URL, SECRET_KEY).
   - `.env.example` versionado, `.env` en `.gitignore`.
   - Migrar `python manage.py migrate`.
   - Crear superuser.
   - **RA cubierto**: Sistemas Informáticos RA4.h + Programación RA9.a.

### 11:30-12:00 Pausa

### 12:00-14:30 Bloque 2 — Primera app Django: `nucleo`
1. (30 min) **Crear app `apps/nucleo`** con IA (Claude/ChatGPT):
   - Pedir un primer modelo `ConfiguracionGlobal` con: `nombre_instancia`, `version`, `fecha_creacion`.
   - **Cada uno lee la respuesta de la IA y subraya lo que no entiende**.
   - La tutora resuelve dudas por chat.
2. (45 min) **Migración + admin**:
   - `makemigrations`, `migrate`.
   - Registrar en admin.
   - Crear primer objeto desde admin.
3. (75 min) **Modelo Tenant** (con IA, pero con espíritu crítico):
   - Pedir un modelo `Tenant`: `nombre`, `slug` (unique), `creado_en`, `activo`.
   - Validar slug con regex.
   - Sobrescribir `__str__` y `save()` (cubre Programación RA7.e).
   - Registrar en admin.
   - Crear 2 tenants de prueba.
   - **RA cubierto**: Programación RA7.b/e/j + RA9.c · BD RA4.h, RA6.

### 14:30-15:00 Cierre
- Diario + review de la tutora.

**Criterio éxito día 2**: servidor corre, admin accesible, modelo Tenant funciona, han usado IA pero **han marcado lo que no entendían** en su diario.

---

## X 20 mayo — Día 3: Multi-tenant por subdirectorio

### 9:00-9:15 Check-in chat

### 9:15-11:30 Bloque 1 — Concepto multi-tenant + middleware
1. (30 min) **Hilo chat**: qué es multi-tenant, por qué subdirectorio `/e/<slug>/` (sencillo en dev) vs subdominio (producción). Ejemplos reales (Shopify, Slack workspaces). Discusión.
2. (90 min) **Middleware con IA**:
   - Pedir middleware que extraiga `slug` de URL y cargue `Tenant` en `request.tenant`.
   - **Línea por línea**: ¿qué hace `__init__`? ¿por qué `get_response`? ¿qué pasa si el tenant no existe?
   - Discutir: ¿404 o redirect a página de selección de tenant?
   - **RA cubierto**: Programación RA7.a + RA9.b.

### 11:30-12:00 Pausa

### 12:00-14:30 Bloque 2 — URLs anidadas + probar
1. (60 min) **URLs con prefijo `/e/<slug>/`**:
   - `kore/urls.py` con `path('e/<slug:slug>/', include('apps.nucleo.urls'))`.
   - Vista placeholder que muestra `request.tenant.nombre`.
2. (60 min) **Probar y romper**:
   - Acceder a `/e/tenant1/`, `/e/tenant2/`.
   - Acceder a `/e/inexistente/` → manejar 404.
   - **Ejercicio**: cada alumno intenta acceder al tenant del otro modificando URL. Hoy aún no hay auth, mañana se cierra la grieta.
3. Commit, PR, review cruzada.

### 14:30-15:00 Cierre
- Diario + review.

**Criterio éxito día 3**: navegan a `/e/<slug>/` correctamente, manejan 404, detectan la grieta de seguridad que se cerrará en J21.

---

## J 21 mayo — Día 4: Autenticación + Perfil + autorización

### 9:00-9:15 Check-in chat

### 9:15-11:30 Bloque 1 — Auth built-in Django
1. (30 min) **Hilo chat**: `django.contrib.auth`. Por qué no inventar. Diferencia User (auth) vs Perfil (negocio).
2. (90 min) **Implementar con IA**:
   - Vistas signup, login, logout (built-in donde se pueda; signup custom).
   - Templates mínimos.
   - Modelo `Perfil` con OneToOne a User + FK a Tenant + datos negocio.
   - Signal `post_save` que crea Perfil automáticamente al crear User.
   - **Cada uno revisa el signal**: ¿qué pasa si falla? ¿se queda User huérfano?
   - **RA cubierto**: Programación RA7.b/c/d + RA9.c.

### 11:30-12:00 Pausa

### 12:00-14:30 Bloque 2 — Autorización por tenant
1. (45 min) **Mixin `TenantRequeridoMixin`** que comprueba que `request.user.perfil.tenant == request.tenant`. Si no, 403.
   - **RA cubierto**: Programación RA7.h · Lenguajes Marcas RA7.f.
2. (45 min) **Aplicar a vista placeholder** del tenant. Probar:
   - Login como user1 (tenant1) → entra a /e/tenant1/ OK.
   - Login como user1 → intenta /e/tenant2/ → 403.
3. (45 min) **Logout, signup público, tests manuales en parejas**: uno crea cuenta, otro intenta romper.
4. Commit, PR, review.

### 14:30-15:00 Cierre

**Criterio éxito día 4**: signup funcional, login/logout, no puedes ver el tenant ajeno.

---

## V 22 mayo — Día 5: Dashboard + manifiesto + primera app cargada

### 9:00-9:15 Check-in chat

### 9:15-11:30 Bloque 1 — Manifiesto y registro de apps
1. (30 min) **Hilo chat**: qué es el manifiesto (`manifiesto.toml`), por qué TOML, qué campos debe declarar una app (nombre, versión, descripción, qué aporta al menú, permisos, capacidades IA).
2. (90 min) **Implementar registro de apps**:
   - Modelo `AppRegistrada` con campos del manifiesto.
   - Comando `python manage.py descubrir_apps` que escanea `apps/` y lee manifiestos.
   - Tabla N:N `Tenant ↔ AppRegistrada` con `AppInstalada` (M:M through).
   - **RA cubierto**: Programación RA7.f + RA8.h + RA9.g.

### 11:30-12:00 Pausa

### 12:00-14:00 Bloque 2 — App `hola_mundo` + dashboard
1. (45 min) **App dummy `apps/hola_mundo/`**:
   - `manifiesto.toml` mínimo.
   - Vista que muestra "Hola Mundo desde Kore".
   - Template heredando del base.
2. (60 min) **Dashboard del tenant**:
   - Vista `/e/<slug>/` que lista las apps instaladas para ese tenant.
   - Si hola-mundo está instalada, aparece y se puede clicar.
   - Si no, mensaje "instala tu primera app".
3. (15 min) **Instalar hola_mundo en un tenant** desde admin. Comprobar que aparece.

### 14:00-15:00 Cierre semanal
- 30 min: cada uno consolida en su diario lo aprendido en la semana, lo que NO entendió del todo, lo que quiere reforzar en S2.
- 15 min: retrospectiva escrita en hilo de chat (qué fue bien, qué fue mal, qué cambiamos S2).
- 15 min: **Carmen consolida el registro semanal interno** (basado en commits, PRs y diarios).

**Criterio éxito S1**: signup → login → dashboard del tenant → hola_mundo instalada y funcionando. Ambos lo entienden y pueden explicarlo por escrito.

---

## Notas para la tutora

- **Ritmo**: para 1º DAM con Python nuevo, este S1 es ambicioso pero hacible. Si M19 cuesta más de lo esperado, X20 se simplifica (multi-tenant solo por sesión, sin middleware completo) y se cierra en J21 con tiempo.
- **Check-in por chat 9:00 + pings durante el día**: si un alumno no responde dentro del horario laboral (9:00-15:00), queda anotado en su registro semanal.
- **Diario diario**: cada noche queda en su repo privado, la tutora lo revisa antes del check-in del día siguiente.
- **Revisión de IA**: en cada PR el mensaje DEBE tener una sección `## Revisión de IA` con lo que se modificó / mejoró respecto a lo que la IA propuso.
- **Si alguien se atasca > 1h en un error de entorno**: el alumno manda al chat captura del error + lo que ya ha probado. La tutora responde por chat o con un commit de ejemplo en una rama auxiliar. Sin videollamada, sin screen-share.

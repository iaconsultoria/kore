# Scripts de Kore

Este directorio contiene scripts de utilidad para gestionar Kore.

## arrancar-kore.ps1

Script de arranque de Kore en Windows (PowerShell).

### Requisitos previos

1. Python 3.8+ instalado
2. PostgreSQL corriendo (local o remota)
3. Variables de entorno configuradas en .env:
   - DB_HOST: Host de PostgreSQL (ej. localhost)
   - DB_USER: Usuario de BD (ej. postgres)
   - DB_PASSWORD: Contraseña de BD
   - DB_NAME: Nombre de la BD (ej. kore)
4. Venv ya creado: python -m venv venv
5. Dependencias instaladas: pip install -r requirements.txt

### Uso

```powershell
.\scripts\arrancar-kore.ps1
```

### Qué hace

1. Verifica PostgreSQL: Conecta a la BD para asegurar disponibilidad
2. Activa venv: Entorno virtual de Python
3. Aplica migraciones: manage.py migrate
4. Verifica .env: Comprueba que exista archivo de configuración
5. Arranca servidor: manage.py runserver en http://localhost:8000

### Salida esperada
=== Iniciando Kore ===
[0/4] Verificando PostgreSQL...

✓ PostgreSQL disponible
[1/4] Activando entorno virtual...

✓ Entorno virtual activado
[2/4] Aplicando migraciones de BD...

✓ Migraciones aplicadas
[3/4] Verificando configuración...

✓ Archivo .env encontrado
[4/4] Iniciando servidor Django...
╔════════════════════════════════════════════════╗

║  Kore está disponible en:                      ║

║  • App: http://localhost:8000                  ║

║  • Admin: http://localhost:8000/admin          ║

║  • Facturas: http://localhost:8000/facturas    ║

║  • Calendario: http://localhost:8000/calendario║

║                                                ║

║  Presiona Ctrl+C para detener                  ║

╚════════════════════════════════════════════════╝

### Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| PostgreSQL no está disponible | BD no corre | Inicia PostgreSQL (Docker, pgAdmin, etc.) |
| No se encontró venv | Venv no creado | python -m venv venv |
| No se encontró .env | Falta configuración | Copia .env.example a .env y configura |
| Migraciones fallidas | Esquema desactualizado | Verifica que PostgreSQL sea accesible |

## nota-arranque-vs-java.md

Comparativa técnica entre el arranque de Django (Kore) vs un ejecutable Java equivalente. Solo lectura, no es ejecutable.

## Próximos scripts (futuros)

- crear-superuser.ps1: Crear usuario admin
- resetear-bd.ps1: Limpiar y reiniciar BD
- backup-bd.ps1: Hacer backup de PostgreSQL

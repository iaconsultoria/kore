# Script de arranque de Kore
# Uso: .\scripts\arrancar-kore.ps1

# Colores para output
$Success = 'Green'
$Error = 'Red'
$Info = 'Cyan'
$Warning = 'Yellow'

Write-Host "=== Iniciando Kore ===" -ForegroundColor $Info

# 0. Verificar PostgreSQL
Write-Host "`n[0/4] Verificando PostgreSQL..." -ForegroundColor $Info
try {
    $env:PGPASSWORD = $env:DB_PASSWORD
    psql -h $env:DB_HOST -U $env:DB_USER -d $env:DB_NAME -c "SELECT 1" > $null 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ PostgreSQL disponible" -ForegroundColor $Success
    } else {
        throw "No se pudo conectar a PostgreSQL"
    }
} catch {
    Write-Host "✗ PostgreSQL no está disponible" -ForegroundColor $Error
    Write-Host "  Verifica que PostgreSQL esté corriendo en: $env:DB_HOST" -ForegroundColor $Warning
    Write-Host "  Variables de entorno esperadas: DB_HOST, DB_USER, DB_PASSWORD, DB_NAME" -ForegroundColor $Warning
    exit 1
}

# 1. Activar venv
Write-Host "`n[1/4] Activando entorno virtual..." -ForegroundColor $Info
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    & .\venv\Scripts\Activate.ps1
    Write-Host "✓ Entorno virtual activado" -ForegroundColor $Success
} else {
    Write-Host "✗ No se encontró venv" -ForegroundColor $Error
    Write-Host "  Ejecuta primero: python -m venv venv" -ForegroundColor $Warning
    Write-Host "  Luego: venv\Scripts\Activate.ps1" -ForegroundColor $Warning
    Write-Host "  Después: pip install -r requirements.txt" -ForegroundColor $Warning
    exit 1
}

# 2. Aplicar migraciones
Write-Host "`n[2/4] Aplicando migraciones de BD..." -ForegroundColor $Info
python manage.py migrate
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Migraciones aplicadas" -ForegroundColor $Success
} else {
    Write-Host "✗ Error en migraciones" -ForegroundColor $Error
    exit 1
}

# 3. Verificar .env
Write-Host "`n[3/4] Verificando configuración..." -ForegroundColor $Info
if (Test-Path ".\.env") {
    Write-Host "✓ Archivo .env encontrado" -ForegroundColor $Success
} else {
    Write-Host "✗ No se encontró .env" -ForegroundColor $Error
    Write-Host "  Copia .env.example a .env y configura las variables" -ForegroundColor $Warning
    exit 1
}

# 4. Arrancar servidor
Write-Host "`n[4/4] Iniciando servidor Django..." -ForegroundColor $Info
Write-Host "`n╔════════════════════════════════════════════════╗" -ForegroundColor $Success
Write-Host "║  Kore está disponible en:                      ║" -ForegroundColor $Success
Write-Host "║  • App: http://localhost:8000                  ║" -ForegroundColor $Success
Write-Host "║  • Admin: http://localhost:8000/admin          ║" -ForegroundColor $Success
Write-Host "║  • Facturas: http://localhost:8000/facturas    ║" -ForegroundColor $Success
Write-Host "║  • Calendario: http://localhost:8000/calendario║" -ForegroundColor $Success
Write-Host "║                                                ║" -ForegroundColor $Success
Write-Host "║  Presiona Ctrl+C para detener                  ║" -ForegroundColor $Success
Write-Host "╚════════════════════════════════════════════════╝`n" -ForegroundColor $Success

python manage.py runserver

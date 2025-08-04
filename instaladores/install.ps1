Write-Host "Iniciando el proceso de instalación..." -ForegroundColor Cyan

# Función para verificar respuesta afirmativa
function EsSi($respuesta) {
    return $respuesta -match '^(y|s)$'
}

# Preguntar por Python
$instalarPython = Read-Host "¿Quieres instalar Python? (y/s para sí, cualquier otra tecla para no)"
if (EsSi $instalarPython) {
    Write-Host "Descargando Python..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe" -OutFile "python-installer.exe"
    Write-Host "Instalando Python..." -ForegroundColor Green
    Start-Process -FilePath "python-installer.exe" -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
    Remove-Item "python-installer.exe" -Force
}

# Preguntar por Node.js
$instalarNode = Read-Host "¿Quieres instalar Node.js? (y/s para sí, cualquier otra tecla para no)"
if (EsSi $instalarNode) {
    Write-Host "Descargando Node.js..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://nodejs.org/dist/v20.12.2/node-v20.12.2-x64.msi" -OutFile "node-installer.msi"
    Write-Host "Instalando Node.js..." -ForegroundColor Green
    Start-Process -FilePath "msiexec.exe" -ArgumentList "/i node-installer.msi /quiet" -Wait
    Remove-Item "node-installer.msi" -Force
}

# Verificación
Write-Host "`nVerificando instalaciones..." -ForegroundColor Cyan

if (EsSi $instalarPython) {
    Write-Host "Python: " -NoNewline; python --version
    Write-Host "Pip: " -NoNewline; pip --version
}

if (EsSi $instalarNode) {
    Write-Host "Node.js: " -NoNewline; node -v
    Write-Host "NPM: " -NoNewline; npm -v
}

Write-Host "`n✅ Instalación completada." -ForegroundColor Cyan

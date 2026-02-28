@echo off
chcp 65001 >nul
REM ═══════════════════════════════════════════════════════
REM  ARCHIVO: iniciar_servidor.bat
REM  DESCRIPCION: Inicio rápido del servidor PHP integrado
REM  AUTOR: German Gonzalez | FECHA: 2026-02-24
REM ═══════════════════════════════════════════════════════

title AuthSistema — Servidor PHP

echo.
echo  ╔══════════════════════════════════════════════╗
echo  ║       AuthSistema ^| Login y Registro         ║
echo  ║       Desarrollado por German Gonzalez        ║
echo  ╚══════════════════════════════════════════════╝
echo.

REM ──────────────────────────────────────────────────────
REM  BUSCAR PHP EN RUTAS CONOCIDAS
REM ──────────────────────────────────────────────────────
SET "PHP_EXE="

REM Intentar PHP en el PATH del sistema
where php >nul 2>&1
IF NOT ERRORLEVEL 1 (
    SET "PHP_EXE=php"
    GOTO :ENCONTRADO
)

REM Buscar en Laragon (versiones comunes)
FOR %%V IN (8.3.0 8.2.0 8.1.0 8.0.0 7.4.0) DO (
    IF EXIST "C:\laragon\bin\php\php%%V\php.exe" (
        SET "PHP_EXE=C:\laragon\bin\php\php%%V\php.exe"
        GOTO :ENCONTRADO
    )
)

REM Buscar en XAMPP
IF EXIST "C:\xampp\php\php.exe" (
    SET "PHP_EXE=C:\xampp\php\php.exe"
    GOTO :ENCONTRADO
)

REM Buscar en WAMP
FOR %%V IN (8.3.0 8.2.0 8.1.0) DO (
    IF EXIST "C:\wamp64\bin\php\php%%V\php.exe" (
        SET "PHP_EXE=C:\wamp64\bin\php\php%%V\php.exe"
        GOTO :ENCONTRADO
    )
)

REM Buscar en carpeta php en raíz
IF EXIST "C:\php\php.exe" (
    SET "PHP_EXE=C:\php\php.exe"
    GOTO :ENCONTRADO
)

REM ──────────────────────────────────────────────────────
REM  PHP NO ENCONTRADO — Instrucciones de instalación
REM ──────────────────────────────────────────────────────
:NO_ENCONTRADO
echo  ╔══════════════════════════════════════════════╗
echo  ║  ❌  PHP no está instalado en tu sistema     ║
echo  ╚══════════════════════════════════════════════╝
echo.
echo  Para ejecutar este proyecto necesitas PHP 8.1 o superior.
echo  Elige una de estas opciones (recomendamos la #1):
echo.
echo  ┌─────────────────────────────────────────────────┐
echo  │  OPCION 1 — Laragon (MAS FACIL, recomendado)    │
echo  │  https://laragon.org/download                   │
echo  │  • Instala Laragon Full                         │
echo  │  • Abre Laragon y activa "Start All"            │
echo  │  • Vuelve a ejecutar este .bat                  │
echo  ├─────────────────────────────────────────────────┤
echo  │  OPCION 2 — XAMPP (muy popular)                 │
echo  │  https://www.apachefriends.org/es/download.html │
echo  │  • Instala XAMPP                                │
echo  │  • Agrega C:\xampp\php al PATH del sistema      │
echo  │  • Vuelve a ejecutar este .bat                  │
echo  ├─────────────────────────────────────────────────┤
echo  │  OPCION 3 — PHP nativo (avanzado)               │
echo  │  https://windows.php.net/download               │
echo  │  • Descarga PHP 8.3 Thread Safe (x64)           │
echo  │  • Extrae en C:\php\                            │
echo  │  • Agrega C:\php al PATH del sistema            │
echo  │  • Vuelve a ejecutar este .bat                  │
echo  └─────────────────────────────────────────────────┘
echo.
echo  Presiona cualquier tecla para abrir el sitio de Laragon...
pause >nul
start "" "https://laragon.org/download"
exit /b 1

REM ──────────────────────────────────────────────────────
REM  PHP ENCONTRADO — Ejecutar servidor
REM ──────────────────────────────────────────────────────
:ENCONTRADO
echo  ✅ PHP encontrado en: %PHP_EXE%
echo.

REM Mostrar versión de PHP
"%PHP_EXE%" --version
echo.

REM ──────────────────────────────────────────────────────
REM  EJECUTAR MIGRACIÓN DE BASE DE DATOS
REM ──────────────────────────────────────────────────────
echo  ────────────────────────────────────────────────
echo  📦 Ejecutando migración...
echo  ────────────────────────────────────────────────
"%PHP_EXE%" migraciones\crear_tabla_usuarios.php
echo.

REM ──────────────────────────────────────────────────────
REM  INICIAR SERVIDOR PHP INTEGRADO
REM ──────────────────────────────────────────────────────
echo  ────────────────────────────────────────────────
echo  🚀 Servidor iniciado en: http://localhost:8000
echo  📂 Carpeta pública:      publico\
echo  ────────────────────────────────────────────────
echo.
echo  Rutas disponibles:
echo    http://localhost:8000/login     → Iniciar sesión
echo    http://localhost:8000/registro  → Crear cuenta
echo    http://localhost:8000/panel     → Panel (requiere login)
echo    http://localhost:8000/logout    → Cerrar sesión
echo.
echo  Presiona Ctrl+C para detener el servidor
echo.

REM Abrir navegador automáticamente
timeout /t 1 /nobreak >nul
start "" "http://localhost:8000/login"

REM Iniciar el servidor PHP integrado
"%PHP_EXE%" -S localhost:8000 -t publico/

pause

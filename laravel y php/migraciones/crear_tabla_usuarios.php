<?php
/**
 * ARCHIVO: migraciones/crear_tabla_usuarios.php
 * DESCRIPCION: Migración para crear la tabla `usuarios` en la base de datos MySQL
 * AUTOR: German Gonzalez
 * FECHA: 2026-02-24
 *
 * USO: Ejecutar una sola vez desde la línea de comandos:
 *      php migraciones/crear_tabla_usuarios.php
 *
 * PREREQUISITO: Crear la base de datos previamente:
 *      CREATE DATABASE auth_laravel CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
 */

require_once __DIR__ . '/../config/base_datos.php';

// ─────────────────────────────────────────────
// CONEXIÓN A LA BASE DE DATOS
// ─────────────────────────────────────────────

try {
    $dsn       = sprintf('%s:host=%s;port=%s;charset=%s', BD_MOTOR, BD_HOST, BD_PUERTO, BD_CHARSET);
    $conexion  = new PDO($dsn, BD_USUARIO, BD_CONTRASENA);
    $conexion->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    echo "✅ Conexión al servidor MySQL exitosa.\n";

    // Crear base de datos si no existe
    $conexion->exec("CREATE DATABASE IF NOT EXISTS `" . BD_NOMBRE . "` 
                     CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
    echo "✅ Base de datos `" . BD_NOMBRE . "` verificada/creada.\n";

    // Seleccionar la base de datos
    $conexion->exec("USE `" . BD_NOMBRE . "`");

} catch (PDOException $excepcion) {
    echo "❌ Error de conexión: " . $excepcion->getMessage() . "\n";
    exit(1);
}

// ─────────────────────────────────────────────
// CREAR TABLA USUARIOS
// ─────────────────────────────────────────────

/**
 * Definición de la tabla `usuarios`
 * 
 * Columnas (orden ascendente por tipo/tamaño):
 *  - id          → Clave primaria auto-incremental
 *  - nombre      → Nombre completo (máx 100 chars)
 *  - correo      → Correo electrónico único (máx 150 chars)
 *  - contrasena  → Hash bcrypt (máx 255 chars)
 *  - creado_en   → Fecha y hora de registro
 */
$sqlCrearTabla = "
    CREATE TABLE IF NOT EXISTS `usuarios` (
        `id`          INT             UNSIGNED NOT NULL AUTO_INCREMENT,
        `nombre`      VARCHAR(100)    NOT NULL,
        `correo`      VARCHAR(150)    NOT NULL UNIQUE,
        `contrasena`  VARCHAR(255)    NOT NULL,
        `creado_en`   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (`id`),
        INDEX `idx_correo` (`correo`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
";

try {
    $conexion->exec($sqlCrearTabla);
    echo "✅ Tabla `usuarios` creada correctamente.\n";
    echo "\n🎉 ¡Migración completada! El sistema está listo.\n";
    echo "   Ejecuta el servidor con: php -S localhost:8000 -t publico/\n\n";

} catch (PDOException $excepcion) {
    echo "❌ Error al crear la tabla: " . $excepcion->getMessage() . "\n";
    exit(1);
}

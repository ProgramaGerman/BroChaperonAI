<?php
/**
 * ARCHIVO: config/base_datos.php
 * DESCRIPCION: Configuración de la base de datos del sistema
 * AUTOR: German Gonzalez
 * FECHA: 2026-02-24
 * 
 * Tamaño: PEQUEÑO (configuración simple)
 * Orden: A - Primero en cargarse
 */

// ─────────────────────────────────────────────
// CONSTANTES DE CONFIGURACIÓN DE BASE DE DATOS
// ─────────────────────────────────────────────

/** @var string Motor de base de datos (mysql | sqlite | pgsql) */
define('BD_MOTOR',      'mysql');

/** @var string Nombre del host donde corre la BD */
define('BD_HOST',       'localhost');

/** @var string Nombre de la base de datos del proyecto */
define('BD_NOMBRE',     'auth_laravel');

/** @var string Usuario de la base de datos */
define('BD_USUARIO',    'root');

/** @var string Contraseña del usuario de la BD */
define('BD_CONTRASENA', '');

/** @var string Puerto de conexión */
define('BD_PUERTO',     '3306');

/** @var string Conjunto de caracteres */
define('BD_CHARSET',    'utf8mb4');

// ─────────────────────────────────────────────
// CONFIGURACIÓN DE SESIÓN
// ─────────────────────────────────────────────

/** @var string Nombre de la sesión activa */
define('SESION_NOMBRE', 'auth_sesion');

/** @var int Duración de la sesión en segundos (8 horas) */
define('SESION_DURACION', 28800);

// ─────────────────────────────────────────────
// CONFIGURACIÓN DE SEGURIDAD
// ─────────────────────────────────────────────

/** @var string Clave secreta para tokens CSRF */
define('CLAVE_SECRETA', 'laravel_auth_clave_2026_german');

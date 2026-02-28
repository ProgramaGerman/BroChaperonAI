<?php
/**
 * ARCHIVO: publico/index.php
 * DESCRIPCION: Punto de entrada único (Front Controller) del sistema
 *              Todo el tráfico HTTP pasa por este archivo gracias al servidor PHP integrado
 * AUTOR: German Gonzalez
 * FECHA: 2026-02-24
 *
 * Tamaño: MUY PEQUEÑO (solo actúa como bootstrapper)
 * Orden: G - Último archivo en ejecutarse, es el punto de entrada
 *
 * FLUJO:
 *   petición HTTP → index.php → rutas/web.php → Enrutador → Controlador → Vista
 */

// ─────────────────────────────────────────────
// CONSTANTES DEL SISTEMA
// ─────────────────────────────────────────────

/** @var string Directorio raíz del proyecto */
define('RAIZ', dirname(__DIR__));

// ─────────────────────────────────────────────
// CARGAR CONFIGURACIÓN BASE
// ─────────────────────────────────────────────

require_once RAIZ . '/config/base_datos.php';

// ─────────────────────────────────────────────
// CARGAR LAS RUTAS (despacha la petición)
// ─────────────────────────────────────────────

require_once RAIZ . '/rutas/web.php';

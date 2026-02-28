<?php
/**
 * ARCHIVO: rutas/web.php
 * DESCRIPCION: Definición de todas las rutas web del sistema de autenticación
 * AUTOR: German Gonzalez
 * FECHA: 2026-02-24
 *
 * Tamaño: PEQUEÑO-MEDIANO
 * Orden: F - Se carga después de los controladores
 *
 * CONVENCIÓN: Rutas ordenadas alfabéticamente por URI
 */

require_once __DIR__ . '/../controladores/AuthControlador.php';
require_once __DIR__ . '/../controladores/RegistroControlador.php';
require_once __DIR__ . '/../nucleo/Enrutador.php';

// ─────────────────────────────────────────────
// INSTANCIAR EL ENRUTADOR
// ─────────────────────────────────────────────

/** @var Enrutador $enrutador Instancia global del motor de rutas */
$enrutador = new Enrutador();

// ─────────────────────────────────────────────
// DEFINICIÓN DE RUTAS (orden alfabético por URI)
// ─────────────────────────────────────────────

// Ruta raíz → redirige al login
$enrutador->get('/', [AuthControlador::class, 'mostrarFormulario']);

// /login → GET: mostrar formulario | POST: procesar login
$enrutador->get('/login',  [AuthControlador::class, 'mostrarFormulario']);
$enrutador->post('/login', [AuthControlador::class, 'procesarLogin']);

// /logout → cerrar sesión
$enrutador->get('/logout', [AuthControlador::class, 'cerrarSesion']);

// /panel → panel del usuario autenticado
$enrutador->get('/panel', [AuthControlador::class, 'mostrarPanel']);

// /registro → GET: mostrar formulario | POST: procesar registro
$enrutador->get('/registro',  [RegistroControlador::class, 'mostrarFormulario']);
$enrutador->post('/registro', [RegistroControlador::class, 'procesarRegistro']);

// ─────────────────────────────────────────────
// DESPACHAR LA PETICIÓN ACTUAL
// ─────────────────────────────────────────────

$enrutador->despachar();

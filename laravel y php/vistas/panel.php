<?php
/**
 * ARCHIVO: vistas/panel.php
 * DESCRIPCION: Vista del panel del usuario autenticado (dashboard protegido)
 * AUTOR: German Gonzalez
 * FECHA: 2026-02-24
 *
 * VARIABLES DISPONIBLES (inyectadas desde AuthControlador::mostrarPanel):
 *   - $usuario (array) - Datos del usuario: ['id', 'nombre', 'correo']
 */

require_once __DIR__ . '/plantilla.php';
encabezado('Panel');
?>

<!-- ═══════════════════════════════════════════ -->
<!-- PANEL DEL USUARIO AUTENTICADO               -->
<!-- ═══════════════════════════════════════════ -->
<main class="contenedor-panel">

    <!-- Barra de navegación -->
    <nav class="barra-nav">
        <div class="nav-marca">🔐 AuthSistema</div>
        <div class="nav-usuario">
            <span class="nav-nombre">👋 <?= htmlspecialchars($usuario['nombre']) ?></span>
            <a id="btn-logout" class="btn-cerrar-sesion" href="/logout">
                Cerrar Sesión
            </a>
        </div>
    </nav>

    <!-- Contenido del panel -->
    <div class="panel-contenido">

        <!-- Tarjeta de bienvenida -->
        <div class="tarjeta-bienvenida">
            <div class="avatar">
                <?= strtoupper(substr($usuario['nombre'], 0, 1)) ?>
            </div>
            <div class="bienvenida-info">
                <h1 class="titulo-panel">
                    ¡Bienvenido, <?= htmlspecialchars($usuario['nombre']) ?>! 🎉
                </h1>
                <p class="correo-panel">
                    📧 <?= htmlspecialchars($usuario['correo']) ?>
                </p>
                <span class="insignia-activo">✅ Sesión Activa</span>
            </div>
        </div>

        <!-- Tarjetas de información -->
        <div class="cuadricula-info">

            <div class="tarjeta-info">
                <div class="tarjeta-info-icono">🔑</div>
                <h2 class="tarjeta-info-titulo">Autenticación</h2>
                <p class="tarjeta-info-desc">
                    Tu sesión está activa y protegida con tokens CSRF y hashing bcrypt.
                </p>
            </div>

            <div class="tarjeta-info">
                <div class="tarjeta-info-icono">🛡️</div>
                <h2 class="tarjeta-info-titulo">Seguridad</h2>
                <p class="tarjeta-info-desc">
                    Contraseñas hasheadas con bcrypt (cost=12) y protección contra Session Fixation.
                </p>
            </div>

            <div class="tarjeta-info">
                <div class="tarjeta-info-icono">⚡</div>
                <h2 class="tarjeta-info-titulo">Performance</h2>
                <p class="tarjeta-info-desc">
                    Sistema liviano sin frameworks pesados — PHP puro con arquitectura MVC limpia.
                </p>
            </div>

        </div>

    </div><!-- /panel-contenido -->

</main>

<?php piePagina(); ?>

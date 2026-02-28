<?php
/**
 * ARCHIVO: vistas/login.php
 * DESCRIPCION: Vista del formulario de inicio de sesión
 * AUTOR: German Gonzalez
 * FECHA: 2026-02-24
 *
 * VARIABLES DISPONIBLES (inyectadas desde AuthControlador):
 *   - $errores       (array) - Lista de mensajes de error
 *   - $_SESSION['exito_registro'] (string) - Mensaje de registro exitoso
 */

require_once __DIR__ . '/plantilla.php';
encabezado('Iniciar Sesión');
?>

<!-- ═══════════════════════════════════════════ -->
<!-- CONTENEDOR PRINCIPAL DEL LOGIN              -->
<!-- ═══════════════════════════════════════════ -->
<main class="contenedor-auth">

    <div class="tarjeta-auth">

        <!-- Encabezado de la tarjeta -->
        <div class="encabezado-tarjeta">
            <div class="icono-auth">🔐</div>
            <h1 class="titulo-auth">Iniciar Sesión</h1>
            <p class="subtitulo-auth">Bienvenido de nuevo — ingresa tus credenciales</p>
        </div>

        <!-- ─────────────────────────────────── -->
        <!-- MENSAJE DE ÉXITO (post-registro)    -->
        <!-- ─────────────────────────────────── -->
        <?php if (!empty($_SESSION['exito_registro'])): ?>
            <div class="alerta alerta-exito" role="alert">
                <span class="alerta-icono">✅</span>
                <?= htmlspecialchars($_SESSION['exito_registro']) ?>
            </div>
            <?php unset($_SESSION['exito_registro']); ?>
        <?php endif; ?>

        <!-- ─────────────────────────────────── -->
        <!-- MENSAJES DE ERROR                   -->
        <!-- ─────────────────────────────────── -->
        <?php if (!empty($errores)): ?>
            <div class="alerta alerta-error" role="alert">
                <span class="alerta-icono">⚠️</span>
                <ul class="lista-errores">
                    <?php foreach ($errores as $error): ?>
                        <li><?= htmlspecialchars($error) ?></li>
                    <?php endforeach; ?>
                </ul>
            </div>
        <?php endif; ?>

        <!-- ─────────────────────────────────── -->
        <!-- FORMULARIO DE LOGIN                 -->
        <!-- ─────────────────────────────────── -->
        <form 
            id="formulario-login"
            class="formulario"
            action="/login" 
            method="POST"
            novalidate
        >
            <!-- Token CSRF oculto -->
            <input type="hidden" name="_token" value="<?= htmlspecialchars($_SESSION['_token']) ?>">

            <!-- Campo: Correo Electrónico -->
            <div class="grupo-campo">
                <label class="etiqueta" for="correo">
                    📧 Correo Electrónico
                </label>
                <input
                    id="correo"
                    class="campo"
                    type="email"
                    name="correo"
                    placeholder="tu@correo.com"
                    autocomplete="email"
                    required
                >
            </div>

            <!-- Campo: Contraseña -->
            <div class="grupo-campo">
                <label class="etiqueta" for="contrasena">
                    🔑 Contraseña
                </label>
                <div class="campo-con-icono">
                    <input
                        id="contrasena"
                        class="campo"
                        type="password"
                        name="contrasena"
                        placeholder="Tu contraseña segura"
                        autocomplete="current-password"
                        required
                    >
                    <!-- Botón para mostrar/ocultar contraseña -->
                    <button 
                        type="button" 
                        class="btn-ojo" 
                        onclick="alternarContrasena('contrasena')"
                        aria-label="Mostrar u ocultar contraseña"
                        title="Ver contraseña"
                    >👁</button>
                </div>
            </div>

            <!-- Botón de envío -->
            <button id="btn-login" class="btn-primario" type="submit">
                <span class="btn-texto">Iniciar Sesión</span>
                <span class="btn-cargando" hidden>Verificando...</span>
            </button>

        </form>

        <!-- ─────────────────────────────────── -->
        <!-- ENLACE AL REGISTRO                  -->
        <!-- ─────────────────────────────────── -->
        <div class="pie-tarjeta">
            <p>¿No tienes cuenta? 
                <a id="enlace-registro" class="enlace" href="/registro">
                    Regístrate gratis
                </a>
            </p>
        </div>

    </div><!-- /tarjeta-auth -->

</main>

<!-- ═══════════════════════════════════════════ -->
<!-- SCRIPTS DE LA VISTA                         -->
<!-- ═══════════════════════════════════════════ -->
<script>
/**
 * Alterna la visibilidad de un campo de contraseña
 * @param {string} idCampo - ID del input de contraseña
 */
function alternarContrasena(idCampo) {
    const campo = document.getElementById(idCampo);
    campo.type = (campo.type === 'password') ? 'text' : 'password';
}

/**
 * Muestra el estado de carga al enviar el formulario
 */
document.getElementById('formulario-login').addEventListener('submit', function() {
    const btnTexto    = document.querySelector('.btn-texto');
    const btnCargando = document.querySelector('.btn-cargando');
    btnTexto.hidden    = true;
    btnCargando.hidden = false;
});
</script>

<?php piePagina(); ?>

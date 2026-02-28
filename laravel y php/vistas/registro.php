<?php
/**
 * ARCHIVO: vistas/registro.php
 * DESCRIPCION: Vista del formulario de registro de nuevos usuarios
 * AUTOR: German Gonzalez
 * FECHA: 2026-02-24
 *
 * VARIABLES DISPONIBLES (inyectadas desde RegistroControlador):
 *   - $errores         (array)  - Lista de mensajes de error
 *   - $datosAnteriores (array)  - Datos para repoblar el formulario ['nombre', 'correo']
 */

require_once __DIR__ . '/plantilla.php';
encabezado('Crear Cuenta');
?>

<!-- ═══════════════════════════════════════════ -->
<!-- CONTENEDOR PRINCIPAL DEL REGISTRO           -->
<!-- ═══════════════════════════════════════════ -->
<main class="contenedor-auth">

    <div class="tarjeta-auth tarjeta-registro">

        <!-- Encabezado de la tarjeta -->
        <div class="encabezado-tarjeta">
            <div class="icono-auth">✨</div>
            <h1 class="titulo-auth">Crear Cuenta</h1>
            <p class="subtitulo-auth">Únete hoy — es gratis y rápido</p>
        </div>

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
        <!-- FORMULARIO DE REGISTRO              -->
        <!-- ─────────────────────────────────── -->
        <form 
            id="formulario-registro"
            class="formulario"
            action="/registro" 
            method="POST"
            novalidate
        >
            <!-- Token CSRF oculto -->
            <input type="hidden" name="_token" value="<?= htmlspecialchars($_SESSION['_token']) ?>">

            <!-- Campo: Nombre Completo -->
            <div class="grupo-campo">
                <label class="etiqueta" for="nombre">
                    👤 Nombre Completo
                </label>
                <input
                    id="nombre"
                    class="campo"
                    type="text"
                    name="nombre"
                    value="<?= htmlspecialchars($datosAnteriores['nombre'] ?? '') ?>"
                    placeholder="Tu nombre completo"
                    autocomplete="name"
                    maxlength="100"
                    required
                >
            </div>

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
                    value="<?= htmlspecialchars($datosAnteriores['correo'] ?? '') ?>"
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
                        placeholder="Mínimo 8 caracteres, 1 mayúscula, 1 número"
                        autocomplete="new-password"
                        minlength="8"
                        required
                    >
                    <button 
                        type="button" 
                        class="btn-ojo"
                        onclick="alternarContrasena('contrasena')"
                        aria-label="Ver contraseña"
                    >👁</button>
                </div>
                <!-- Indicador de fortaleza de contraseña -->
                <div class="barra-fortaleza-contenedor" hidden id="barra-contenedor">
                    <div id="barra-fortaleza" class="barra-fortaleza"></div>
                    <span id="texto-fortaleza" class="texto-fortaleza"></span>
                </div>
            </div>

            <!-- Campo: Confirmar Contraseña -->
            <div class="grupo-campo">
                <label class="etiqueta" for="confirmar_contrasena">
                    🔒 Confirmar Contraseña
                </label>
                <div class="campo-con-icono">
                    <input
                        id="confirmar_contrasena"
                        class="campo"
                        type="password"
                        name="confirmar_contrasena"
                        placeholder="Repite tu contraseña"
                        autocomplete="new-password"
                        required
                    >
                    <button 
                        type="button" 
                        class="btn-ojo"
                        onclick="alternarContrasena('confirmar_contrasena')"
                        aria-label="Ver confirmación"
                    >👁</button>
                </div>
            </div>

            <!-- Botón de envío -->
            <button id="btn-registro" class="btn-primario" type="submit">
                <span class="btn-texto">🚀 Crear Mi Cuenta</span>
                <span class="btn-cargando" hidden>Registrando...</span>
            </button>

        </form>

        <!-- ─────────────────────────────────── -->
        <!-- ENLACE AL LOGIN                     -->
        <!-- ─────────────────────────────────── -->
        <div class="pie-tarjeta">
            <p>¿Ya tienes cuenta? 
                <a id="enlace-login" class="enlace" href="/login">
                    Inicia sesión aquí
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
 * @param {string} idCampo - ID del input
 */
function alternarContrasena(idCampo) {
    const campo = document.getElementById(idCampo);
    campo.type = (campo.type === 'password') ? 'text' : 'password';
}

/**
 * Calcula y muestra la fortaleza de la contraseña
 * @param {string} contrasena - Contraseña ingresada
 * @returns {number} Puntaje de fortaleza (0-4)
 */
function calcularFortaleza(contrasena) {
    let puntaje = 0;
    if (contrasena.length >= 8)             puntaje++;
    if (/[A-Z]/.test(contrasena))           puntaje++;
    if (/[0-9]/.test(contrasena))           puntaje++;
    if (/[^A-Za-z0-9]/.test(contrasena))   puntaje++;
    return puntaje;
}

// Escuchar cambios en el campo de contraseña
document.getElementById('contrasena').addEventListener('input', function() {
    const valor      = this.value;
    const contenedor = document.getElementById('barra-contenedor');
    const barra      = document.getElementById('barra-fortaleza');
    const texto      = document.getElementById('texto-fortaleza');

    if (valor.length === 0) {
        contenedor.hidden = true;
        return;
    }

    contenedor.hidden = false;
    const puntaje = calcularFortaleza(valor);
    const niveles = ['', 'debil', 'media', 'buena', 'fuerte'];
    const textos  = ['', '😟 Muy débil', '😐 Media', '😊 Buena', '💪 Fuerte'];

    barra.className   = 'barra-fortaleza nivel-' + (niveles[puntaje] || 'debil');
    texto.textContent = textos[puntaje] || textos[1];
});

// Estado de carga al enviar el formulario
document.getElementById('formulario-registro').addEventListener('submit', function() {
    document.querySelector('.btn-texto').hidden    = true;
    document.querySelector('.btn-cargando').hidden = false;
});
</script>

<?php piePagina(); ?>

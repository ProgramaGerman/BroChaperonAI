<?php
/**
 * ARCHIVO: vistas/plantilla.php
 * DESCRIPCION: Plantilla HTML base compartida por todas las vistas del sistema
 * AUTOR: German Gonzalez
 * FECHA: 2026-02-24
 *
 * USO: Esta plantilla NO se renderiza sola — las vistas hijas incluyen el encabezado
 *      y pie de página directamente con las funciones definidas aquí.
 */

/**
 * Renderiza el encabezado HTML de la página
 *
 * @param string $titulo Título de la pestaña del navegador
 * @return void
 */
function encabezado(string $titulo = 'Auth Sistema'): void
{
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <!-- ═══════════════════════════════════════ -->
    <!-- META TAGS ESENCIALES                    -->
    <!-- ═══════════════════════════════════════ -->
    <meta charset="UTF-8">
    <meta name="viewport"    content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Sistema de autenticación seguro con PHP y Laravel">
    <meta name="author"      content="German Gonzalez">

    <title><?= htmlspecialchars($titulo) ?> | AuthSistema</title>

    <!-- ═══════════════════════════════════════ -->
    <!-- FUENTES Y ESTILOS                       -->
    <!-- ═══════════════════════════════════════ -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/css/estilos.css">
</head>
<body>
<?php
}

/**
 * Renderiza el pie de página HTML y cierra las etiquetas del documento
 *
 * @return void
 */
function piePagina(): void
{
?>
    <!-- ═══════════════════════════════════════ -->
    <!-- PIE DE PÁGINA                           -->
    <!-- ═══════════════════════════════════════ -->
    <footer class="pie">
        <p>
            &copy; <?= date('Y') ?> AuthSistema &mdash; 
            Desarrollado por <strong>German Gonzalez</strong>
        </p>
    </footer>

</body>
</html>
<?php
}

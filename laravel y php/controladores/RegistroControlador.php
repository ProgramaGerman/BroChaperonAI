<?php
/**
 * ARCHIVO: controladores/RegistroControlador.php
 * DESCRIPCION: Controlador de registro — gestiona la creación de nuevas cuentas de usuario
 * AUTOR: German Gonzalez
 * FECHA: 2026-02-24
 *
 * Tamaño: GRANDE
 * Orden: E - Segundo controlador (R después de A en alfabético para 'Registro')
 *
 * RESPONSABILIDAD: Mostrar el formulario de registro y procesar la creación de usuarios
 */

require_once __DIR__ . '/../modelos/Usuario.php';

// ─────────────────────────────────────────────
// CLASE REGISTRO CONTROLADOR
// ─────────────────────────────────────────────

class RegistroControlador
{
    /** @var Usuario Instancia del modelo de usuario */
    private Usuario $modeloUsuario;

    // ──────────────────────────────────────────
    // CONSTRUCTOR
    // ──────────────────────────────────────────

    /**
     * Constructor: inicializa el modelo e inicia la sesión activa
     */
    public function __construct()
    {
        if (session_status() === PHP_SESSION_NONE) {
            session_name(SESION_NOMBRE);
            session_start();
        }

        $this->modeloUsuario = new Usuario();
    }

    // ──────────────────────────────────────────
    // MÉTODOS PÚBLICOS (orden alfabético)
    // ──────────────────────────────────────────

    /**
     * Acción: mostrar el formulario de registro
     * Ruta: GET /registro
     *
     * @return void
     */
    public function mostrarFormulario(): void
    {
        // Si ya está autenticado → redirigir al panel
        if (isset($_SESSION['usuario'])) {
            $this->redirigir('/panel');
            return;
        }

        // Generar token CSRF
        if (empty($_SESSION['_token'])) {
            $_SESSION['_token'] = bin2hex(random_bytes(32));
        }

        // Recuperar errores y datos anteriores del formulario (si los hay)
        $errores       = $_SESSION['errores_registro'] ?? [];
        $datosAnteriores = $_SESSION['datos_registro'] ?? [];
        unset($_SESSION['errores_registro'], $_SESSION['datos_registro']);

        // Renderizar la vista de registro
        require_once __DIR__ . '/../vistas/registro.php';
    }

    /**
     * Acción: procesar el formulario de registro enviado
     * Ruta: POST /registro
     *
     * @return void
     */
    public function procesarRegistro(): void
    {
        // 1. Validar token CSRF
        $tokenRecibido = $_POST['_token'] ?? '';
        if (!isset($_SESSION['_token']) || !hash_equals($_SESSION['_token'], $tokenRecibido)) {
            $_SESSION['errores_registro'] = ['Token de seguridad inválido. Recarga la página.'];
            $this->redirigir('/registro');
            return;
        }

        // 2. Recoger y limpiar los datos del formulario
        $nombre          = trim($_POST['nombre'] ?? '');
        $correo          = trim(strtolower($_POST['correo'] ?? ''));
        $contrasena      = $_POST['contrasena'] ?? '';
        $confirmar       = $_POST['confirmar_contrasena'] ?? '';

        // 3. Guardar datos anteriores para repoblar el formulario en caso de error
        $_SESSION['datos_registro'] = [
            'nombre' => htmlspecialchars($nombre),
            'correo' => htmlspecialchars($correo),
        ];

        // 4. Validar todos los campos del formulario
        $errores = $this->validarDatosRegistro($nombre, $correo, $contrasena, $confirmar);

        if (!empty($errores)) {
            $_SESSION['errores_registro'] = $errores;
            $this->redirigir('/registro');
            return;
        }

        // 5. Verificar si el correo ya está registrado
        if ($this->modeloUsuario->correoExiste($correo)) {
            $_SESSION['errores_registro'] = ['Este correo electrónico ya está en uso.'];
            $this->redirigir('/registro');
            return;
        }

        // 6. Crear el usuario en la base de datos
        $creado = $this->modeloUsuario->crear($nombre, $correo, $contrasena);

        if (!$creado) {
            $_SESSION['errores_registro'] = ['Error al crear la cuenta. Intente de nuevo.'];
            $this->redirigir('/registro');
            return;
        }

        // 7. Registro exitoso → informar y redirigir al login
        $_SESSION['exito_registro'] = '¡Cuenta creada exitosamente! Ya puedes iniciar sesión.';
        unset($_SESSION['datos_registro']);
        $this->redirigir('/login');
    }

    // ──────────────────────────────────────────
    // MÉTODOS PRIVADOS (orden alfabético)
    // ──────────────────────────────────────────

    /**
     * Redirige a la URL especificada y finaliza la ejecución
     *
     * @param string $url Ruta de destino
     * @return void
     */
    private function redirigir(string $url): void
    {
        header('Location: ' . $url);
        exit;
    }

    /**
     * Valida todos los campos del formulario de registro
     *
     * @param string $nombre     Nombre del usuario
     * @param string $correo     Correo electrónico
     * @param string $contrasena Contraseña nueva
     * @param string $confirmar  Confirmación de contraseña
     * @return array Lista de errores encontrados
     */
    private function validarDatosRegistro(
        string $nombre,
        string $correo,
        string $contrasena,
        string $confirmar
    ): array {
        $errores = [];

        // Validar nombre
        if (empty($nombre)) {
            $errores[] = 'El nombre completo es requerido.';
        } elseif (strlen($nombre) < 3) {
            $errores[] = 'El nombre debe tener al menos 3 caracteres.';
        } elseif (strlen($nombre) > 100) {
            $errores[] = 'El nombre no puede superar los 100 caracteres.';
        }

        // Validar correo
        if (empty($correo)) {
            $errores[] = 'El correo electrónico es requerido.';
        } elseif (!filter_var($correo, FILTER_VALIDATE_EMAIL)) {
            $errores[] = 'El formato del correo electrónico no es válido.';
        }

        // Validar contraseña
        if (empty($contrasena)) {
            $errores[] = 'La contraseña es requerida.';
        } elseif (strlen($contrasena) < 8) {
            $errores[] = 'La contraseña debe tener al menos 8 caracteres.';
        } elseif (!preg_match('/[A-Z]/', $contrasena)) {
            $errores[] = 'La contraseña debe contener al menos una letra mayúscula.';
        } elseif (!preg_match('/[0-9]/', $contrasena)) {
            $errores[] = 'La contraseña debe contener al menos un número.';
        }

        // Validar confirmación de contraseña
        if ($contrasena !== $confirmar) {
            $errores[] = 'Las contraseñas no coinciden.';
        }

        return $errores;
    }
}

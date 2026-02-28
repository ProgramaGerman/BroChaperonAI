<?php
/**
 * ARCHIVO: controladores/AuthControlador.php
 * DESCRIPCION: Controlador de autenticación — gestiona el inicio de sesión y cierre de sesión
 * AUTOR: German Gonzalez
 * FECHA: 2026-02-24
 *
 * Tamaño: GRANDE
 * Orden: D - Controlador principal de auth (A antes que R en alfabético)
 *
 * RESPONSABILIDAD: Procesar login/logout, validar datos e iniciar sesiones PHP
 */

require_once __DIR__ . '/../modelos/Usuario.php';

// ─────────────────────────────────────────────
// CLASE AUTH CONTROLADOR
// ─────────────────────────────────────────────

class AuthControlador
{
    /** @var Usuario Instancia del modelo de usuario */
    private Usuario $modeloUsuario;

    // ──────────────────────────────────────────
    // CONSTRUCTOR
    // ──────────────────────────────────────────

    /**
     * Constructor: inicializa el modelo de usuario e inicia la sesión
     */
    public function __construct()
    {
        // Iniciar sesión si no está activa
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
     * Acción: cerrar la sesión del usuario actual
     * Ruta: GET /logout
     *
     * @return void
     */
    public function cerrarSesion(): void
    {
        // Destruir todos los datos de sesión
        $_SESSION = [];
        session_destroy();

        // Redirigir al login
        $this->redirigir('/login');
    }

    /**
     * Acción: mostrar el formulario de inicio de sesión
     * Ruta: GET /login
     *
     * @return void
     */
    public function mostrarFormulario(): void
    {
        // Si el usuario ya está autenticado → redirigir al panel
        if ($this->estaAutenticado()) {
            $this->redirigir('/panel');
            return;
        }

        // Generar token CSRF para el formulario
        $this->generarTokenCsrf();

        // Obtener errores previos si existen
        $errores = $_SESSION['errores_login'] ?? [];
        unset($_SESSION['errores_login']);

        // Renderizar la vista de login
        require_once __DIR__ . '/../vistas/login.php';
    }

    /**
     * Acción: mostrar el panel del usuario autenticado
     * Ruta: GET /panel
     *
     * @return void
     */
    public function mostrarPanel(): void
    {
        // Verificar autenticación, si no → redirigir al login
        if (!$this->estaAutenticado()) {
            $this->redirigir('/login');
            return;
        }

        $usuario = $_SESSION['usuario'];
        require_once __DIR__ . '/../vistas/panel.php';
    }

    /**
     * Acción: procesar el formulario de inicio de sesión enviado
     * Ruta: POST /login
     *
     * @return void
     */
    public function procesarLogin(): void
    {
        // 1. Validar token CSRF
        if (!$this->validarTokenCsrf($_POST['_token'] ?? '')) {
            $this->guardarError('login', 'Token de seguridad inválido. Recarga la página.');
            $this->redirigir('/login');
            return;
        }

        // 2. Obtener y limpiar los datos del formulario
        $correo     = trim($_POST['correo'] ?? '');
        $contrasena = $_POST['contrasena'] ?? '';

        // 3. Validar que los campos no estén vacíos
        $errores = $this->validarCamposLogin($correo, $contrasena);

        if (!empty($errores)) {
            $_SESSION['errores_login'] = $errores;
            $this->redirigir('/login');
            return;
        }

        // 4. Buscar el usuario en la base de datos
        $usuario = $this->modeloUsuario->buscarPorCorreo($correo);

        // 5. Verificar existencia y contraseña
        if (!$usuario || !$this->modeloUsuario->verificarContrasena($contrasena, $usuario['contrasena'])) {
            $_SESSION['errores_login'] = ['Correo o contraseña incorrectos.'];
            $this->redirigir('/login');
            return;
        }

        // 6. Autenticación exitosa → guardar en sesión y redirigir
        $this->iniciarSesionUsuario($usuario);
        $this->redirigir('/panel');
    }

    // ──────────────────────────────────────────
    // MÉTODOS PRIVADOS (orden alfabético)
    // ──────────────────────────────────────────

    /**
     * Verifica si el usuario tiene una sesión activa
     *
     * @return bool true si está autenticado
     */
    private function estaAutenticado(): bool
    {
        return isset($_SESSION['usuario']);
    }

    /**
     * Genera y almacena un token CSRF en la sesión
     *
     * @return void
     */
    private function generarTokenCsrf(): void
    {
        if (empty($_SESSION['_token'])) {
            $_SESSION['_token'] = bin2hex(random_bytes(32));
        }
    }

    /**
     * Almacena un mensaje de error en la sesión
     *
     * @param string $clave Clave del error
     * @param string $mensaje Mensaje de error
     * @return void
     */
    private function guardarError(string $clave, string $mensaje): void
    {
        $_SESSION['errores_' . $clave] = [$mensaje];
    }

    /**
     * Guarda los datos del usuario autenticado en la sesión
     *
     * @param array $usuario Datos del usuario desde la BD
     * @return void
     */
    private function iniciarSesionUsuario(array $usuario): void
    {
        // Regenerar ID de sesión por seguridad (previene Session Fixation)
        session_regenerate_id(true);

        $_SESSION['usuario'] = [
            'id'     => $usuario['id'],
            'nombre' => $usuario['nombre'],
            'correo' => $usuario['correo'],
        ];
    }

    /**
     * Redirige a la URL especificada y termina la ejecución
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
     * Valida los campos del formulario de login
     *
     * @param string $correo     Correo ingresado
     * @param string $contrasena Contraseña ingresada
     * @return array Lista de errores (vacía si no hay errores)
     */
    private function validarCamposLogin(string $correo, string $contrasena): array
    {
        $errores = [];

        if (empty($correo)) {
            $errores[] = 'El correo electrónico es requerido.';
        } elseif (!filter_var($correo, FILTER_VALIDATE_EMAIL)) {
            $errores[] = 'El formato del correo electrónico no es válido.';
        }

        if (empty($contrasena)) {
            $errores[] = 'La contraseña es requerida.';
        }

        return $errores;
    }

    /**
     * Valida el token CSRF de la petición
     *
     * @param string $tokenRecibido Token enviado desde el formulario
     * @return bool true si el token es válido
     */
    private function validarTokenCsrf(string $tokenRecibido): bool
    {
        return isset($_SESSION['_token']) && hash_equals($_SESSION['_token'], $tokenRecibido);
    }
}

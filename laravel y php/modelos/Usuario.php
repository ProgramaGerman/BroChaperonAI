<?php
/**
 * ARCHIVO: modelos/Usuario.php
 * DESCRIPCION: Modelo de usuario — gestiona la interacción con la tabla `usuarios` en BD
 * AUTOR: German Gonzalez
 * FECHA: 2026-02-24
 *
 * Tamaño: MEDIANO-GRANDE
 * Orden: C - Después de la configuración y el núcleo
 *
 * RESPONSABILIDAD: Solo lógica de datos del usuario (patrón Active Record simplificado)
 */

require_once __DIR__ . '/../config/base_datos.php';

// ─────────────────────────────────────────────
// CLASE USUARIO (Modelo)
// ─────────────────────────────────────────────

class Usuario
{
    /** @var PDO Conexión activa a la base de datos */
    private PDO $conexion;

    // ──────────────────────────────────────────
    // CONSTRUCTOR
    // ──────────────────────────────────────────

    /**
     * Constructor: establece la conexión PDO al arrancar el modelo
     */
    public function __construct()
    {
        $this->conexion = $this->conectar();
    }

    // ──────────────────────────────────────────
    // MÉTODOS PÚBLICOS (orden alfabético)
    // ──────────────────────────────────────────

    /**
     * Busca un usuario por su dirección de correo electrónico
     *
     * @param string $correo Correo electrónico a buscar
     * @return array|false Datos del usuario o false si no existe
     */
    public function buscarPorCorreo(string $correo): array|false
    {
        $consulta = $this->conexion->prepare(
            'SELECT id, nombre, correo, contrasena, creado_en 
             FROM usuarios 
             WHERE correo = :correo 
             LIMIT 1'
        );

        $consulta->execute([':correo' => $correo]);
        return $consulta->fetch(PDO::FETCH_ASSOC);
    }

    /**
     * Verifica si un correo ya existe en la base de datos
     *
     * @param string $correo Correo a verificar
     * @return bool true si ya existe, false si está disponible
     */
    public function correoExiste(string $correo): bool
    {
        $consulta = $this->conexion->prepare(
            'SELECT COUNT(*) FROM usuarios WHERE correo = :correo'
        );

        $consulta->execute([':correo' => $correo]);
        return (int) $consulta->fetchColumn() > 0;
    }

    /**
     * Crea (registra) un nuevo usuario en la base de datos
     *
     * @param string $nombre    Nombre completo del usuario
     * @param string $correo    Correo electrónico (único)
     * @param string $contrasena Contraseña en texto plano (se hashea aquí)
     * @return bool true si fue creado exitosamente
     */
    public function crear(string $nombre, string $correo, string $contrasena): bool
    {
        // Hash seguro de la contraseña usando bcrypt
        $hash = password_hash($contrasena, PASSWORD_BCRYPT, ['cost' => 12]);

        $consulta = $this->conexion->prepare(
            'INSERT INTO usuarios (nombre, correo, contrasena, creado_en) 
             VALUES (:nombre, :correo, :contrasena, NOW())'
        );

        return $consulta->execute([
            ':nombre'     => trim($nombre),
            ':correo'     => strtolower(trim($correo)),
            ':contrasena' => $hash,
        ]);
    }

    /**
     * Verifica si la contraseña ingresada coincide con el hash almacenado
     *
     * @param string $contrasenaIngresada Contraseña en texto plano del usuario
     * @param string $hashAlmacenado      Hash guardado en la BD
     * @return bool true si la contraseña es correcta
     */
    public function verificarContrasena(string $contrasenaIngresada, string $hashAlmacenado): bool
    {
        return password_verify($contrasenaIngresada, $hashAlmacenado);
    }

    // ──────────────────────────────────────────
    // MÉTODOS PRIVADOS (orden alfabético)
    // ──────────────────────────────────────────

    /**
     * Establece y retorna la conexión PDO a la base de datos
     *
     * @throws PDOException Si la conexión falla
     * @return PDO Instancia de conexión
     */
    private function conectar(): PDO
    {
        $dsn = sprintf(
            '%s:host=%s;port=%s;dbname=%s;charset=%s',
            BD_MOTOR,
            BD_HOST,
            BD_PUERTO,
            BD_NOMBRE,
            BD_CHARSET
        );

        $opciones = [
            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES   => false,
        ];

        return new PDO($dsn, BD_USUARIO, BD_CONTRASENA, $opciones);
    }
}

<?php
/**
 * ARCHIVO: nucleo/Enrutador.php
 * DESCRIPCION: Motor de enrutamiento — procesa la URL y despacha el controlador correcto
 * AUTOR: German Gonzalez
 * FECHA: 2026-02-24
 *
 * Tamaño: MEDIANO
 * Orden: B - Segundo en cargarse, después de la config
 * 
 * PRINCIPIO: SRP (Single Responsibility Principle)
 *   → Esta clase SÓLO se encarga de enrutar peticiones HTTP
 */

// ─────────────────────────────────────────────
// CLASE ENRUTADOR
// ─────────────────────────────────────────────

class Enrutador
{
    /** @var array Lista de rutas GET registradas */
    private array $rutasGet = [];

    /** @var array Lista de rutas POST registradas */
    private array $rutasPost = [];

    // ──────────────────────────────────────────
    // MÉTODOS PÚBLICOS (orden alfabético)
    // ──────────────────────────────────────────

    /**
     * Despacha la petición actual al controlador correspondiente
     * 
     * @return void
     */
    public function despachar(): void
    {
        // Obtener la URI actual sin parámetros
        $uri    = $this->obtenerUri();
        $metodo = $_SERVER['REQUEST_METHOD'];

        // Buscar la ruta en el listado correspondiente
        if ($metodo === 'GET' && isset($this->rutasGet[$uri])) {
            $this->ejecutarAccion($this->rutasGet[$uri]);
            return;
        }

        if ($metodo === 'POST' && isset($this->rutasPost[$uri])) {
            $this->ejecutarAccion($this->rutasPost[$uri]);
            return;
        }

        // Ruta no encontrada → error 404
        $this->mostrarError404();
    }

    /**
     * Registra una ruta GET en el enrutador
     *
     * @param string $uri  La URI a registrar (ej: '/login')
     * @param array  $accion Arreglo [Controlador::class, 'metodo']
     * @return self
     */
    public function get(string $uri, array $accion): self
    {
        $this->rutasGet[$uri] = $accion;
        return $this;
    }

    /**
     * Registra una ruta POST en el enrutador
     *
     * @param string $uri  La URI a registrar (ej: '/login')
     * @param array  $accion Arreglo [Controlador::class, 'metodo']
     * @return self
     */
    public function post(string $uri, array $accion): self
    {
        $this->rutasPost[$uri] = $accion;
        return $this;
    }

    // ──────────────────────────────────────────
    // MÉTODOS PRIVADOS (orden alfabético)
    // ──────────────────────────────────────────

    /**
     * Ejecuta la acción de un controlador dado
     *
     * @param array $accion [Controlador::class, 'metodo']
     * @return void
     */
    private function ejecutarAccion(array $accion): void
    {
        [$controlador, $metodo] = $accion;
        $instancia = new $controlador();
        $instancia->$metodo();
    }

    /**
     * Obtiene la URI limpia de la petición actual
     *
     * @return string URI limpia sin query params
     */
    private function obtenerUri(): string
    {
        $uri = $_SERVER['REQUEST_URI'] ?? '/';
        return strtok($uri, '?'); // Eliminar parámetros GET
    }

    /**
     * Muestra una página de error 404 personalizada
     *
     * @return void
     */
    private function mostrarError404(): void
    {
        http_response_code(404);
        echo '<div style="font-family:sans-serif;text-align:center;padding:50px;">';
        echo '<h1>404 - Página No Encontrada</h1>';
        echo '<p>La ruta solicitada no existe.</p>';
        echo '<a href="/">← Volver al inicio</a>';
        echo '</div>';
    }
}

/**
 * ARCHIVO: servidor.js
 * DESCRIPCION: Servidor de demostración Node.js que replica el comportamiento
 *              del sistema PHP de autenticación (Login y Registro).
 *              Usa SOLO módulos nativos de Node.js — sin dependencias externas.
 * AUTOR: German Gonzalez
 * FECHA: 2026-02-24
 *
 * USO: node servidor.js
 *      Luego abrir: http://localhost:8000
 *
 * NOTA: Este servidor es equivalente a ejecutar:
 *       php -S localhost:8000 -t publico/
 */

"use strict";

// ─────────────────────────────────────────────
// MÓDULOS NATIVOS DE NODE.JS
// ─────────────────────────────────────────────
const http = require("http");
const fs = require("fs");
const path = require("path");
const url = require("url");

// ─────────────────────────────────────────────
// CONFIGURACIÓN DEL SERVIDOR
// ─────────────────────────────────────────────

/** @type {number} Puerto del servidor */
const PUERTO = 8000;

/** @type {string} Host del servidor */
const HOST = "localhost";

/** @type {Map} Almacén de sesiones en memoria (simula $_SESSION de PHP) */
const sesiones = new Map();

/** @type {Map} Base de datos en memoria (simula MySQL) */
const usuarios = new Map();

// ─────────────────────────────────────────────
// UTILIDADES (orden alfabético)
// ─────────────────────────────────────────────

/**
 * Lee el CSS de estilos del proyecto PHP
 * @returns {string} Contenido del archivo CSS
 */
function leerCss() {
  try {
    return fs.readFileSync(
      path.join(__dirname, "publico", "css", "estilos.css"),
      "utf8",
    );
  } catch {
    return "";
  }
}

/**
 * Genera la cabecera HTML común (replica plantilla.php)
 * @param {string} titulo - Título de la página
 * @returns {string} HTML del encabezado
 */
function encabezado(titulo) {
  return `<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Sistema de autenticación seguro con PHP y Laravel">
    <meta name="author" content="German Gonzalez">
    <title>${titulo} | AuthSistema</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>${leerCss()}</style>
</head>
<body>`;
}

/**
 * Genera el pie de página HTML (replica piePagina de plantilla.php)
 * @returns {string} HTML del pie de página
 */
function piePagina() {
  const anio = new Date().getFullYear();
  return `
    <footer class="pie">
        <p>&copy; ${anio} AuthSistema &mdash; Desarrollado por <strong>German Gonzalez</strong></p>
    </footer>
</body>
</html>`;
}

/**
 * Genera un token CSRF aleatorio
 * @returns {string} Token de 64 caracteres hex
 */
function generarToken() {
  return require("crypto").randomBytes(32).toString("hex");
}

/**
 * Obtiene o crea la sesión del usuario desde la cookie
 * @param {http.IncomingMessage} req - Petición HTTP
 * @returns {{id: string, datos: object}} Sesión del usuario
 */
function obtenerSesion(req) {
  const cookieHeader = req.headers.cookie || "";
  const match = cookieHeader.match(/sesion_id=([^;]+)/);
  const sesionId = match ? match[1] : null;

  if (sesionId && sesiones.has(sesionId)) {
    return { id: sesionId, datos: sesiones.get(sesionId) };
  }

  // Crear nueva sesión
  const nuevoId = require("crypto").randomBytes(16).toString("hex");
  const datos = { _token: generarToken() };
  sesiones.set(nuevoId, datos);
  return { id: nuevoId, datos };
}

/**
 * Hash simple de contraseña (simula password_hash de PHP con bcrypt)
 * @param {string} contrasena - Contraseña en texto plano
 * @returns {string} Hash de la contraseña
 */
function hashContrasena(contrasena) {
  return require("crypto")
    .createHash("sha256")
    .update(contrasena + "salt_german_2026")
    .digest("hex");
}

/**
 * Parsea el cuerpo de una petición POST
 * @param {http.IncomingMessage} req - Petición HTTP
 * @returns {Promise<object>} Datos del formulario
 */
function parsearCuerpo(req) {
  return new Promise((resolve) => {
    let cuerpo = "";
    req.on("data", (chunk) => {
      cuerpo += chunk.toString();
    });
    req.on("end", () => {
      const params = new URLSearchParams(cuerpo);
      const datos = {};
      for (const [clave, valor] of params.entries()) {
        datos[clave] = valor;
      }
      resolve(datos);
    });
  });
}

/**
 * Valida los datos del formulario de registro
 * @param {string} nombre - Nombre del usuario
 * @param {string} correo - Correo electrónico
 * @param {string} contrasena - Contraseña
 * @param {string} confirmar - Confirmación de contraseña
 * @returns {string[]} Lista de errores
 */
function validarRegistro(nombre, correo, contrasena, confirmar) {
  const errores = [];

  if (!nombre || nombre.trim().length < 3)
    errores.push("El nombre debe tener al menos 3 caracteres.");

  if (!correo || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo))
    errores.push("El formato del correo electrónico no es válido.");

  if (!contrasena || contrasena.length < 8)
    errores.push("La contraseña debe tener al menos 8 caracteres.");
  else if (!/[A-Z]/.test(contrasena))
    errores.push("La contraseña debe contener al menos una letra mayúscula.");
  else if (!/[0-9]/.test(contrasena))
    errores.push("La contraseña debe contener al menos un número.");

  if (contrasena !== confirmar) errores.push("Las contraseñas no coinciden.");

  return errores;
}

// ─────────────────────────────────────────────
// VISTAS HTML (réplicas de las vistas PHP)
// ─────────────────────────────────────────────

/**
 * Renderiza la vista de la página de login
 * @param {object} sesion - Datos de sesión actual
 * @returns {string} HTML completo de la página de login
 */
function vistaLogin(sesion) {
  const errores = sesion.datos.errores_login || [];
  const exitoReg = sesion.datos.exito_registro || "";
  delete sesion.datos.errores_login;
  delete sesion.datos.exito_registro;

  const alertaExito = exitoReg
    ? `<div class="alerta alerta-exito" role="alert">
               <span class="alerta-icono">✅</span>
               ${exitoReg}
           </div>`
    : "";

  const alertaError = errores.length
    ? `<div class="alerta alerta-error" role="alert">
               <span class="alerta-icono">⚠️</span>
               <ul class="lista-errores">
                   ${errores.map((e) => `<li>${e}</li>`).join("")}
               </ul>
           </div>`
    : "";

  return `${encabezado("Iniciar Sesión")}
<main class="contenedor-auth">
    <div class="tarjeta-auth">
        <div class="encabezado-tarjeta">
            <div class="icono-auth">🔐</div>
            <h1 class="titulo-auth">Iniciar Sesión</h1>
            <p class="subtitulo-auth">Bienvenido de nuevo — ingresa tus credenciales</p>
        </div>
        ${alertaExito}
        ${alertaError}
        <form id="formulario-login" class="formulario" action="/login" method="POST" novalidate>
            <input type="hidden" name="_token" value="${sesion.datos._token}">
            <div class="grupo-campo">
                <label class="etiqueta" for="correo">📧 Correo Electrónico</label>
                <input id="correo" class="campo" type="email" name="correo"
                    placeholder="tu@correo.com" autocomplete="email" required>
            </div>
            <div class="grupo-campo">
                <label class="etiqueta" for="contrasena">🔑 Contraseña</label>
                <div class="campo-con-icono">
                    <input id="contrasena" class="campo" type="password" name="contrasena"
                        placeholder="Tu contraseña segura" autocomplete="current-password" required>
                    <button type="button" class="btn-ojo"
                        onclick="alternarContrasena('contrasena')" title="Ver contraseña">👁</button>
                </div>
            </div>
            <button id="btn-login" class="btn-primario" type="submit">
                <span class="btn-texto">Iniciar Sesión</span>
                <span class="btn-cargando" hidden>Verificando...</span>
            </button>
        </form>
        <div class="pie-tarjeta">
            <p>¿No tienes cuenta? <a id="enlace-registro" class="enlace" href="/registro">Regístrate gratis</a></p>
        </div>
    </div>
</main>
<script>
function alternarContrasena(id) {
    const c = document.getElementById(id);
    c.type = c.type === 'password' ? 'text' : 'password';
}
document.getElementById('formulario-login').addEventListener('submit', function() {
    document.querySelector('.btn-texto').hidden    = true;
    document.querySelector('.btn-cargando').hidden = false;
});
</script>
${piePagina()}`;
}

/**
 * Renderiza la vista del formulario de registro
 * @param {object} sesion - Datos de sesión actual
 * @returns {string} HTML completo de la página de registro
 */
function vistaRegistro(sesion) {
  const errores = sesion.datos.errores_registro || [];
  const anterior = sesion.datos.datos_registro || {};
  delete sesion.datos.errores_registro;
  delete sesion.datos.datos_registro;

  const alertaError = errores.length
    ? `<div class="alerta alerta-error" role="alert">
               <span class="alerta-icono">⚠️</span>
               <ul class="lista-errores">
                   ${errores.map((e) => `<li>${e}</li>`).join("")}
               </ul>
           </div>`
    : "";

  return `${encabezado("Crear Cuenta")}
<main class="contenedor-auth">
    <div class="tarjeta-auth tarjeta-registro">
        <div class="encabezado-tarjeta">
            <div class="icono-auth">✨</div>
            <h1 class="titulo-auth">Crear Cuenta</h1>
            <p class="subtitulo-auth">Únete hoy — es gratis y rápido</p>
        </div>
        ${alertaError}
        <form id="formulario-registro" class="formulario" action="/registro" method="POST" novalidate>
            <input type="hidden" name="_token" value="${sesion.datos._token}">
            <div class="grupo-campo">
                <label class="etiqueta" for="nombre">👤 Nombre Completo</label>
                <input id="nombre" class="campo" type="text" name="nombre"
                    value="${anterior.nombre || ""}" placeholder="Tu nombre completo"
                    autocomplete="name" maxlength="100" required>
            </div>
            <div class="grupo-campo">
                <label class="etiqueta" for="correo">📧 Correo Electrónico</label>
                <input id="correo" class="campo" type="email" name="correo"
                    value="${anterior.correo || ""}" placeholder="tu@correo.com"
                    autocomplete="email" required>
            </div>
            <div class="grupo-campo">
                <label class="etiqueta" for="contrasena">🔑 Contraseña</label>
                <div class="campo-con-icono">
                    <input id="contrasena" class="campo" type="password" name="contrasena"
                        placeholder="Mínimo 8 caracteres, 1 mayúscula, 1 número"
                        autocomplete="new-password" minlength="8" required>
                    <button type="button" class="btn-ojo"
                        onclick="alternarContrasena('contrasena')">👁</button>
                </div>
                <div class="barra-fortaleza-contenedor" hidden id="barra-contenedor">
                    <div id="barra-fortaleza" class="barra-fortaleza"></div>
                    <span id="texto-fortaleza" class="texto-fortaleza"></span>
                </div>
            </div>
            <div class="grupo-campo">
                <label class="etiqueta" for="confirmar_contrasena">🔒 Confirmar Contraseña</label>
                <div class="campo-con-icono">
                    <input id="confirmar_contrasena" class="campo" type="password"
                        name="confirmar_contrasena" placeholder="Repite tu contraseña"
                        autocomplete="new-password" required>
                    <button type="button" class="btn-ojo"
                        onclick="alternarContrasena('confirmar_contrasena')">👁</button>
                </div>
            </div>
            <button id="btn-registro" class="btn-primario" type="submit">
                <span class="btn-texto">🚀 Crear Mi Cuenta</span>
                <span class="btn-cargando" hidden>Registrando...</span>
            </button>
        </form>
        <div class="pie-tarjeta">
            <p>¿Ya tienes cuenta? <a id="enlace-login" class="enlace" href="/login">Inicia sesión aquí</a></p>
        </div>
    </div>
</main>
<script>
function alternarContrasena(id) {
    const c = document.getElementById(id);
    c.type = c.type === 'password' ? 'text' : 'password';
}
function calcularFortaleza(p) {
    let s = 0;
    if (p.length >= 8)           s++;
    if (/[A-Z]/.test(p))         s++;
    if (/[0-9]/.test(p))         s++;
    if (/[^A-Za-z0-9]/.test(p)) s++;
    return s;
}
document.getElementById('contrasena').addEventListener('input', function() {
    const cont = document.getElementById('barra-contenedor');
    const bar  = document.getElementById('barra-fortaleza');
    const txt  = document.getElementById('texto-fortaleza');
    if (!this.value) { cont.hidden = true; return; }
    cont.hidden = false;
    const s       = calcularFortaleza(this.value);
    const niveles = ['', 'debil', 'media', 'buena', 'fuerte'];
    const textos  = ['', '😟 Muy débil', '😐 Media', '😊 Buena', '💪 Fuerte'];
    bar.className   = 'barra-fortaleza nivel-' + (niveles[s] || 'debil');
    txt.textContent = textos[s] || textos[1];
});
document.getElementById('formulario-registro').addEventListener('submit', function() {
    document.querySelector('.btn-texto').hidden    = true;
    document.querySelector('.btn-cargando').hidden = false;
});
</script>
${piePagina()}`;
}

/**
 * Renderiza la vista del panel del usuario autenticado
 * @param {object} usuario - Datos del usuario logueado {nombre, correo}
 * @returns {string} HTML completo del panel
 */
function vistaPanel(usuario) {
  const inicial = usuario.nombre.charAt(0).toUpperCase();
  const anio = new Date().getFullYear();

  return `${encabezado("Panel")}
<main class="contenedor-panel">
    <nav class="barra-nav">
        <div class="nav-marca">🔐 AuthSistema</div>
        <div class="nav-usuario">
            <span class="nav-nombre">👋 ${usuario.nombre}</span>
            <a id="btn-logout" class="btn-cerrar-sesion" href="/logout">Cerrar Sesión</a>
        </div>
    </nav>
    <div class="panel-contenido">
        <div class="tarjeta-bienvenida">
            <div class="avatar">${inicial}</div>
            <div class="bienvenida-info">
                <h1 class="titulo-panel">¡Bienvenido, ${usuario.nombre}! 🎉</h1>
                <p class="correo-panel">📧 ${usuario.correo}</p>
                <span class="insignia-activo">✅ Sesión Activa</span>
            </div>
        </div>
        <div class="cuadricula-info">
            <div class="tarjeta-info">
                <div class="tarjeta-info-icono">🔑</div>
                <h2 class="tarjeta-info-titulo">Autenticación</h2>
                <p class="tarjeta-info-desc">Sesión activa y protegida con tokens CSRF y hashing seguro.</p>
            </div>
            <div class="tarjeta-info">
                <div class="tarjeta-info-icono">🛡️</div>
                <h2 class="tarjeta-info-titulo">Seguridad</h2>
                <p class="tarjeta-info-desc">Contraseñas hasheadas y protección contra Session Fixation.</p>
            </div>
            <div class="tarjeta-info">
                <div class="tarjeta-info-icono">⚡</div>
                <h2 class="tarjeta-info-titulo">Performance</h2>
                <p class="tarjeta-info-desc">Sistema liviano con arquitectura MVC PHP limpia y ordenada.</p>
            </div>
        </div>
    </div>
</main>
<footer class="pie">
    <p>&copy; ${anio} AuthSistema &mdash; Desarrollado por <strong>German Gonzalez</strong></p>
</footer>
</body></html>`;
}

// ─────────────────────────────────────────────
// MANEJADOR DE PETICIONES HTTP
// ─────────────────────────────────────────────

/**
 * Manejador principal de peticiones HTTP — equivalente al enrutador PHP
 * @param {http.IncomingMessage} req - Petición entrante
 * @param {http.ServerResponse}  res - Respuesta a enviar
 */
async function manejarPeticion(req, res) {
  const parsedUrl = url.parse(req.url);
  const ruta = parsedUrl.pathname;
  const metodo = req.method;

  // Obtener sesión del usuario
  const sesion = obtenerSesion(req);

  // Configurar cookie de sesión en la respuesta
  const cookieOpciones = `sesion_id=${sesion.id}; HttpOnly; Path=/; SameSite=Strict`;

  // Función helper para responder con HTML
  const responderHtml = (html, codigo = 200) => {
    res.writeHead(codigo, {
      "Content-Type": "text/html; charset=utf-8",
      "Set-Cookie": cookieOpciones,
    });
    res.end(html);
  };

  // Función helper para redirigir
  const redirigir = (destino) => {
    res.writeHead(302, {
      Location: destino,
      "Set-Cookie": cookieOpciones,
    });
    res.end();
  };

  console.log(`[${new Date().toLocaleTimeString("es-VE")}] ${metodo} ${ruta}`);

  // ──────────────────────────────────────────
  // ENRUTAMIENTO (equivalente a rutas/web.php)
  // ──────────────────────────────────────────

  // GET / → redirigir a /login
  if (ruta === "/" && metodo === "GET") {
    return redirigir("/login");
  }

  // GET /login → mostrar formulario de login
  if (ruta === "/login" && metodo === "GET") {
    if (sesion.datos.usuario) return redirigir("/panel");
    return responderHtml(vistaLogin(sesion));
  }

  // POST /login → procesar inicio de sesión
  if (ruta === "/login" && metodo === "POST") {
    const datos = await parsearCuerpo(req);

    // Validar token CSRF
    if (datos._token !== sesion.datos._token) {
      sesion.datos.errores_login = [
        "Token de seguridad inválido. Recarga la página.",
      ];
      return redirigir("/login");
    }

    const correo = (datos.correo || "").trim().toLowerCase();
    const contrasena = datos.contrasena || "";

    // Validar campos
    if (!correo || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo)) {
      sesion.datos.errores_login = [
        "El formato del correo electrónico no es válido.",
      ];
      return redirigir("/login");
    }
    if (!contrasena) {
      sesion.datos.errores_login = ["La contraseña es requerida."];
      return redirigir("/login");
    }

    // Buscar usuario
    const usuario = usuarios.get(correo);
    if (!usuario || usuario.contrasena !== hashContrasena(contrasena)) {
      sesion.datos.errores_login = ["Correo o contraseña incorrectos."];
      return redirigir("/login");
    }

    // Login exitoso
    sesion.datos.usuario = { nombre: usuario.nombre, correo: usuario.correo };
    sesion.datos._token = generarToken(); // Regenerar token por seguridad
    return redirigir("/panel");
  }

  // GET /registro → mostrar formulario de registro
  if (ruta === "/registro" && metodo === "GET") {
    if (sesion.datos.usuario) return redirigir("/panel");
    return responderHtml(vistaRegistro(sesion));
  }

  // POST /registro → procesar registro de nuevo usuario
  if (ruta === "/registro" && metodo === "POST") {
    const datos = await parsearCuerpo(req);

    // Validar CSRF
    if (datos._token !== sesion.datos._token) {
      sesion.datos.errores_registro = ["Token de seguridad inválido."];
      return redirigir("/registro");
    }

    const nombre = (datos.nombre || "").trim();
    const correo = (datos.correo || "").trim().toLowerCase();
    const contra = datos.contrasena || "";
    const confirmar = datos.confirmar_contrasena || "";

    // Guardar para repoblar formulario
    sesion.datos.datos_registro = { nombre, correo };

    // Validar datos
    const errores = validarRegistro(nombre, correo, contra, confirmar);
    if (errores.length) {
      sesion.datos.errores_registro = errores;
      return redirigir("/registro");
    }

    // Verificar correo duplicado
    if (usuarios.has(correo)) {
      sesion.datos.errores_registro = [
        "Este correo electrónico ya está en uso.",
      ];
      return redirigir("/registro");
    }

    // Crear usuario
    usuarios.set(correo, {
      nombre,
      correo,
      contrasena: hashContrasena(contra),
    });

    delete sesion.datos.datos_registro;
    sesion.datos.exito_registro = `¡Cuenta creada exitosamente! Ya puedes iniciar sesión.`;
    sesion.datos._token = generarToken();

    console.log(`  ✅ Usuario registrado: ${nombre} <${correo}>`);
    return redirigir("/login");
  }

  // GET /panel → panel protegido
  if (ruta === "/panel" && metodo === "GET") {
    if (!sesion.datos.usuario) return redirigir("/login");
    return responderHtml(vistaPanel(sesion.datos.usuario));
  }

  // GET /logout → cerrar sesión
  if (ruta === "/logout" && metodo === "GET") {
    sesiones.delete(sesion.id);
    res.writeHead(302, {
      Location: "/login",
      "Set-Cookie": `sesion_id=; HttpOnly; Path=/; Max-Age=0`,
    });
    return res.end();
  }

  // 404 — Ruta no encontrada
  res.writeHead(404, { "Content-Type": "text/html; charset=utf-8" });
  res.end(`<div style="font-family:sans-serif;text-align:center;padding:50px;background:#0f0f1a;color:#f1f5f9;min-height:100vh">
        <h1 style="font-size:3rem">404</h1>
        <p>Página no encontrada</p>
        <a href="/login" style="color:#6366f1">← Volver al inicio</a>
    </div>`);
}

// ─────────────────────────────────────────────
// INICIAR EL SERVIDOR
// ─────────────────────────────────────────────

const servidor = http.createServer(manejarPeticion);

servidor.listen(PUERTO, HOST, () => {
  console.log("\n╔══════════════════════════════════════════════╗");
  console.log("║       AuthSistema | Login y Registro         ║");
  console.log("║       Desarrollado por German Gonzalez        ║");
  console.log("╚══════════════════════════════════════════════╝\n");
  console.log(`✅ Servidor iniciado exitosamente`);
  console.log(`🌐 Abre en tu navegador: http://${HOST}:${PUERTO}/login\n`);
  console.log("Rutas disponibles:");
  console.log(`  http://${HOST}:${PUERTO}/login     → Iniciar Sesión`);
  console.log(`  http://${HOST}:${PUERTO}/registro  → Crear Cuenta`);
  console.log(`  http://${HOST}:${PUERTO}/panel     → Panel (requiere login)`);
  console.log(`  http://${HOST}:${PUERTO}/logout    → Cerrar Sesión`);
  console.log("\nPresiona Ctrl+C para detener\n");
  console.log("─────────────────────────────────────────");
});

# Sistema de Autenticación - Laravel & PHP

## Proyecto: Login y Registro

> Creado por: German Gonzalez
> Versión: 1.0.0
> Fecha: 2026-02-24

---

## 📁 Estructura del Proyecto (orden alfabético + tamaño ascendente)

```
laravel-auth/
├── config/
│   └── base_datos.php          [config pequeña]
├── migraciones/
│   └── crear_tabla_usuarios.php [migración]
├── modelos/
│   └── Usuario.php              [modelo]
├── controladores/
│   ├── AuthControlador.php      [controlador auth]
│   └── RegistroControlador.php  [controlador registro]
├── vistas/
│   ├── plantilla.php            [plantilla base]
│   ├── login.php                [vista login]
│   └── registro.php             [vista registro]
├── rutas/
│   └── web.php                  [definición de rutas]
├── nucleo/
│   └── Enrutador.php            [motor de rutas]
├── publico/
│   ├── css/
│   │   └── estilos.css          [estilos globales]
│   └── index.php                [punto de entrada]
└── README.md
```

---

## 🚀 Instalación Rápida

### Requisitos

- PHP >= 8.1
- MySQL o SQLite
- Composer (opcional para dependencias)

### Pasos

```bash
# 1. Clonar o descargar el proyecto
cd laravel-auth

# 2. Configurar la base de datos en config/base_datos.php
# 3. Ejecutar migración
php migraciones/crear_tabla_usuarios.php

# 4. Iniciar servidor integrado de PHP
php -S localhost:8000 -t publico/
```

### 5. Abrir el navegador

```
http://localhost:8000
```

---

## 🔐 Características

- ✅ Registro de usuarios con validación
- ✅ Login seguro con hash de contraseña
- ✅ Sesiones PHP nativas
- ✅ Protección CSRF básica
- ✅ Código en español
- ✅ Organización alfabética y por tamaño

---

## 📝 Licencia

MIT - German Gonzalez © 2026

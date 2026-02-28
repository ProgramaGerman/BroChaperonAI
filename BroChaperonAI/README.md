# 💬 BroChaperonAI

> _Tu copiloto de conversaciones. Analiza capturas de pantalla de chats y genera respuestas perfectas para cada situación._

---

## ¿Qué es?

**BroChaperonAI** es una herramienta de escritorio que usa **inteligencia artificial multimodal** para leer capturas de pantalla de conversaciones y sugerirte la respuesta ideal. Solo sube la imagen, elige tu estilo y copia la respuesta generada.

Sin rodeos. Sin pensar demasiado. Solo resultados.

---

## Modos de Respuesta

| Modo                 | Descripción                                    |
| -------------------- | ---------------------------------------------- |
| 🔥 **Provocativo**   | Alta tensión emocional y picardía calculada    |
| 💕 **Enamorar**      | Respuestas profundas, románticas y vulnerables |
| ⚡ **Salvada Épica** | Salidas ingeniosas para situaciones incómodas  |
| 😏 **Coquetear**     | Tono lúdico, ligero y con humor sutil          |

---

## Tecnologías

- **Python 3.13+** — tipado estático avanzado
- **CustomTkinter** — interfaz moderna con modo oscuro nativo
- **OpenRouter API** — modelos de visión multimodal (Qwen VL, Gemini, etc.)
- **Pillow** — procesamiento de imágenes
- **httpx** — cliente HTTP asíncrono
- **python-dotenv** — gestión segura de credenciales

---

## Arquitectura

El proyecto sigue el patrón **Modelo-Vista-Presentador (MVP)**:

```
BroChaperonAI/
├── app/
│   ├── models/
│   │   ├── ai_engine.py        ← Llamadas a OpenRouter (lógica de IA)
│   │   └── image_processor.py  ← Carga, resize y thumbnail de imágenes
│   ├── presenters/
│   │   └── chat_presenter.py   ← Orquesta Vista ↔ Modelos en hilos
│   └── views/
│       └── main_window.py      ← UI dark mode con CustomTkinter
├── tests/
│   └── test_suite.py           ← 7 pruebas unitarias (unittest)
├── assets/themes/
├── main.py
├── requirements.txt
└── pyproject.toml
```

---

## Instalación

```powershell
# Clonar / abrir el proyecto
cd BroChaperonAI

# Instalar dependencias
uv add customtkinter httpx Pillow python-dotenv

# Configurar API key (crear archivo .env)
echo OPENROUTER_API_KEY=sk-or-xxxxxxxxxx > .env

# Ejecutar
uv run py main.py
```

---

## Uso

1. **Abre la app** → ventana en modo oscuro.
2. **Haz clic en 📷 CARGAR PANTALLAZО** → selecciona tu captura de pantalla.
3. **Elige un modo** (🔥 💕 ⚡ 😏) → la IA analiza la imagen y genera la respuesta.
4. **Copia** con 📋 COPIAR RESPUESTA y pégala donde quieras.

---

## Pruebas

```powershell
python -m unittest tests/test_suite.py -v
# Ran 7 tests in ~0.7s — OK
```

---

## Licencia

Proyecto personal. Todos los derechos reservados © 2026 German Gonzalez.

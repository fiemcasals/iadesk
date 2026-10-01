# 🧠 Memoria y Lineamientos del Módulo: `presentacion/`

> Base de conocimiento y objetivos del módulo de diapositivas de IA Desk.

## 🎯 Objetivos de `presentacion/`
- Explicar didácticamente cómo se construye el sistema IA Desk desde cero.
- Enfocar la narrativa en:
  1. El framework web Django (MTV, `settings.py`, `urls.py`, `views.py`).
  2. La integración oficial del SDK de Anthropic Claude (`client.messages.create`).
  3. La seguridad estricta y gestión de API Keys mediante `.env` y variables de entorno.
  4. La mecánica de Tool Calling (bucle `tool_use` -> ejecución local -> `tool_result`).
  5. La memoria en 3 capas (`INDEX.md`, `MEMORY.md`, `CHAT_HISTORY.json`).

## 📌 Decisiones y Acuerdos de Diseño
- Formato: Diapositivas HTML autónomas interactivas (estilo presentación moderna Keynote/Reveal).
- Controles: Teclas de flecha, barra espaciadora, pantalla completa (`F`), dots inferiores, barra de progreso y botón de pestaña completa.

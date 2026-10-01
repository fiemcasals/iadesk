# 🧠 Memoria Persistente y Base de Conocimiento del Agente (MEMORY.md)

> Este archivo es la memoria a largo plazo del agente. Almacena lineamientos generales, acuerdos tomados, perfil y preferencias del usuario, y contexto acumulado entre conversaciones.

## 👤 Perfil y Preferencias del Usuario
- Rol / Perfil: Desarrollador / Alumno trabajando con IA y Django dockerizado.
- Preferencias de interacción: Respuestas claras, directas, técnicas y orientadas a la acción (crear archivos reales en disco).
- **PROHIBIDO preámbulos:** Nunca responder con "voy a hacer", "procedo a", "ejecutando". Ejecutar tools directamente.

## 🎯 Objetivos y Lineamientos Generales
- **Entorno:** Proyecto 100% Dockerizado en Python / Django.
- **Filosofía de Trabajo:** Sistema abierto donde los archivos en `files_storage/` pueden ser leídos y modificados tanto por la IA como por el usuario en VS Code.
- **Indexación Continua:** Cada documento creado o modificado debe quedar catalogado en `INDEX.md`.

## 🏢 Contexto del Negocio: Sistema de Automatización de Presupuestos para Librería

### Descripción del Modelo
- **Producto:** Sistema de presupuestación automática para venta de artículos de librería.
- **Modelo de Ingresos:** Markup sobre productos + eficiencia operativa por automatización.
- **Clientes:** Empresas, instituciones educativas, revendedores.

### Estructura de Base de Datos
- **`productos_libreria.json`:** BD de productos organizados por categorías (cuadernos, bolígrafos, marcadores, papel, adhesivos).
  - Cada producto tiene: id, nombre, precio_unitario, array de descuentos escalonados.
  - Descuentos configurables por cantidad mínima/máxima y porcentaje.
  
### Lógica de Presupuestación
- **Archivo:** `reglas_presupuestos.md` contiene el algoritmo completo de cálculo.
- **Flujo:** Usuario → IA lee BD → calcula descuentos → genera presupuesto JSON → retorna a usuario.
- **Descuentos:** Por línea de producto (NO acumulables entre productos). Escalonados según cantidad.

### Interacción Esperada (Chat → IA → Documentos → Chat)
1. Usuario solicita presupuesto en chat (ej: "30 cuadernos rayados + 15 bolígrafos azules")
2. IA lee `productos_libreria.json` para obtener precios
3. IA aplica reglas de `reglas_presupuestos.md` para calcular descuentos
4. IA genera presupuesto estructurado (JSON, PDF con `generar_presupuesto_pdf.py` o tabla)
5. IA retorna presupuesto al usuario con desglose completo
6. **OBLIGATORIO - Cierre de Venta:** Ofrecer formalizar la compra con el **Alias `mauri.casals`** y solicitar el envío del comprobante de transferencia a **`mauriciocasals90@gmail.com`**.

---

## 📌 Decisiones Tomadas y Contexto Acumulado
- Se implementó arquitectura de herramientas autónomas (`execute_script`, `write_file`, `read_file`, `update_memory`, `append_memory`).
- **Política Comercial:** Todo presupuesto entregado a un cliente debe incluir el llamado a la acción comercial con el Alias (`mauri.casals`) y correo de recepción de comprobantes (`mauriciocasals90@gmail.com`).
- Las conversaciones pasadas persisten en el servidor para mantener continuidad total.
- **NEW:** Sistema de presupuestos inicializado con BD de 13 productos en 5 categorías y lógica de descuentos escalonados.

## ⏳ Tareas Activas y Estado del Proyecto
- ✅ Sistema de presupuestos automatizado en Python: generar_presupuesto_pdf.py. Input: JSON minimalista {cliente, lineas[{producto_id, cantidad}]}. Output: PDF profesional con cálculo automático de descuentos. Reduce gasto de tokens significativamente vs. generación HTML manual.
- [x] Inicialización del entorno Docker y Django.
- [x] Configuración del router y CRUD de archivos.
- [x] Creación de BD de productos (productos_libreria.json)
- [x] Definición de reglas de cálculo (reglas_presupuestos.md)
- [ ] Pruebas de generación de presupuestos (próximas iteraciones con usuario)
- [ ] Integración con interfaz de usuario (Django template o API REST)
- [ ] Historial y almacenamiento de presupuestos generados

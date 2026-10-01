# 🗂️ Índice Maestro y Router de Documentos (INDEX.md)

> Catálogo semántico que la IA consulta primero para decidir qué archivos cargar antes de responder.

## 📋 Catálogo Semántico de Documentos

| Archivo | Temas y Palabras Clave | Resumen del Contenido | Cuándo Consultar |
| :--- | :--- | :--- | :--- |
| `INDEX.md` | `índice, catálogo, router, estructura, metadatos, enrutamiento` | Catálogo semántico de documentos con rutas de acceso y reglas de enrutamiento automático para la IA | Consulta primero al procesar cualquier pregunta del usuario para identificar qué documentos leer |
| `MEMORY.md` | `memoria`, `lineamientos`, `perfil`, `decisiones`, `contexto`, `negocio` | Memoria persistente del agente: perfil del usuario, objetivos, decisiones técnicas, contexto del negocio. | Antes de responder cualquier pregunta, para respetar lineamientos y mantener coherencia. |
| `tips_productividad.md` | `productividad, pomodoro, priorización, tiempo, hábitos, eficiencia` | Recopilación de técnicas y estrategias para mejorar la productividad personal y laboral. | Consulta cuando necesites consejos para optimizar tu flujo de trabajo o quieras implementar nuevas técnicas de gestión de tiempo. |
| `tips_aprendizaje.md` | `aprendizaje, memoria, spaced repetition, interleaving, técnica Feynman, active recall, estudio` | Estrategias y técnicas basadas en neurociencia para aprender de forma más efectiva y retener información a largo plazo. | Consulta cuando busques mejorar tus métodos de estudio o necesites técnicas científicas para aprender mejor. |
| `tareasfuturas.md` | `tareas, pendientes, roadmap, seguimiento, estado, prioridades` | Lista de tareas futuras, prioridades y estado de avance del proyecto. | Consulta para revisar tareas pendientes, prioridades y estado general del proyecto. |
| `productos_libreria.json` | `productos, librería, cuadernos, bolígrafos, marcadores, papel, adhesivos, precios, descuentos, cantidad, BD` | Base de datos de artículos de librería organizados por categorías, con precios unitarios y descuentos escalonados por cantidad. | Consulta al crear presupuestos, buscar productos, validar precios o aplicar descuentos automáticos según cantidad. |
| `reglas_presupuestos.md` | `presupuestos, cálculo, descuentos, algoritmo, lógica, automatización, librería, cliente` | Algoritmo completo de cálculo de presupuestos: validación, búsqueda de descuento, cálculo de montos y generación de respuesta. Incluye ejemplos. | Consulta cuando generes un presupuesto, necesites aplicar descuentos, o valides el cálculo de un total. |

---

| `presupuesto_mauricio_casals.html` | `presupuesto, cliente, mauricio casals, PDF, HTML, descarga, botón, exportar, factura` | Presupuesto HTML para Mauricio Casals con botón de descarga PDF integrado | Cuando necesites exportar presupuestos a PDF con diseño profesional. Incluye botones para descargar PDF y imprimir directamente. |

| `presupuesto_lodi_benetti.html` | `presupuesto, cliente, lodi benetti, PDF, HTML, descarga, botón, exportar` | Presupuesto HTML para Lodi Benetti con botón de descarga PDF integrado | Cuando necesites exportar presupuestos a PDF con diseño profesional. Incluye botones para descargar PDF e imprimir directamente. |

| `generar_presupuesto_pdf.py` | `presupuesto, PDF, ReportLab, JSON, automatización, generador` | Script Python para generar presupuestos en PDF desde JSON minimalista | Consultas sobre generar_presupuesto_pdf.py |

| `ejemplo_presupuesto.json` | `ejemplo, JSON, presupuesto, entrada, datos` | Ejemplo de JSON minimalista para generar presupuestos | Como referencia para estructurar datos de entrada al script generar_presupuesto_pdf.py |

| `DOCUMENTACION_PRESUPUESTOS.md` | `presupuesto, PDF, ReportLab, documentación, uso, API, JSON` | Documentación completa del script generador de presupuestos en PDF | Cuando necesites entender cómo usar generar_presupuesto_pdf.py o configurar un flujo de presupuestación automatizado |

| `setup_venv.sh` | `venv, setup, bash, virtual environment, reportlab, instalación` | Script bash para crear venv e instalar reportlab automáticamente | Ejecutar en terminal para crear y activar el venv con todas las dependencias listas |

| `setup_venv.bat` | `venv, setup, batch, windows, virtual environment, reportlab, instalación` | Script batch para crear venv e instalar reportlab automáticamente (Windows) | Ejecutar en CMD/PowerShell de Windows para crear y activar el venv con todas las dependencias |

| `PROCEDIMIENTO_GENERAR_PDF.md` | `presupuesto, PDF, procedimiento, venv, automatización, script, bash, batch, flujo, ejecución` | Procedimiento estándar completo para generar presupuestos en PDF: scripts bash/batch, flujo automatizado, checklist y troubleshooting | Cuando necesites generar un presupuesto en PDF o necesites entender el flujo completo automatizado para presupuestos |

| `presupuesto_rossi.json` | `presupuesto, rossi, JSON, entrada, datos` | JSON de presupuesto para Rossi: 50 rotuladores permanentes + 10 cuadernos | Input para generar presupuesto_rossi.pdf |

| `presupuesto_nicolas_gomez.json` | `presupuesto, nicolas gomez, JSON, entrada` | JSON minimalista para presupuesto Nicolas Gomez: 5 cuadernos rayados + 10 bolígrafos gel | Input para generar presupuesto_nicolas_gomez.pdf |
| `presentacion/` | `presentacion, slides, powerpoint, arquitectura, django, api, keys, tutorial, clase` | Módulo de presentación interactiva con diapositivas animadas explicando paso a paso la arquitectura Django, integración de Claude API y seguridad de Keys | Consultas sobre cómo explicar o enseñar la arquitectura y construcción del sistema |

| `presupuesto_bruno_monzon.json` | `presupuesto, bruno monzon, JSON, lápices, cuadernos` | JSON de presupuesto para Bruno Monzon: 30 lápices gel + 10 cuadernos espiral | Input para generar presupuesto_bruno_monzon.pdf |

| `presupuesto_esteban_lopez.json` | `presupuesto, esteban lopez, cuadernos, bolígrafos, JSON` | Presupuesto para Esteban López: 20 cuadernos + 15 bolígrafos | Input para generar presupuesto_esteban_lopez.pdf con generar_presupuesto_pdf.py |

## 🏷️ Reglas de Mantenimiento para la IA:
1. Cada vez que generes o edites un archivo en este directorio, agrega o actualiza su fila en la tabla anterior.
2. En **Temas y Palabras Clave**, coloca sinónimos y términos de búsqueda para facilitar el enrutamiento.
3. En **Cuándo Consultar**, describe de forma concisa el tipo de preguntas que resuelve este archivo.

---

## 🔄 Flujo de Interacción: Chat → IA → Documentos → IA → Chat

**Ejemplo práctico del sistema de presupuestos:**

1. **Usuario en chat:** "Necesito presupuesto para 30 cuadernos rayados A4 y 15 cajas de bolígrafos azules"
2. **IA ejecuta:** 
   - Lee `INDEX.md` (ubicación de documentos relevantes)
   - Lee `productos_libreria.json` (obtiene precios de CUA001 y BOL001)
   - Lee `reglas_presupuestos.md` (aplica algoritmo de descuentos)
3. **IA calcula:**
   - CUA001: 30 unid × $2.50 con descuento 10% = $67.50
   - BOL001: 15 unid × $5.00 con descuento 10% = $67.50
   - Total: $135.00 (ahorro: $15.00)
4. **IA responde:** Presupuesto detallado en tabla/JSON con desglose de precios, descuentos y totales

---

## 🎯 Documentos Estructurales (NO modificar)
- `INDEX.md` - Este archivo (router central)
- `MEMORY.md` - Memoria persistente del agente

## 📄 Documentos de Negocio (actualizables)
- `productos_libreria.json` - BD de productos
- `reglas_presupuestos.md` - Lógica de cálculo

## 📚 Documentos de Referencia (actualizables)
- `tips_productividad.md`
- `tips_aprendizaje.md`
- `tareasfuturas.md`

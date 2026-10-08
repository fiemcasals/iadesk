# 🗂️ Índice Maestro General (INDEX.md)

> Router semántico principal del catálogo multirubro. La IA consulta este índice primero para redirigir la solicitud al módulo específico correspondiente.

## 📋 Catálogo de Módulos y Carpetas

| Carpeta / Módulo | Temas y Palabras Clave | Resumen del Contenido | Cuándo Consultar |
| :--- | :--- | :--- | :--- |
| `libreria/` | `libro`, `cuaderno`, `lapiz`, `borrador`, `regla`, `resma`, `hojas`, `libreria`, `escolar`, `oficina` | Precios y stock de artículos de librería y papelería técnica | Al consultar por útiles, hojas o material de oficina |
| `indumentaria/` | `remera`, `pantalon`, `buzo`, `camisa`, `campera`, `ropa`, `uniforme`, `calzado` | Precios y stock de indumentaria laboral, informal y calzado | Al consultar por prendas de vestir o uniformes |
| `carniceria/` | `carne`, `pollo`, `pescado`, `asado`, `milanesa`, `vacio`, `lomo`, `alimentos` | Precios por kilo y disponibilidad de cortes cárnicos frescos | Al consultar por cortes de carne o menú gastronómico |

## 🏷️ Reglas de Enrutamiento
1. Si el cliente pregunta por un insumo específico (ej: *"cuaderno más barato"*), identificar primero el módulo correspondiente (`libreria/`).
2. Abrir el `INDEX.md` del módulo local o ejecutar la Tool de base de datos SQL sobre la categoría.
3. Aplicar las directrices de `MEMORY.md` para el tono y estilo comercial.

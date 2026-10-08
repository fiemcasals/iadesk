# 📚 Guía y Manual de la Clase 8: Skills de IA, Router Jerárquico, SQL y Memoria Adaptativa

Bienvenido al módulo **`clase8/10-skill`**. Esta guía detalla cómo está estructurada la clase, el orden recomendado de lectura, cómo inicializar los componentes y cómo ejecutar las pruebas tanto en consola como en la interfaz web interactiva.

---

## 🧭 1. Cómo Leer y Estudiar este Módulo (Ruta de Aprendizaje)

Para aprovechar al máximo el contenido pedagógico y técnico, sigue este orden:

```text
1. 📄 plaDeClases.md        ➔  Plan pedagógico, objetivos y cronograma (120 min).
2. 📊 presentacion_clase8.html ➔  Diapositivas interactivas con simulador en vivo.
3. 📁 sample_storage/       ➔  Estructura de índices jerárquicos (libreria, indumentaria, carniceria).
4. 🗄️ catalogo_db.py        ➔  Motor SQLite, esquema relacional y queries ordenadas.
5. 🧠 skills_engine.py      ➔  Orquestador de habilidades, análisis léxico (Mirroring) y permisos.
```

### 📂 Mapa de Archivos del Módulo

| Archivo / Carpeta | Propósito y Contenido |
| :--- | :--- |
| **[plaDeClases.md](file:///c:/Users/mcasals/Desktop/cideso/personal/clases/clasesIA/iaDesk/clase8/10-skill/plaDeClases.md)** | **Plan Maestro:** Detalle bloque por bloque de la clase, teoría de Skills vs. Prompts monolíticos, y guión de ejercicios. |
| **[presentacion_clase8.html](file:///c:/Users/mcasals/Desktop/cideso/personal/clases/clasesIA/iaDesk/clase8/10-skill/presentacion_clase8.html)** | **Presentación Interactiva:** Slide deck en modo oscuro con simulador de ejecución en tiempo real y visor de código con botón de copiado. |
| **[catalogo_db.py](file:///c:/Users/mcasals/Desktop/cideso/personal/clases/clasesIA/iaDesk/clase8/10-skill/catalogo_db.py)** | **Base de Datos:** Inicializa SQLite (`catalogo.sqlite3`), introspección de esquema (`PRAGMA table_info`) y búsqueda del producto más económico (`ORDER BY precio ASC LIMIT 1`). |
| **[skills_engine.py](file:///c:/Users/mcasals/Desktop/cideso/personal/clases/clasesIA/iaDesk/clase8/10-skill/skills_engine.py)** | **Motor de Skills:** Implementa `RouterJerarquicoSkill`, `CatalogoSQLSkill`, `AsesorVentasSkill` y `SkillManager`. |
| **[sample_storage/](file:///c:/Users/mcasals/Desktop/cideso/personal/clases/clasesIA/iaDesk/clase8/10-skill/sample_storage/)** | **Sistema de Archivos Modular:** Contiene los `INDEX.md` y `MEMORY.md` del router general y de cada submódulo. |

---

## 🚀 2. Cómo Inicializar el Entorno y Ejecutar

No se requieren dependencias externas adicionales, ya que el motor utiliza la biblioteca estándar de Python (`sqlite3`, `re`, `json`, `pathlib`).

### Paso A: Inicializar la Base de Datos de Catálogo
Ejecuta el script de base de datos para crear la estructura relacional y poblar los insumos de ejemplo:

```powershell
# En Windows (PowerShell / CMD) o Linux / macOS
python clase8/10-skill/catalogo_db.py
```

*¿Qué hace este comando?*
1. Crea el archivo `catalogo.sqlite3` si no existe.
2. Crea las tablas `categorias` e `insumos`.
3. Carga los productos de librería, indumentaria y carnicería con precios y stock.
4. Muestra en pantalla el esquema introspeccionado y una consulta de prueba.

---

### Paso B: Ejecutar el Motor de Skills y el Asesor de Ventas
Ejecuta el orquestador principal para probar el pipeline completo de habilidades:

```powershell
python clase8/10-skill/skills_engine.py
```

*Salida generada:*
- **Matcher:** Identifica las skills pertinentes (`RouterJerarquicoSkill`, `CatalogoSQLSkill`, `AsesorVentasSkill`).
- **Router:** Lee el `INDEX.md` raíz y navega al módulo específico (`libreria/`).
- **SQL Tool:** Genera y ejecuta `SELECT * FROM insumos WHERE ... ORDER BY precio ASC LIMIT 1`.
- **Mirroring:** Detecta el tono informal del usuario y adapta el saludo y cierre.
- **Permisos:** Consulta `MEMORY.md` para respetar autorizaciones previas sin repreguntar.
- **Respuesta Bonita:** Emite la cotización clara y vendedora con precio ($95.00) y stock (250 unidades).

---

## 🧪 3. Pruebas Rápidas de Tono (Mirroring) y Rubros

Puedes ejecutar directamente desde la terminal diferentes variantes de pruebas:

### 🔹 Prueba 1: Tono Formal (Módulo Indumentaria)
```powershell
python -c "import sys; sys.path.insert(0, 'clase8/10-skill'); from skills_engine import SkillManager; m = SkillManager(); print(m.process_prompt('Estimado, solicito cotizacion de la remera mas barata')['resultado_asesor']['respuesta_sugerida'])"
```
> **Respuesta:** Adapta el saludo a *"Estimado/a, le presento la cotización más conveniente disponible..."* con cierre protocolar.

### 🔹 Prueba 2: Tono Informal (Módulo Carnicería)
```powershell
python -c "import sys; sys.path.insert(0, 'clase8/10-skill'); from skills_engine import SkillManager; m = SkillManager(); print(m.process_prompt('Hola che, pasame el asado mas barato que tengas')['resultado_asesor']['respuesta_sugerida'])"
```
> **Respuesta:** Adapta el saludo a *"¡Qué tal! Acá tenés la mejor opción económica..."* con llamada a la acción cercana.

---

## 📊 4. Cómo Abrir y Usar la Presentación Interactiva

La presentación [presentacion_clase8.html](file:///c:/Users/mcasals/Desktop/cideso/personal/clases/clasesIA/iaDesk/clase8/10-skill/presentacion_clase8.html) está diseñada para proyectar en clase o estudiar de forma autónoma.

### Opción 1: Directo en el Navegador
- Haz doble clic o abre con tu navegador preferido:
  `clase8/10-skill/presentacion_clase8.html`

### Opción 2: Desde la Aplicación Web Django
1. Levanta el servidor local o Docker (`python manage.py runserver` o `docker compose up`).
2. Entra a `http://localhost:8000/app/`.
3. En la barra superior, haz clic en el botón morado: **`📊 Clase 8 (Skills)`** (o accede directo a `http://localhost:8000/app/clase8/`).

### ⌨️ Atajos de la Presentación:
- **`➡` / Barra Espaciadora:** Avanzar a la siguiente diapositiva.
- **`⬅`:** Retroceder diapositiva.
- **`⛶ Pantalla Completa`:** Botón superior derecho para modo presentación.
- **`Simulador Interactivo (Slide 6)`:** Escribe cualquier consulta o presiona los botones de prueba para ver el pipeline ejecutándose en vivo.
- **`Visor de Códigos (Slide 7)`:** Alterna entre pestañas para inspeccionar y copiar el código de cada archivo con un solo clic.

---

## 🧠 5. Resumen de Conceptos Clave para la Clase

1. **Desacoplamiento mediante Skills:** En lugar de saturar el *System Prompt* con miles de instrucciones, creamos componentes autónomos que validan su activación (`match`) y ejecutan su lógica (`execute`).
2. **Router Jerárquico de Índices:** La IA solo lee el catálogo general `INDEX.md` para elegir la subcarpeta adecuada (`libreria/`, `indumentaria/`, etc.) y luego carga el archivo puntual. Esto ahorra hasta un 80% de tokens de contexto.
3. **Cálculos Numéricos con SQL:** Las comparaciones de precios o filtros de stock no se delegan a la intuición del LLM; se resuelven de forma determinística con `SELECT ... ORDER BY precio ASC LIMIT 1`.
4. **Memoria Continua y Permisos:** `MEMORY.md` almacena las preferencias aprendidas del cliente. Si ya autorizó un procedimiento, la IA nunca debe volver a repreguntarlo.

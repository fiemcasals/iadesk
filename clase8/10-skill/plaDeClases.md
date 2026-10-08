# 🎓 Plan de Clase 8: Skills Especializadas de IA, Router Jerárquico, Consultas SQL y Memoria Adaptativa

**Módulo:** Inteligencia Artificial Aplicada y Agentes Autónomos  
**Tema:** Arquitectura de *Skills*, Navegación Jerárquica de Índices (`INDEX.md`), Consultas Estructuradas a Bases de Datos (SQL Tools) y Memoria Adaptativa con *Mirroring* y Gestión de Permisos.  
**Duración:** 120 minutos (2 horas)  
**Modalidad:** Teórico-Práctica con Live Coding y Simulación Interactiva  

---

## 🎯 1. Objetivos Pedagógicos

Al finalizar la clase, el estudiante será capaz de:
1. **Comprender el concepto de *Skill* (Habilidad Especializada):** Diferenciar entre un System Prompt genérico y una habilidad modular que encapsula herramientas, lógica de activación (*matchers*) y formato de salida.
2. **Implementar un Router Jerárquico de Documentos:** Diseñar un sistema de índices Markdown multinivel (`INDEX.md` raíz $\rightarrow$ `libreria/INDEX.md`, `indumentaria/INDEX.md`, `carniceria/INDEX.md`) que ahorra hasta un 80% de tokens en contextos extensos.
3. **Integrar el Agente con Bases de Datos Relacionales (SQL Tooling):** Configurar la introspección de esquemas (`DESCRIBE` / `PRAGMA table_info`) y la generación de sentencias SQL precisas como `SELECT * FROM insumos WHERE ... ORDER BY precio ASC LIMIT 1`.
4. **Desarrollar Memoria Adaptativa con *Mirroring* y Persistencia de Permisos:** Programar el agente para que analice el estilo léxico del usuario (formal vs. informal), adapte su tono y recuerde autorizaciones otorgadas sin volver a repreguntar.
5. **Formular Respuestas Comerciales Pulidas ("Respuestas Bonitas"):** Estructurar cotizaciones y recomendaciones persuasivas, con stock, precio y llamados a la acción claros.

---

## 📂 2. Estructura de Archivos de la Clase (`clase8/10-skill/`)

```text
clase8/10-skill/
├── plaDeClases.md                 # 📖 Plan de clase pedagógico exhaustivo
├── README.md                      # 🚀 Guía rápida de ejecución y enlaces
├── catalogo_db.py                 # 🗄️ Base de datos SQLite, esquema (DESCRIBE) y queries
├── skills_engine.py               # 🧠 Motor de Skills: Router, SQL, Asesor y Memoria
├── presentacion_clase8.html       # 📊 Presentación interactiva en diapositivas con simulador
└── sample_storage/                # 📁 Sistema de archivos con jerarquía modular
    ├── INDEX.md                   # Índice General (Router Semántico multirubro)
    ├── MEMORY.md                  # Memoria General y Políticas de Permisos
    ├── libreria/
    │   ├── INDEX.md               # Catálogo e insumos de librería
    │   └── MEMORY.md              # Reglas y criterios específicos de librería
    ├── indumentaria/
    │   └── INDEX.md               # Catálogo de indumentaria comercial
    └── carniceria/
        └── INDEX.md               # Catálogo de carnicería y alimentos
```

---

## ⏱️ 3. Cronograma y Desarrollo Detallado de la Clase

### 🕒 Bloque 1: Arquitectura de Skills y Concepto Modular (20 min)
- **Problema:** Un prompt gigante con todas las funciones satura el contexto del LLM y degrada la precisión.
- **Solución:** Arquitectura de *Skills*. Cada Skill cuenta con:
  - **Metadata:** Nombre, descripción y versión.
  - **Matcher (`match`):** Lógica rápida que evalúa si el prompt del usuario requiere esta habilidad.
  - **Executor (`execute`):** Invocación de herramientas (Tools), llamadas a API o consultas SQL.
- **Comparativa visual:** Monolito vs. Agente Modular con Registro de Skills.

### 🕒 Bloque 2: Router Jerárquico de Carpetas e Índices (25 min)
- **Concepto:** Cómo navegar estructuras de datos sin cargar todos los archivos a memoria.
- **Flujo de Ejecución:**
  1. El usuario pregunta: *"Quiero saber cuál es el cuaderno más barato"*.
  2. El **RouterJerarquicoSkill** lee únicamente el `INDEX.md` raíz.
  3. Detecta que la palabra `cuaderno` mapea al módulo `libreria/`.
  4. Carga bajo demanda `sample_storage/libreria/INDEX.md` sin tocar `indumentaria/` ni `carniceria/`.
- **Ejercicio en Vivo:** Probar el ruteo en consola con `python -m clase8.10-skill.skills_engine`.

### 🕒 Bloque 3: Consultas SQL y Búsqueda de Insumos Óptimos (30 min)
- **El reto:** Las comparaciones de precios o filtros numéricos en texto libre suelen fallar en los LLM.
- **La solución:** Delegar el cálculo a un motor relacional (SQLite) mediante **SQL Tooling**.
- **Paso 1: Introspección del Esquema:**
  ```sql
  PRAGMA table_info(insumos);
  -- Permite a la IA saber que existen las columnas: id, nombre, descripcion, precio, stock, categoria_id
  ```
- **Paso 2: Generación del Query Óptimo:**
  ```sql
  SELECT * FROM insumos 
  WHERE LOWER(nombre) LIKE '%cuaderno%' OR LOWER(palabras_relacionadas) LIKE '%cuaderno%' 
  ORDER BY precio ASC 
  LIMIT 1;
  ```
- **Resultado:** La base de datos devuelve exactamente el producto más económico: *Cuaderno económico escolar a $95*.

### 🕒 Bloque 4: Memoria Adaptativa, Espejado Léxico (Mirroring) y Permisos (25 min)
- **Análisis de Estilo del Cliente:**
  - Si el usuario dice *"hola che tenes cuadernos baratos"*, la IA detecta tono **informal_cercano** y responde: *"¡Qué tal! Acá tenés la mejor opción..."*.
  - Si el usuario dice *"Estimado, solicito cotización formal"*, la IA detecta tono **formal_ejecutivo** y responde: *"Estimado/a, le presento la cotización correspondiente..."*.
- **Gestión Inteligente de Permisos:**
  - Si el usuario ya autorizó cotizaciones directas o envío de comprobantes, se registra en `MEMORY.md`.
  - **Regla estricta:** La IA lee `MEMORY.md` y **no vuelve a preguntar** lo que ya fue acordado.

### 🕒 Bloque 5: Integración, Demostración y Pruebas en Vivo (20 min)
- Ejecución completa del pipeline en `presentacion_clase8.html` y en la terminal.
- Visualización interactiva del flujo en la presentación HTML.
- Espacio para preguntas y respuestas.

---

## 🧪 4. Guión de Pruebas y Ejercicios Prácticos

### 🔹 Caso de Prueba 1: Búsqueda de Insumo más Barato (Librería)
- **Prompt:** `"Hola, quiero saber cuál es el cuaderno más barato"`
- **Flujo esperado:**
  1. Activación de `RouterJerarquicoSkill` $\rightarrow$ Módulo `libreria/`.
  2. Activación de `CatalogoSQLSkill` $\rightarrow$ Ejecuta query `ORDER BY precio ASC LIMIT 1`.
  3. Activación de `AsesorVentasSkill` $\rightarrow$ Genera "Respuesta Bonita" con producto de $95.

### 🔹 Caso de Prueba 2: Adaptación de Tono (Mirroring)
- **Prompt Formal:** `"Estimado, agradecería me informe los precios y stock de remeras de trabajo"`
- **Resultado:** Respuesta con vocabulario protocolar, estructura corporativa y llamado formal.
- **Prompt Informal:** `"Hola, pasame el precio del asado para el finde"`
- **Resultado:** Respuesta cálida, cercana y directa con stock disponible en carnicería.

### 🔹 Caso de Prueba 3: Comprobación de Permisos sin Repreguntar
- **Prompt:** `"Te doy permiso para que en todas las cotizaciones incluyas el stock disponible y presupuestes en pesos sin pedirme confirmación."`
- **Acción:** La IA actualiza `MEMORY.md` con la clave `permiso: cotizacion_directa`.
- **Siguiente Prompt:** `"Cotizame 10 resmas A4"`
- **Resultado:** La IA emite el presupuesto directamente sin realizar preguntas redundantes de confirmación.

---

## 💻 5. Comandos de Ejecución

### Ejecutar prueba rápida en consola:
```bash
python clase8/10-skill/skills_engine.py
```

### Inicializar / Consultar la Base de Datos SQLite:
```bash
python clase8/10-skill/catalogo_db.py
```

### Ver la Presentación Interactiva:
- Abrir en el navegador: [presentacion_clase8.html](file:///c:/Users/mcasals/Desktop/cideso/personal/clases/clasesIA/iaDesk/clase8/10-skill/presentacion_clase8.html)
- O navegar en Django a: `http://localhost:8000/clase8/` (si el servidor está corriendo).

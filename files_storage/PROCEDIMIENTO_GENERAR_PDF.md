# 📋 Procedimiento Estándar: Generar Presupuesto en PDF

> Flujo completo y documentado para generar presupuestos en PDF de forma automatizada y estandarizada.

---

## 🎯 Cuándo Usar Este Procedimiento

**Usuario solicita:** "Necesito presupuesto para X productos"

**IA debe ejecutar este flujo:**
1. ✅ Leer `productos_libreria.json`
2. ✅ Validar productos y cantidades
3. ✅ Crear JSON de entrada minimalista
4. ✅ Ejecutar script Python
5. ✅ Entregar PDF al usuario

---

## 📝 Paso a Paso: Procedimiento Automático

### **PASO 1: Validar Productos y Crear JSON**

Ejemplo - Usuario pide: "40 lapiceras baratas y 20 cuadernos baratos"

**IA selecciona los más económicos:**
- `BOL003` → Bolígrafo Gel Premium ($1.20/unid) - MÁS BARATO
- `CUA002` → Cuaderno Cuadriculado ($2.00/unid) - MÁS BARATO

**IA crea el JSON:**
```json
{
  "cliente": "Nombre Del Cliente",
  "lineas": [
    {"producto_id": "BOL003", "cantidad": 40},
    {"producto_id": "CUA002", "cantidad": 20}
  ]
}
```

---

### **PASO 2: Ejecutar el Script (Bash - Linux/macOS)**

```bash
#!/bin/bash

# Variables
VENV_DIR="venv"
SCRIPT="generar_presupuesto_pdf.py"
JSON_INPUT="presupuesto_entrada.json"  # El archivo JSON creado en PASO 1
PDF_OUTPUT="presupuesto_salida.pdf"

# 1. Crear venv si no existe
if [ ! -d "$VENV_DIR" ]; then
  echo "📦 Creando venv..."
  python3 -m venv "$VENV_DIR"
  echo "✅ venv creado"
fi

# 2. Activar venv
echo "🔌 Activando venv..."
source "$VENV_DIR/bin/activate"

# 3. Instalar reportlab si no está
echo "📚 Verificando reportlab..."
pip install -q reportlab

# 4. Ejecutar script
echo "⚙️  Generando PDF..."
python "$SCRIPT" "$JSON_INPUT" "$PDF_OUTPUT"

# 5. Verificar resultado
if [ -f "$PDF_OUTPUT" ]; then
  echo "✅ PDF generado exitosamente: $PDF_OUTPUT"
else
  echo "❌ Error al generar PDF"
  deactivate
  exit 1
fi

# 6. Desactivar venv
echo "🔌 Desactivando venv..."
deactivate

echo "✨ Procedimiento completado"
```

**Guardar como:** `generar_pdf.sh`

**Ejecutar:**
```bash
chmod +x generar_pdf.sh
./generar_pdf.sh
```

---

### **PASO 3: Ejecutar el Script (Batch - Windows)**

```batch
@echo off
setlocal enabledelayedexpansion

REM Variables
set VENV_DIR=venv
set SCRIPT=generar_presupuesto_pdf.py
set JSON_INPUT=presupuesto_entrada.json
set PDF_OUTPUT=presupuesto_salida.pdf

REM 1. Crear venv si no existe
if not exist "%VENV_DIR%" (
  echo 📦 Creando venv...
  python -m venv "%VENV_DIR%"
  echo ✅ venv creado
)

REM 2. Activar venv
echo 🔌 Activando venv...
call "%VENV_DIR%\Scripts\activate.bat"

REM 3. Instalar reportlab
echo 📚 Verificando reportlab...
pip install -q reportlab

REM 4. Ejecutar script
echo ⚙️  Generando PDF...
python "%SCRIPT%" "%JSON_INPUT%" "%PDF_OUTPUT%"

REM 5. Verificar resultado
if exist "%PDF_OUTPUT%" (
  echo ✅ PDF generado exitosamente: %PDF_OUTPUT%
) else (
  echo ❌ Error al generar PDF
  deactivate
  exit /b 1
)

REM 6. Desactivar venv
echo 🔌 Desactivando venv...
deactivate

echo ✨ Procedimiento completado
endlocal
```

**Guardar como:** `generar_pdf.bat`

**Ejecutar:**
```cmd
generar_pdf.bat
```

---

## 🤖 Pseudo-Código: Cómo la IA Ejecuta Este Flujo

```
CUANDO usuario solicita presupuesto:

  1. READ "productos_libreria.json"
  2. FILTER productos_baratos_por_categoria()
  3. CREATE JSON minimalista con {cliente, lineas[]}
  4. WRITE JSON a disco (ej: presupuesto_entrada.json)
  5. EXECUTE script según SO:
       - Linux/macOS: bash generar_pdf.sh
       - Windows: call generar_pdf.bat
  6. VERIFY PDF fue creado en disco
  7. RETURN "Presupuesto generado: presupuesto_salida.pdf"

CUANDO usuario pide solo cotización (NO PDF):
  - Mostrar tabla/resumen en chat
  - NO ejecutar script
  - Ahorrar tiempo y tokens
```

---

## 📊 Comparativa: Con PDF vs Sin PDF

| Escenario | Acción | Tokens Usados |
|-----------|--------|--------------|
| **Cotización rápida** | Solo tabla en chat | 🟢 **Mínimos** |
| **Presupuesto para exportar** | Ejecutar script → PDF | 🟡 **Bajos** (solo JSON) |
| **Múltiples presupuestos** | Batch: 5 JSONs → 5 PDFs | 🟢 **Muy eficiente** |

---

## ✅ Checklist: Antes de Ejecutar

- [ ] `generar_presupuesto_pdf.py` existe en el directorio
- [ ] `productos_libreria.json` existe y es válido
- [ ] Python 3.6+ instalado en el sistema
- [ ] Tengo permisos de escritura en el directorio
- [ ] Seleccioné los productos correctos del usuario

---

## 🔍 Troubleshooting

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError: reportlab` | Ejecutar: `pip install reportlab` |
| `FileNotFoundError: generar_presupuesto_pdf.py` | Verificar que el archivo existe en el directorio |
| `Permission denied` (Linux) | Ejecutar: `chmod +x generar_pdf.sh` |
| PDF vacío o corrupto | Revisar JSON de entrada (validar producto_id y cantidad) |

---

## 📝 Ejemplo Completo de Ejecución

### Usuario pide:
> "Presupuesto para 40 lapiceras y 20 cuadernos (los más baratos), exportar a PDF para Lodi Benetti"

### IA ejecuta:

**1. Selecciona productos baratos:**
```json
{
  "cliente": "Lodi Benetti",
  "lineas": [
    {"producto_id": "BOL003", "cantidad": 40},
    {"producto_id": "CUA002", "cantidad": 20}
  ]
}
```

**2. Guarda y ejecuta script:**
```bash
# En Linux/macOS
bash generar_pdf.sh

# En Windows
generar_pdf.bat
```

**3. Genera PDF automáticamente:**
- ✅ `presupuesto_salida.pdf` listo
- ✅ Detalles calculados automáticamente
- ✅ Descuentos aplicados según cantidad

**4. Responde al usuario:**
> ✅ Presupuesto generado: **presupuesto_salida.pdf**
> - 40 Bolígrafos Gel Premium: $42.40 (descuento 12%)
> - 20 Cuadernos Cuadriculado: $40.00
> - **Total: $82.20**

---

## 🎯 Decisiones de Diseño

- **Por qué venv temporal:** Evita contaminar el sistema, permite múltiples versiones de Python
- **Por qué JSON minimalista:** Reduce tokens, facilita auditoría, permite batch processing
- **Por qué scripts auto-contenidos:** No requieren intervención manual, automatizable en CI/CD
- **Por qué desactivar venv al final:** Limpia el estado, evita conflictos con próximas ejecuciones

---

## 🚀 Optimizaciones Futuras

- [ ] Guardar presupuestos en BD (SQLite/PostgreSQL)
- [ ] Generar batch de 10 PDFs en paralelo
- [ ] Integrar con API de envío de emails
- [ ] Agregar numeración automática de presupuestos
- [ ] Validación de cliente en CRM


# 📊 Documentación: Generador de Presupuestos en PDF

## 🎯 Objetivo

Script Python autónomo que genera presupuestos en PDF reduciendo gasto de tokens.

**Flujo:**
```
usuario → JSON minimalista → script .py → BD de productos → cálculos → PDF profesional
```

---

## 📥 Input: Estructura JSON Minimalista

```json
{
  "cliente": "Nombre del Cliente",
  "numero_presupuesto": "PRES-20250116-001",
  "lineas": [
    {
      "producto_id": "CUA001",
      "cantidad": 30
    },
    {
      "producto_id": "BOL001",
      "cantidad": 15
    }
  ]
}
```

### Campos Requeridos:
- **`cliente`** (string): Nombre del cliente
- **`lineas`** (array): Cada objeto con `producto_id` y `cantidad`

### Campos Opcionales:
- **`numero_presupuesto`** (string): Si no se proporciona, se genera automáticamente

---

## 📤 Output: PDF Profesional

Documento A4 con:
- ✅ Encabezado con número y fecha
- ✅ Datos del cliente
- ✅ Tabla detallada con cálculo automático de descuentos
- ✅ Resumen de totales (sin descuento, descuentos, total final)
- ✅ Diseño profesional y responsive

---

## 🚀 Cómo Usar

### 1. Instalación de Dependencias

```bash
pip install reportlab
```

### 2. Ejecutar el Script

```bash
python generar_presupuesto_pdf.py input.json output.pdf
```

### 3. Ejemplo Completo

```bash
# Crear archivo JSON
cat > presupuesto_cliente.json << 'EOF'
{
  "cliente": "Lodi Benetti",
  "lineas": [
    {"producto_id": "BOL003", "cantidad": 40},
    {"producto_id": "CUA002", "cantidad": 20}
  ]
}
EOF

# Generar PDF
python generar_presupuesto_pdf.py presupuesto_cliente.json presupuesto_lodi_benetti.pdf

# El script imprime:
# ✅ JSON con presupuesto completo (para auditoría/registro)
# ✅ Confirmación de PDF generado
```

---

## 🔄 Flujo Interno

1. **Lee `productos_libreria.json`** → Obtiene BD de productos
2. **Valida cada línea** → Busca producto por ID, verifica cantidad
3. **Calcula descuentos** → Aplica tramos de descuento automáticamente según cantidad
4. **Genera JSON interno** → Estructura completa con montos y ahorros
5. **Imprime JSON** → Para auditoría/registro en DB (opcional)
6. **Genera PDF** → Diseño profesional con ReportLab

---

## 📊 Ejemplo de Salida (JSON + PDF)

### JSON Impreso en Consola:
```json
{
  "numero_presupuesto": "PRES-20250116-0123",
  "fecha": "2025-01-16",
  "cliente": "Lodi Benetti",
  "lineas": [
    {
      "producto_id": "BOL003",
      "producto_nombre": "Bolígrafo Gel Premium",
      "cantidad": 40,
      "precio_unitario": 1.20,
      "descuento_porcentaje": 12,
      "precio_con_descuento": 1.06,
      "subtotal": 42.40,
      "ahorro": 5.80
    },
    {
      "producto_id": "CUA002",
      "producto_nombre": "Cuaderno Cuadriculado A4 80 Hojas",
      "cantidad": 20,
      "precio_unitario": 2.00,
      "descuento_porcentaje": 0,
      "precio_con_descuento": 2.00,
      "subtotal": 40.00,
      "ahorro": 0.00
    }
  ],
  "resumen": {
    "total_sin_descuento": 88.00,
    "total_descuentos": 5.80,
    "total_final": 82.20,
    "descuento_promedio_porcentaje": 6.59
  },
  "notas": "Presupuesto válido por 30 días"
}
```

### PDF Generado:
Documento profesional con tabla, resumen y datos del cliente.

---

## ⚙️ Configuración y Extensiones

### Cambiar Formato o Notas

Edita `generar_presupuesto_pdf.py`:

```python
# Línea ~250: Cambiar notas
'notas': 'Presupuesto válido por 30 días. Consulte términos y condiciones.'
```

### Agregar Logo o Encabezado Personalizado

Modifica la función `generar_pdf()` para insertar imagen de logo (usa `Image` de `reportlab.platypus`).

### Exportar a CSV Además de PDF

Agrega al final de `main()`:
```python
import csv
with open(archivo_output.replace('.pdf', '.csv'), 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['producto_id', 'cantidad', 'subtotal'])
    writer.writeheader()
    writer.writerows(presupuesto['lineas'])
```

---

## 🔐 Errores Comunes

| Error | Solución |
|-------|----------|
| `Archivo no encontrado` | Verifica la ruta del JSON de entrada |
| `Error al parsear JSON` | Valida sintaxis JSON (usa `python -m json.tool`) |
| `Producto no encontrado` | Revisa que `producto_id` existe en `productos_libreria.json` |
| `ModuleNotFoundError: reportlab` | Instala: `pip install reportlab` |

---

## 💰 Ventajas vs. HTML Manual

| Aspecto | HTML Manual | Script Python |
|--------|-----------|--------------|
| **Gasto de Tokens** | Alto (genero HTML completo) | Bajo (solo JSON) |
| **Formato Consistente** | Variable | Estandarizado |
| **Escalabilidad** | Manual por cliente | Batch (100+ presupuestos) |
| **Auditoría** | Difícil trackear | JSON guardado automáticamente |
| **Integración API** | No | Sí (se puede dockerizar) |

---

## 📋 Próximas Iteraciones

- [ ] Agregar logo de empresa en PDF
- [ ] Generar también en Excel (.xlsx)
- [ ] API REST para generar presupuestos (Django)
- [ ] Almacenar presupuestos en base de datos (historial)
- [ ] QR code con link al presupuesto online
- [ ] Envío automático por email

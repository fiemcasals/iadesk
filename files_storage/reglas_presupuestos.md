# 📊 Reglas y Lógica de Cálculo de Presupuestos

## 🎯 Objetivo del Sistema
Automatizar la generación de presupuestos para venta de artículos de librería con aplicación automática de descuentos por cantidad.

---

## 📐 Algoritmo de Cálculo

### Paso 1: Validación de Producto
1. Verificar que el producto existe en `productos_libreria.json`
2. Extraer `precio_unitario` de la categoría correspondiente
3. Si no existe, retornar error "Producto no encontrado"

### Paso 2: Búsqueda de Descuento Aplicable
```
Para cada línea de descuento:
  SI cantidad_solicitada >= cantidad_minima 
    Y (cantidad_maxima == null O cantidad_solicitada <= cantidad_maxima)
  ENTONCES
    descuento_aplicable = descuento_porcentaje
    ROMPER bucle
  FIN SI
FIN PARA
```

**Si no hay descuento aplicable:** descuento_aplicable = 0%

### Paso 3: Cálculo de Montos
```
precio_con_descuento = precio_unitario * (1 - descuento_porcentaje / 100)
subtotal_linea = precio_con_descuento * cantidad
ahorro_linea = precio_unitario * cantidad - subtotal_linea
```

### Paso 4: Totales del Presupuesto
```
total_sin_descuento = SUM(precio_unitario * cantidad) para todas las líneas
total_descuentos = SUM(ahorro_linea) para todas las líneas
total_final = total_sin_descuento - total_descuentos

porcentaje_descuento_promedio = (total_descuentos / total_sin_descuento) * 100
```

---

## 💰 Ejemplo de Cálculo

**Presupuesto: Cliente solicita 30 cuadernos rayados A4 + 15 bolígrafos azules**

### Línea 1: Cuadernos Rayados (CUA001)
- Producto: CUA001 (Cuaderno Rayado A4 100 Hojas)
- Cantidad: 30
- Precio unitario: $2.50
- Descuento aplicable: 10% (porque 30 está en rango 25-49)
- Precio con descuento: $2.50 × (1 - 10/100) = $2.25
- Subtotal: $2.25 × 30 = **$67.50**
- Ahorro: ($2.50 × 30) - $67.50 = **$7.50**

### Línea 2: Bolígrafos Azules (BOL001)
- Producto: BOL001 (Bolígrafo Azul caja x 50)
- Cantidad: 15
- Precio unitario: $5.00
- Descuento aplicable: 10% (porque 15 está en rango 10-24)
- Precio con descuento: $5.00 × (1 - 10/100) = $4.50
- Subtotal: $4.50 × 15 = **$67.50**
- Ahorro: ($5.00 × 15) - $67.50 = **$7.50**

### Totales del Presupuesto
- Total sin descuento: $2.50×30 + $5.00×15 = $75 + $75 = **$150.00**
- Total descuentos: $7.50 + $7.50 = **$15.00**
- **Total final: $135.00**
- Descuento promedio: ($15 / $150) × 100 = **10%**

---

## 📋 Estructura de Respuesta del Presupuesto

```json
{
  "numero_presupuesto": "PRES-20250116-001",
  "fecha": "2025-01-16",
  "cliente": "Nombre del Cliente",
  "lineas": [
    {
      "producto_id": "CUA001",
      "producto_nombre": "Cuaderno Rayado A4 100 Hojas",
      "categoria": "cuadernos",
      "cantidad": 30,
      "precio_unitario": 2.50,
      "descuento_porcentaje": 10,
      "precio_con_descuento": 2.25,
      "subtotal": 67.50,
      "ahorro": 7.50
    }
  ],
  "resumen": {
    "total_sin_descuento": 150.00,
    "total_descuentos": 15.00,
    "total_final": 135.00,
    "descuento_promedio_porcentaje": 10.0
  },
  "notas": "Presupuesto válido por 30 días"
}
```

---

## 🔄 Flujo de Interacción User → IA → Documentos → IA → User

1. **Usuario solicita presupuesto:** "Quiero 30 cuadernos rayados y 15 bolígrafos azules"
2. **IA lee:** `productos_libreria.json` para obtener precios y tramos de descuento
3. **IA calcula:** Aplica las reglas de `reglas_presupuestos.md` a cada línea
4. **IA genera:** JSON o PDF con presupuesto detallado
5. **Usuario recibe:** Presupuesto formateado con desglose de ahorro y total
6. **Cierre de Venta (Obligatorio):** La IA ofrece formalizar la compra indicando el **Alias: `mauri.casals`** y solicitando enviar el comprobante a **`mauriciocasals90@gmail.com`**.

---

## ⚙️ Reglas Especiales

- **Descuentos acumulables por línea:** Cada producto se calcula con su propio tramo de descuento. NO hay descuentos cruzados entre productos.
- **Redondeo:** Todos los montos se redondean a 2 decimales.
- **Validación:** Si cantidad < 1 o producto no existe, presupuesto rechazado con mensaje claro.
- **Cambios en BD:** Si se modifica `productos_libreria.json`, todos los presupuestos futuros usarán los nuevos precios y descuentos automáticamente.

---

## 📝 Casos de Uso

1. **Presupuesto simple:** Usuario solicita 1 producto
2. **Presupuesto múltiple:** Usuario solicita varios productos y cantidades
3. **Presupuesto comparativo:** ¿Cuánto ahorra si compra en mayor cantidad?
4. **Presupuesto batch:** Sistema genera presupuestos automáticos para múltiples clientes


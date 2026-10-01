#!/usr/bin/env python3
"""
Generador de Presupuestos en PDF
Entrada: JSON con datos mínimos
Salida: PDF estandarizado con formato profesional

Uso:
    python generar_presupuesto_pdf.py input.json output.pdf
"""

import json
import sys
from datetime import datetime
from decimal import Decimal
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, grey
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.pdfgen import canvas
import os

# Cargar BD de productos
def cargar_productos():
    """Lee productos_libreria.json"""
    productos_path = os.path.join(os.path.dirname(__file__), 'productos_libreria.json')
    with open(productos_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Buscar producto en BD
def buscar_producto(producto_id, productos_db):
    """Retorna (categoria, producto) si existe, senó (None, None)"""
    for categoria, datos in productos_db['categorias'].items():
        for prod in datos['productos']:
            if prod['id'] == producto_id:
                return categoria, prod
    return None, None

# Calcular descuento aplicable
def calcular_descuento(cantidad, descuentos):
    """Retorna porcentaje de descuento según cantidad"""
    for desc in descuentos:
        min_cant = desc['cantidad_minima']
        max_cant = desc['cantidad_maxima']
        
        if cantidad >= min_cant and (max_cant is None or cantidad <= max_cant):
            return desc['descuento_porcentaje']
    
    return 0

# Procesar línea de presupuesto
def procesar_linea(producto_id, cantidad, productos_db):
    """
    Retorna dict con:
    - producto_id, nombre, categoria, cantidad
    - precio_unitario, descuento_porcentaje, precio_con_descuento
    - subtotal, ahorro
    O None si hay error
    """
    if cantidad < 1:
        return None
    
    categoria, producto = buscar_producto(producto_id, productos_db)
    
    if not producto:
        return None
    
    precio_unitario = float(producto['precio_unitario'])
    descuento_pct = calcular_descuento(cantidad, producto['descuentos'])
    precio_con_descuento = precio_unitario * (1 - descuento_pct / 100)
    subtotal = round(precio_con_descuento * cantidad, 2)
    ahorro = round((precio_unitario * cantidad) - subtotal, 2)
    
    return {
        'producto_id': producto_id,
        'producto_nombre': producto['nombre'],
        'categoria': categoria,
        'cantidad': cantidad,
        'precio_unitario': precio_unitario,
        'descuento_porcentaje': descuento_pct,
        'precio_con_descuento': round(precio_con_descuento, 2),
        'subtotal': subtotal,
        'ahorro': ahorro
    }

# Generar presupuesto (JSON)
def generar_presupuesto(cliente, lineas_datos, productos_db, numero_presupuesto=None):
    """
    Genera estructura de presupuesto completo
    
    Input:
        cliente: str con nombre
        lineas_datos: list[{"producto_id": str, "cantidad": int}]
        productos_db: dict con BD de productos
        numero_presupuesto: str opcional
    
    Output:
        dict con presupuesto completo o None si hay error
    """
    if numero_presupuesto is None:
        numero_presupuesto = f"PRES-{datetime.now().strftime('%Y%m%d')}-{int(datetime.now().timestamp()) % 10000:04d}"
    
    lineas = []
    total_sin_descuento = 0
    total_descuentos = 0
    
    # Procesar cada línea
    for linea_req in lineas_datos:
        linea = procesar_linea(linea_req['producto_id'], linea_req['cantidad'], productos_db)
        
        if not linea:
            print(f"❌ Error: Producto '{linea_req['producto_id']}' no encontrado o cantidad inválida")
            return None
        
        lineas.append(linea)
        total_sin_descuento += linea['precio_unitario'] * linea['cantidad']
        total_descuentos += linea['ahorro']
    
    total_final = round(total_sin_descuento - total_descuentos, 2)
    desc_promedio = round((total_descuentos / total_sin_descuento * 100), 2) if total_sin_descuento > 0 else 0
    
    return {
        'numero_presupuesto': numero_presupuesto,
        'fecha': datetime.now().strftime('%Y-%m-%d'),
        'cliente': cliente,
        'lineas': lineas,
        'resumen': {
            'total_sin_descuento': round(total_sin_descuento, 2),
            'total_descuentos': round(total_descuentos, 2),
            'total_final': total_final,
            'descuento_promedio_porcentaje': desc_promedio
        },
        'notas': 'Presupuesto válido por 30 días'
    }

# Generar PDF con ReportLab (Diseño Corporativo y Elocuente)
def generar_pdf(presupuesto, ruta_salida):
    """
    Crea un documento de propuesta comercial y presupuesto formal, elocuente y estilizado
    """
    doc = SimpleDocTemplate(
        ruta_salida,
        pagesize=letter,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # Paleta de colores corporativos
    PRIMARY_COLOR = HexColor('#1e3a8a')   # Azul marino profundo
    SECONDARY_COLOR = HexColor('#0284c7') # Azul cielo profesional
    DARK_TEXT = HexColor('#1e293b')       # Texto oscuro elegante
    LIGHT_BG = HexColor('#f8fafc')        # Fondo suave
    ACCENT_GREEN = HexColor('#166534')    # Verde ahorro
    ACCENT_BG = HexColor('#dcfce7')       # Fondo verde suave
    BORDER_COLOR = HexColor('#cbd5e1')    # Borde sutil

    # Estilos de párrafos personalizados
    header_title_style = ParagraphStyle(
        'HeaderTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=PRIMARY_COLOR,
        fontName='Helvetica-Bold'
    )

    header_sub_style = ParagraphStyle(
        'HeaderSub',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11,
        textColor=HexColor('#64748b'),
        fontName='Helvetica'
    )

    meta_label_style = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11,
        textColor=DARK_TEXT,
        alignment=2 # Derecha
    )

    intro_p_style = ParagraphStyle(
        'IntroP',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=14,
        textColor=DARK_TEXT,
        fontName='Helvetica'
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=10,
        textColor=HexColor('#ffffff'),
        fontName='Helvetica-Bold',
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11,
        textColor=DARK_TEXT,
        fontName='Helvetica'
    )

    table_cell_center = ParagraphStyle(
        'TableCellCenter',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11,
        textColor=DARK_TEXT,
        fontName='Helvetica',
        alignment=1
    )

    table_cell_right = ParagraphStyle(
        'TableCellRight',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11,
        textColor=DARK_TEXT,
        fontName='Helvetica',
        alignment=2
    )

    discount_badge_style = ParagraphStyle(
        'DiscountBadge',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
        textColor=ACCENT_GREEN,
        fontName='Helvetica-Bold',
        alignment=1
    )

    terms_title_style = ParagraphStyle(
        'TermsTitle',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=12,
        textColor=PRIMARY_COLOR,
        fontName='Helvetica-Bold'
    )

    terms_body_style = ParagraphStyle(
        'TermsBody',
        parent=styles['Normal'],
        fontSize=8,
        leading=11.5,
        textColor=HexColor('#475569'),
        fontName='Helvetica'
    )

    # 1. Cabecera Corporativa con datos de emisor y presupuesto
    empresa_info = (
        f"<b>LIBRERÍA & PAPELERÍA COMERCIAL S.A.</b><br/>"
        f"<i>Soluciones Integrales para Empresas, Oficinas e Instituciones</i><br/>"
        f"CUIT: 30-71234567-9 | Av. Libertador 4500, CABA<br/>"
        f"ventas@libreriacomercial.com | Tel: (011) 4890-1234"
    )

    meta_info = (
        f"<b>PROPUESTA COMERCIAL</b><br/>"
        f"<font size=11 color='#1e3a8a'><b>Nº {presupuesto['numero_presupuesto']}</b></font><br/>"
        f"<b>Fecha de Emisión:</b> {presupuesto['fecha']}<br/>"
        f"<b>Validez:</b> 30 días corridos<br/>"
        f"<b>Moneda:</b> Pesos Argentinos (ARS)"
    )

    cabecera_data = [
        [Paragraph(empresa_info, header_sub_style), Paragraph(meta_info, meta_label_style)]
    ]
    cabecera_table = Table(cabecera_data, colWidths=[4.2*inch, 3.3*inch])
    cabecera_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, -1), 1.5, PRIMARY_COLOR),
    ]))
    story.append(cabecera_table)
    story.append(Spacer(1, 0.12*inch))

    # 2. Presentación Elocuente y Destinatario
    cliente_nombre = presupuesto.get('cliente', 'Estimado Cliente')
    ahorro_total = presupuesto['resumen']['total_descuentos']
    desc_prom = presupuesto['resumen']['descuento_promedio_porcentaje']

    intro_texto = (
        f"<b>Estimado/a {cliente_nombre}:</b><br/>"
        f"Agradecemos su interés en nuestras soluciones de librería e insumos comerciales. "
        f"A continuación, presentamos la propuesta económica detallada para los artículos solicitados. "
        f"Conforme a nuestro compromiso de optimizar sus costos operativos, hemos aplicado nuestra "
        f"<b>escala preferencial de bonificaciones por volumen</b>, permitiéndole obtener un ahorro significativo de "
        f"<b>${ahorro_total:,.2f}</b> (equivalente al <b>{desc_prom}%</b> de bonificación global sobre precios de lista)."
    )
    
    intro_table = Table([[Paragraph(intro_texto, intro_p_style)]], colWidths=[7.5*inch])
    intro_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(intro_table)
    story.append(Spacer(1, 0.15*inch))

    # 3. Tabla Detallada de Productos y Descuentos
    headers = [
        Paragraph("Ítem / Descripción del Producto", table_header_style),
        Paragraph("Cant.", table_header_style),
        Paragraph("P. Lista", table_header_style),
        Paragraph("Bonif.", table_header_style),
        Paragraph("P. Neto Unit.", table_header_style),
        Paragraph("Subtotal", table_header_style),
        Paragraph("Ahorro", table_header_style)
    ]
    
    tabla_filas = [headers]
    
    for i, linea in enumerate(presupuesto['lineas'], 1):
        desc_label = f"<b>{linea['descuento_porcentaje']}% OFF</b>" if linea['descuento_porcentaje'] > 0 else "0%"
        tabla_filas.append([
            Paragraph(f"<b>{i}. {linea['producto_nombre']}</b><br/><font color='#64748b' size=7.5>Cat: {linea['categoria'].capitalize()} | SKU: {linea['producto_id']}</font>", table_cell_style),
            Paragraph(f"<b>{linea['cantidad']}</b>", table_cell_center),
            Paragraph(f"${linea['precio_unitario']:,.2f}", table_cell_right),
            Paragraph(desc_label, discount_badge_style if linea['descuento_porcentaje'] > 0 else table_cell_center),
            Paragraph(f"<b>${linea['precio_con_descuento']:,.2f}</b>", table_cell_right),
            Paragraph(f"<b>${linea['subtotal']:,.2f}</b>", table_cell_right),
            Paragraph(f"<font color='#166534'>${linea['ahorro']:,.2f}</font>", table_cell_right)
        ])
    
    col_widths = [2.7*inch, 0.6*inch, 0.8*inch, 0.8*inch, 0.9*inch, 0.9*inch, 0.8*inch]
    tabla_productos = Table(tabla_filas, colWidths=col_widths, repeatRows=1)
    tabla_productos.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#ffffff'), LIGHT_BG]),
    ]))
    story.append(tabla_productos)
    story.append(Spacer(1, 0.12*inch))

    # 4. Bloque Inferior: Beneficios y Resumen Económico Liquidado
    resumen = presupuesto['resumen']
    
    beneficio_texto = (
        f"<b>🎯 Resumen de Beneficios Aplicados:</b><br/>"
        f"• <b>Bonificación por escala:</b> Ha recibido un descuento promedio del <b>{resumen['descuento_promedio_porcentaje']}%</b>.<br/>"
        f"• <b>Ahorro acumulado en este pedido:</b> <font color='#166534'><b>${resumen['total_descuentos']:,.2f}</b></font>.<br/>"
        f"• <b>Envío bonificado:</b> Incluye flete sin cargo para entregas en radio corporativo.<br/>"
        f"• <b>Facturación:</b> Emitimos Factura A o B según su condición fiscal."
    )

    resumen_lineas = [
        [Paragraph("Subtotal Precios de Lista:", table_cell_style), Paragraph(f"${resumen['total_sin_descuento']:,.2f}", table_cell_right)],
        [Paragraph("Bonificación Especial por Volumen:", ParagraphStyle('SubDesc', parent=table_cell_style, textColor=ACCENT_GREEN)), Paragraph(f"<font color='#166534'>- ${resumen['total_descuentos']:,.2f}</font>", table_cell_right)],
        [Paragraph("<b>TOTAL FINAL DE LA PROPUESTA:</b>", ParagraphStyle('TotLabel', parent=table_cell_style, fontSize=10, textColor=PRIMARY_COLOR)), Paragraph(f"<b><font size=11 color='#1e3a8a'>${resumen['total_final']:,.2f}</font></b>", table_cell_right)]
    ]
    resumen_subtable = Table(resumen_lineas, colWidths=[2.1*inch, 1.4*inch])
    resumen_subtable.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('LINEABOVE', (0, 2), (-1, 2), 1, PRIMARY_COLOR),
        ('BACKGROUND', (0, 2), (-1, 2), HexColor('#e0f2fe')),
    ]))

    bloque_balance = [
        [
            Paragraph(beneficio_texto, ParagraphStyle('BenStyle', parent=styles['Normal'], fontSize=8, leading=11, textColor=DARK_TEXT)),
            resumen_subtable
        ]
    ]
    tabla_balance = Table(bloque_balance, colWidths=[3.8*inch, 3.7*inch])
    tabla_balance.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 0), (0, 0), ACCENT_BG),
    ]))
    story.append(tabla_balance)
    story.append(Spacer(1, 0.12*inch))

    # 5. Términos Comerciales y Garantías
    condiciones_texto = (
        f"<b>CONDICIONES COMERCIALES & DATOS DE PAGO:</b><br/>"
        f"1. <b>Forma de Pago:</b> Transferencia bancaria inmediata (<b>Alias: mauri.casals</b>). Enviar comprobante a <b>mauriciocasals90@gmail.com</b>.<br/>"
        f"2. <b>Plazo de Entrega:</b> Despacho inmediato dentro de las 24 a 48 horas hábiles posteriores a la confirmación de la transferencia.<br/>"
        f"3. <b>Garantía de Calidad:</b> Todos nuestros productos cuentan con garantía directa de fábrica y reposición inmediata ante cualquier falla.<br/>"
        f"4. <b>Mantenimiento de Oferta:</b> Los valores informados se mantienen firmes e inalterables por el período de validez estipulado."
    )
    story.append(Paragraph(condiciones_texto, terms_body_style))
    story.append(Spacer(1, 0.15*inch))

    # 6. Cierre de Cortesía y Firmas
    firmas_data = [
        [
            Paragraph("_____________________________<br/><b>Departamento Comercial</b><br/>Librería & Papelería Comercial S.A.", table_cell_center),
            Paragraph("_____________________________<br/><b>Conformidad del Cliente</b><br/>Firma, Aclaración y CUIT", table_cell_center)
        ]
    ]
    firmas_table = Table(firmas_data, colWidths=[3.75*inch, 3.75*inch])
    firmas_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(firmas_table)

    # Construir PDF
    doc.build(story)
    print(f"✅ PDF elocuente generado con éxito: {ruta_salida}")

# Main
def main():
    if len(sys.argv) < 3:
        print("Uso: python generar_presupuesto_pdf.py <archivo_input.json> <archivo_output.pdf>")
        print("\nEjemplo archivo input.json:")
        print(json.dumps({
            "cliente": "Nombre del Cliente",
            "numero_presupuesto": "PRES-20250116-001",  # Opcional
            "lineas": [
                {"producto_id": "CUA001", "cantidad": 30},
                {"producto_id": "BOL001", "cantidad": 15}
            ]
        }, indent=2, ensure_ascii=False))
        sys.exit(1)
    
    archivo_input = sys.argv[1]
    archivo_output = sys.argv[2]
    
    # Validar que existe el archivo de entrada
    if not os.path.exists(archivo_input):
        print(f"❌ Error: Archivo '{archivo_input}' no encontrado")
        sys.exit(1)
    
    # Cargar datos de entrada
    try:
        with open(archivo_input, 'r', encoding='utf-8') as f:
            datos_entrada = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error al parsear JSON: {e}")
        sys.exit(1)
    
    # Validar estructura mínima
    if 'cliente' not in datos_entrada or 'lineas' not in datos_entrada:
        print("❌ Error: JSON debe contener 'cliente' y 'lineas'")
        sys.exit(1)
    
    # Cargar BD de productos
    productos_db = cargar_productos()
    
    # Generar presupuesto
    numero = datos_entrada.get('numero_presupuesto')
    presupuesto = generar_presupuesto(
        datos_entrada['cliente'],
        datos_entrada['lineas'],
        productos_db,
        numero
    )
    
    if not presupuesto:
        print("❌ Error al generar presupuesto")
        sys.exit(1)
    
    # Mostrar presupuesto
    print(json.dumps(presupuesto, indent=2, ensure_ascii=False))
    
    # Generar PDF
    try:
        generar_pdf(presupuesto, archivo_output)
    except Exception as e:
        print(f"❌ Error al generar PDF: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

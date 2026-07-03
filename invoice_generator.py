"""
Sistema de generación de facturas para Respuestos La Tiendita
Genera PDF profesionales con los datos de la tienda y productos vendidos
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from datetime import datetime
from config import TIENDA, COLORES, MONEDA
import os

class FacturaGenerator:
    """Generador de facturas en PDF"""
    
    def __init__(self, numero_factura, cliente_tipo="Consumidor Final"):
        self.numero_factura = numero_factura
        self.cliente_tipo = cliente_tipo
        self.fecha = datetime.now().strftime("%d/%m/%Y")
        self.hora = datetime.now().strftime("%H:%M")
        self.productos = []
        self.subtotal = 0
        self.descuento_porcentaje = 0
        self.pago_recibido = 0
        
    def agregar_producto(self, codigo, descripcion, cantidad, precio_unitario, descuento=0):
        """Agrega un producto a la factura"""
        subtotal_producto = cantidad * precio_unitario
        descuento_monto = (subtotal_producto * descuento) / 100
        total_producto = subtotal_producto - descuento_monto
        
        self.productos.append({
            'codigo': codigo,
            'descripcion': descripcion,
            'cantidad': cantidad,
            'precio_unitario': precio_unitario,
            'descuento': descuento,
            'subtotal': subtotal_producto,
            'total': total_producto
        })
        
        self.subtotal += total_producto
    
    def establecer_pago_recibido(self, monto):
        """Establece el monto de pago recibido"""
        self.pago_recibido = monto
    
    def calcular_cambio(self):
        """Calcula el cambio"""
        return round(self.pago_recibido - self.subtotal, 2)
    
    def generar_factura(self, nombre_archivo="factura.pdf"):
        """Genera la factura en PDF"""
        
        # Crear documento PDF
        doc = SimpleDocTemplate(nombre_archivo, pagesize=letter,
                               rightMargin=0.5*inch, leftMargin=0.5*inch,
                               topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#142C70'),
            spaceAfter=6,
            alignment=1  # Centrado
        )
        
        header_style = ParagraphStyle(
            'HeaderStyle',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#333333'),
            alignment=1
        )
        
        # ============ ENCABEZADO ============
        # Logo y nombre
        encabezado_datos = []
        
        # Intenta agregar logo si existe
        logo_path = TIENDA.get('logo_path')
        if logo_path and os.path.exists(logo_path):
            try:
                logo = Image(logo_path, width=0.8*inch, height=0.8*inch)
                encabezado_datos.append(logo)
            except:
                encabezado_datos.append(Paragraph(TIENDA['nombre'], title_style))
        else:
            encabezado_datos.append(Paragraph(TIENDA['nombre'], title_style))
        
        elements.extend(encabezado_datos)
        
        # Información de la tienda
        info_tienda = f"""
        <b>RIF:</b> {TIENDA['rif']}<br/>
        <b>Teléfono:</b> {TIENDA['telefono']}<br/>
        <b>Correo:</b> {TIENDA['email']}<br/>
        """
        elements.append(Paragraph(info_tienda, header_style))
        elements.append(Spacer(1, 0.15*inch))
        
        # Número de factura
        num_factura = f"<b>FACTURA: FAC-{str(self.numero_factura).zfill(5)}</b>"
        elements.append(Paragraph(num_factura, header_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # ============ CLIENTE Y FECHA ============
        cliente_fecha_data = [
            ['CLIENTE', 'FECHA', 'FORMA DE PAGO'],
            [self.cliente_tipo, self.fecha, 'Contado'],
            ['● Pagada', '', '']
        ]
        
        cliente_fecha_table = Table(cliente_fecha_data, colWidths=[2*inch, 2*inch, 2*inch])
        cliente_fecha_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, 1), 1, colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#142C70')),
        ]))
        
        elements.append(cliente_fecha_table)
        elements.append(Spacer(1, 0.15*inch))
        
        # ============ TABLA DE PRODUCTOS ============
        datos_productos = [
            ['Código', 'Descripción', 'Cant.', f'Precio ({MONEDA})', 'Desc.%', f'Subtotal ({MONEDA})']
        ]
        
        for prod in self.productos:
            datos_productos.append([
                prod['codigo'],
                prod['descripcion'],
                str(prod['cantidad']),
                f"{prod['precio_unitario']:.2f}",
                f"{prod['descuento']:.1f}%",
                f"{prod['total']:.2f}"
            ])
        
        tabla_productos = Table(datos_productos, colWidths=[0.8*inch, 2.5*inch, 0.6*inch, 1*inch, 0.6*inch, 1*inch])
        tabla_productos.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#142C70')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0F0F0')])
        ]))
        
        elements.append(tabla_productos)
        elements.append(Spacer(1, 0.2*inch))
        
        # ============ TOTALES ============
        cambio = self.calcular_cambio()
        
        totales_data = [
            ['', f'Subtotal:', f'$ {self.subtotal:.2f}'],
            ['', f'TOTAL:', f'$ {self.subtotal:.2f}'],
            ['', f'PAGO RECIBIDO:', f'$ {self.pago_recibido:.2f}'],
            ['', f'CAMBIO:', f'$ {cambio:.2f}']
        ]
        
        tabla_totales = Table(totales_data, colWidths=[2.5*inch, 2*inch, 1.5*inch])
        tabla_totales.setStyle(TableStyle([
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (1, 0), (1, 0), 'Helvetica'),
            ('FONTNAME', (1, 1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (1, 0), (-1, -1), 10),
            ('BACKGROUND', (1, 1), (-1, 1), colors.HexColor('#E8F0F8')),
            ('TEXTCOLOR', (1, 1), (-1, 1), colors.HexColor('#142C70')),
            ('GRID', (1, 0), (-1, -1), 1, colors.grey),
            ('TOPPADDING', (1, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (1, 0), (-1, -1), 8),
        ]))
        
        elements.append(tabla_totales)
        elements.append(Spacer(1, 0.3*inch))
        
        # ============ PIE DE PÁGINA ============
        pie = f"""
        <b>¡Gracias por su preferencia! — Respuestos La Tiendita</b><br/>
        Teléfono: {TIENDA['telefono']} | Email: {TIENDA['email']}<br/>
        <font size="7">Generado: {self.fecha} {self.hora}</font>
        """
        elementos_pie = Paragraph(pie, header_style)
        elements.append(elementos_pie)
        
        # Generar PDF
        try:
            doc.build(elements)
            print(f"✅ Factura generada exitosamente: {nombre_archivo}")
            return True
        except Exception as e:
            print(f"❌ Error al generar factura: {e}")
            return False
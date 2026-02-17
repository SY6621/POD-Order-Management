# -*- coding: utf-8 -*-
"""
PDF generation service for POD production documents
Pixel-accurate layout based on SVG template
"""

from pathlib import Path
from typing import Optional
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from src.config.settings import settings

# Page dimensions (A4 in points: 595.28 x 841.89)
PAGE_WIDTH = 595.3
PAGE_HEIGHT = 822

# Colors
RED = colors.Color(0.9, 0, 0.07)  # #E60012
GRAY = colors.Color(0.4, 0.4, 0.4)  # #666666
LIGHT_GRAY = colors.Color(0.83, 0.83, 0.83)  # #D3D3D3
LIGHT_YELLOW = colors.Color(1, 1, 0.9)


class PDFService:
    """PDF document generation service with pixel-accurate layout"""
    
    def __init__(self):
        self.output_dir = settings.OUTPUT_DIR
        self.fonts_dir = settings.FONTS_DIR
        self.photos_dir = settings.ASSETS_DIR / "photos"
        settings.ensure_output_dir()
        self._register_fonts()
    
    def _register_fonts(self):
        """Register Chinese fonts"""
        try:
            back_font = self.fonts_dir / "back_standard.ttf"
            if back_font.exists():
                pdfmetrics.registerFont(TTFont("ChineseFont", str(back_font)))
                print("[OK] Font registered: ChineseFont")
        except Exception as e:
            print(f"[WARN] Font registration failed: {e}")
    
    def generate_production_pdf(self, order_data) -> Optional[Path]:
        """Generate production PDF with pixel-accurate layout"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"POD_{order_data.order_id}_{timestamp}.pdf"
        pdf_path = self.output_dir / filename
        
        try:
            c = canvas.Canvas(str(pdf_path), pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
            
            # Draw all sections
            self._draw_title(c, order_data)
            self._draw_info_section(c, order_data)
            self._draw_preview_section(c, order_data)
            self._draw_shipping_section(c, order_data)
            
            c.save()
            print(f"[OK] Production PDF generated: {filename}")
            return pdf_path
            
        except Exception as e:
            print(f"[ERROR] PDF generation failed: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _draw_title(self, c, order_data):
        """Draw title section"""
        # Main title: POD-订单生产文件
        c.setFont("Helvetica", 36)
        c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 55, "POD-")
        
        try:
            c.setFont("ChineseFont", 36)
            c.drawString(PAGE_WIDTH/2 - 30, PAGE_HEIGHT - 55, "订单生产文件")
        except:
            c.setFont("Helvetica", 36)
            c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 55, "POD-Order Production")
        
        # SKU code (red, bold)
        c.setFillColor(RED)
        c.setFont("Helvetica-Bold", 22)
        c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 105, order_data.sku)
        
        # "产品编号 (SKU)" subtitle
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 10)
        try:
            c.setFont("ChineseFont", 10)
            c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 122, "产品编号 (SKU)")
        except:
            c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 122, "Product Code (SKU)")
    
    def _draw_info_section(self, c, order_data):
        """Draw three-column info section"""
        start_y = PAGE_HEIGHT - 165
        row_height = 17.7
        
        # Column positions
        col1_label_x, col1_value_x = 38, 106
        col2_label_x, col2_value_x = 224, 292
        col3_label_x, col3_value_x = 369, 452
        
        label_width = 67.7
        
        # Section headers (red)
        c.setFillColor(RED)
        c.setFont("Helvetica-Bold", 12)
        try:
            c.setFont("ChineseFont", 12)
        except:
            pass
        c.drawString(col1_label_x, start_y + 15, "订单信息")
        c.drawString(col2_label_x, start_y + 15, "产品 (SKU) 规格")
        c.drawString(col3_label_x, start_y + 15, "定制详情")
        
        # Column 1: Order Info
        col1_data = [
            ("订单ID:", order_data.order_id),
            ("客户:", order_data.customer_name),
            ("订单日期:", order_data.order_date),
            ("发货日期:", order_data.ship_date),
        ]
        self._draw_table_column(c, col1_label_x, col1_value_x, start_y, col1_data, row_height, label_width)
        
        # Column 2: Product Info
        col2_data = [
            ("形状:", order_data.shape),
            ("颜色:", order_data.color),
            ("尺寸:", order_data.size),
            ("工艺:", order_data.craft),
        ]
        self._draw_table_column(c, col2_label_x, col2_value_x, start_y, col2_data, row_height, label_width)
        
        # Column 3: Customization (yellow background)
        col3_data = [
            ("正面:", order_data.front_text),
            ("正面字体:", order_data.front_font),
            ("背面文字:", order_data.back_text),
        ]
        self._draw_table_column(c, col3_label_x, col3_value_x, start_y, col3_data, row_height, label_width, 
                                bg_color=LIGHT_YELLOW)
    
    def _draw_table_column(self, c, label_x, value_x, start_y, data, row_height, label_width, bg_color=None):
        """Draw a table column with labels and values"""
        for i, (label, value) in enumerate(data):
            y = start_y - (i * row_height)
            
            # Draw label cell (gray background)
            c.setFillColor(LIGHT_GRAY)
            c.rect(label_x, y - row_height + 2, label_width, row_height, fill=1, stroke=1)
            
            # Draw value cell
            if bg_color:
                c.setFillColor(bg_color)
            else:
                c.setFillColor(colors.white)
            c.rect(value_x, y - row_height + 2, 77.2, row_height, fill=1, stroke=1)
            
            # Draw text
            c.setFillColor(colors.black)
            c.setFont("Helvetica", 9)
            try:
                c.setFont("ChineseFont", 9)
            except:
                pass
            c.drawString(label_x + 3, y - 10, label)
            c.drawString(value_x + 3, y - 10, str(value))
    
    def _draw_preview_section(self, c, order_data):
        """Draw image preview section"""
        preview_y = PAGE_HEIGHT - 390
        
        # Left box: Product photo placeholder
        c.setStrokeColor(GRAY)
        c.setLineWidth(0.5)
        c.rect(38, preview_y - 120, 140, 120, stroke=1, fill=0)
        
        # "外观，颜色实拍图" label (red)
        c.setFillColor(RED)
        c.setFont("Helvetica", 10)
        try:
            c.setFont("ChineseFont", 10)
            c.drawCentredString(108, preview_y - 135, "外观，颜色实拍图")
        except:
            c.drawCentredString(108, preview_y - 135, "Product Photo")
        
        # Right box: Effect image with dimensions
        c.setStrokeColor(GRAY)
        c.rect(190, preview_y - 120, 165, 120, stroke=1, fill=0)
        
        # Dimension labels
        c.setFillColor(RED)
        c.setFont("Helvetica", 10)
        c.drawCentredString(272, preview_y + 5, f"{order_data.width_mm} mm")
        c.saveState()
        c.translate(185, preview_y - 60)
        c.rotate(90)
        c.drawCentredString(0, 0, f"{order_data.height_mm} mm")
        c.restoreState()
        
        # Effect image info
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 9)
        c.drawString(200, preview_y - 100, f"Front Text: {order_data.front_text}")
        c.drawString(200, preview_y - 112, f"Font: {order_data.front_font}")
        c.drawString(200, preview_y - 124, f"Back Text: {order_data.back_text}")
    
    def _draw_shipping_section(self, c, order_data):
        """Draw shipping label and info section"""
        shipping = order_data.shipping
        section_y = PAGE_HEIGHT - 610
        
        # === Left side: Shipping label mockup ===
        label_x, label_y = 38, section_y - 180
        label_w, label_h = 140, 180
        
        # Label border
        c.setStrokeColor(colors.black)
        c.setLineWidth(1)
        c.rect(label_x, label_y, label_w, label_h, stroke=1, fill=0)
        
        # Postlink header
        c.setFont("Helvetica-Bold", 14)
        c.drawString(label_x + 5, label_y + label_h - 20, "Postlink")
        c.setFont("Helvetica", 8)
        c.drawRightString(label_x + label_w - 5, label_y + label_h - 20, "PX  PX")
        
        # TO: recipient
        c.setFont("Helvetica-Bold", 9)
        c.drawString(label_x + 5, label_y + label_h - 40, "TO:")
        c.setFont("Helvetica", 8)
        c.drawString(label_x + 25, label_y + label_h - 40, shipping.recipient_name)
        c.drawString(label_x + 25, label_y + label_h - 52, shipping.recipient_address)
        c.drawString(label_x + 25, label_y + label_h - 64, 
                    f"{shipping.recipient_postal_code};{shipping.recipient_city}")
        
        # Country code (large)
        c.setFont("Helvetica-Bold", 24)
        c.drawRightString(label_x + label_w - 10, label_y + label_h - 75, shipping.recipient_country_code)
        
        # Barcode placeholder
        c.setFont("Helvetica", 7)
        c.drawCentredString(label_x + label_w/2, label_y + 55, f"[{shipping.tracking_number}]")
        c.rect(label_x + 10, label_y + 60, label_w - 20, 20, stroke=1, fill=0)
        
        # Ref No
        c.setFont("Helvetica", 7)
        c.drawString(label_x + 5, label_y + 40, f"Ref No: {shipping.ref_no}")
        c.drawString(label_x + 5, label_y + 30, "pet ID tag | 0.03KG")
        
        # "面单样版 10X10cm" watermark
        c.setFillColor(colors.Color(1, 0.6, 0))  # Orange
        c.setFont("Helvetica-Bold", 14)
        try:
            c.setFont("ChineseFont", 14)
            c.drawString(label_x + 15, label_y + 10, "面单样版 10X10cm")
        except:
            c.drawString(label_x + 5, label_y + 10, "Label Sample 10X10cm")
        
        # === Right side: Shipping info ===
        info_x = 334
        info_y = section_y
        
        # Header backgroun# -*- coding: utf-8 -*-
"""
PDF generation service for POD production documents
Pixel-accurate layout based on template
"""

from pathlib import Path
from typing import Optional
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from src.config.settings import settings

PAGE_WIDTH, PAGE_HEIGHT = A4
RED = colors.Color(0.9, 0, 0.07)
GRAY = colors.Color(0.4, 0.4, 0.4)
LIGHT_GRAY = colors.Color(0.83, 0.83, 0.83)
ORANGE = colors.Color(1, 0.5, 0)


class PDFService:
    
    def __init__(self):
        self.output_dir = settings.OUTPUT_DIR
        self.fonts_dir = settings.FONTS_DIR
        self.photos_dir = settings.ASSETS_DIR / "photos"
        settings.ensure_output_dir()
        self._register_fonts()
    
    def _register_fonts(self):
        try:
            font_path = self.fonts_dir / "back_standard.ttf"
            if font_path.exists():
                pdfmetrics.registerFont(TTFont("CN", str(font_path)))
                print("[OK] Font registered: CN")
        except Exception as e:
            print(f"[WARN] Font registration failed: {e}")
    
    def _font(self, c, size, bold=False):
        try:
            c.setFont("CN", size)
        except:
            c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
    
    def generate_production_pdf(self, order_data) -> Optional[Path]:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"POD_{order_data.order_id}_{ts}.pdf"
        pdf_path = self.output_dir / filename
        
        try:
            c = canvas.Canvas(str(pdf_path), pagesize=A4)
            self._draw_all(c, order_data)
            c.save()
            print(f"[OK] PDF generated: {filename}")
            return pdf_path
        except Exception as e:
            print(f"[ERROR] PDF failed: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _draw_all(self, c, d):
        self._title(c, d)
        self._info_tables(c, d)
        self._preview(c, d)
        self._shipping(c, d)
    
    def _title(self, c, d):
        # Main title
        c.setFillColor(colors.black)
        self._font(c, 36)
        c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 50, "POD-订单生产文件")
        
        # SKU - RED
        c.setFillColor(RED)
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 95, d.sku)
        
        # Subtitle
        c.setFillColor(colors.black)
        self._font(c, 10)
        c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 115, "产品编号 (SKU)")
    
    def _info_tables(self, c, d):
        y0 = PAGE_HEIGHT - 155
        rh = 18
        
        # Headers
        c.setFillColor(RED)
        self._font(c, 12)
        c.drawString(40, y0, "订单信息")
        c.drawString(220, y0, "产品 (SKU) 规格")
        c.drawString(400, y0, "定制详情")
        
        # Column 1
        c1 = [("订单ID:", d.order_id), ("客户:", d.customer_name),
              ("订单日期:", d.order_date), ("发货日期:", d.ship_date)]
        self._table(c, 40, y0-15, c1, rh)
        
        # Column 2
        c2 = [("形状:", d.shape), ("颜色:", d.color),
              ("尺寸:", d.size), ("工艺:", d.craft)]
        self._table(c, 220, y0-15, c2, rh)
        
        # Column 3
        c3 = [("正面:", d.front_text), ("正面字体:", d.front_font),
              ("背面文字:", d.back_text)]
        self._table(c, 400, y0-15, c3, rh, yellow=True)
    
    def _table(self, c, x, y, data, rh, yellow=False):
        lw, vw = 60, 95
        for i, (label, val) in enumerate(data):
            yi = y - i * rh
            # Label cell
            c.setFillColor(LIGHT_GRAY)
            c.rect(x, yi - rh, lw, rh, fill=1, stroke=1)
            # Value cell
            c.setFillColor(colors.Color(1, 1, 0.85) if yellow else colors.white)
            c.rect(x + lw, yi - rh, vw, rh, fill=1, stroke=1)
            # Text
            c.setFillColor(colors.black)
            self._font(c, 9)
            c.drawString(x + 3, yi - 13, label)
            c.drawString(x + lw + 3, yi - 13, str(val))
    
    def _preview(self, c, d):
        py = PAGE_HEIGHT - 360
        
        # Left: Photo box
        c.setStrokeColor(GRAY)
        c.setLineWidth(0.5)
        c.rect(40, py - 130, 150, 130, stroke=1)
        
        # Photo label
        c.setFillColor(RED)
        self._font(c, 11)
        c.drawCentredString(115, py - 145, "外观，颜色实拍图")
        
        # Right: Effect box
        c.setStrokeColor(GRAY)
        c.rect(210, py - 130, 180, 130, stroke=1)
        
        # Dimensions
        c.setFillColor(RED)
        self._font(c, 11)
        c.drawCentredString(300, py + 8, f"{d.width_mm} mm")
        c.saveState()
        c.translate(200, py - 65)
        c.rotate(90)
        c.drawCentredString(0, 0, f"{d.height_mm} mm")
        c.restoreState()
        
        # Effect info
        c.setFillColor(colors.black)
        self._font(c, 9)
        c.drawString(220, py - 100, f"Front Text: {d.front_text}")
        c.drawString(220, py - 112, f"Font: {d.front_font}")
        c.drawString(220, py - 124, f"Back Text: {d.back_text}")
    
    def _shipping(self, c, d):
        s = d.shipping
        sy = PAGE_HEIGHT - 520
        
        # === Left: Postlink label ===
        lx, ly, lw, lh = 40, sy - 200, 160, 200
        c.setStrokeColor(colors.black)
        c.setLineWidth(1)
        c.rect(lx, ly, lw, lh, stroke=1)
        
        # Header
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(lx + 8, ly + lh - 25, "Postlink")
        c.setFont("Helvetica", 9)
        c.drawRightString(lx + lw - 8, ly + lh - 25, "PX  PX")
        
        # TO
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(RED)
        c.drawString(lx + 8, ly + lh - 50, "TO:")
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 9)
        c.drawString(lx + 30, ly + lh - 50, s.recipient_name)
        c.drawString(lx + 30, ly + lh - 62, s.recipient_address)
        c.drawString(lx + 30, ly + lh - 74, f"{s.recipient_postal_code};{s.recipient_city}")
        
        # Country code
        c.setFont("Helvetica-Bold", 28)
        c.drawRightString(lx + lw - 10, ly + lh - 85, s.recipient_country_code)
        
        # Box for lvP
        c.rect(lx + lw - 45, ly + lh - 120, 35, 35, stroke=1)
        c.setFont("Helvetica", 10)
        c.drawCentredString(lx + lw - 27, ly + lh - 140, "lv.P")
        
        # Barcode
        c.setFont("Helvetica", 8)
        c.drawCentredString(lx + lw/2, ly + 70, s.tracking_number)
        c.rect(lx + 15, ly + 75, lw - 30, 25, stroke=1)
        
        # Ref
        c.setFont("Helvetica", 8)
        c.drawString(lx + 8, ly + 50, f"Ref No: {s.ref_no}")
        c.drawString(lx + 8, ly + 38, "pet ID tag | 0.03KG")
        
        # Watermark
        c.setFillColor(ORANGE)
        self._font(c, 16)
        c.drawString(lx + 20, ly + 12, "面单样版")
        self._font(c, 12)
        c.drawString(lx + 35, ly - 2, "10 X10cm")
        
        # === Right: Shipping info ===
        rx = 220
        
        # Header
        c.setFillColor(LIGHT_GRAY)
        c.rect(rx, sy - 18, 70, 18, fill=1, stroke=1)
        c.setFillColor(colors.black)
        self._font(c, 12)
        c.drawString(rx + 5, sy - 14, "物流信息")
        
        # Tracking box
        c.setStrokeColor(RED)
        c.setLineWidth(1)
        c.rect(rx + 70, sy - 18, 160, 18, stroke=1)
        
        # Tracking label and number
        c.setFillColor(RED)
        self._font(c, 10)
        c.drawString(rx + 5, sy - 38, "物流单号�?)
        c.drawString(rx + 75, sy - 38, s.tracking_number)
        
        # Info box
        c.setStrokeColor(GRAY)
        c.setLineWidth(0.5)
        c.rect(rx, sy - 170, 230, 130, stroke=1)
        
        # Address lines
        c.setFillColor(colors.black)
        self._font(c, 10)
        lines = [
            ("国家�?, s.recipient_country),
            ("收件人名�?, s.recipient_name),
            ("收件省州�?, s.recipient_state),
            ("收件城市�?, s.recipient_city),
            ("收件邮编�?, s.recipient_postal_code),
            ("收件地址�?, s.recipient_address),
        ]
        for i, (lbl, val) in enumerate(lines):
            c.drawString(rx + 45, sy - 55 - i * 18, lbl)
            c.drawString(rx + 105, sy - 55 - i * 18, str(val))
    
    def generate_from_raw_data(self, raw_data):
        from src.services.shipping_service import shipping_service
        order_data = shipping_service.create_order_data(raw_data)
        shipping_service.create_shipping_label(order_data)
        return self.generate_production_pdf(order_data)


pdf_service = PDFService()

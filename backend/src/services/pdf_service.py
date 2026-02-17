# -*- coding: utf-8 -*-
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
        """注册中文字体 - 使用阿里巴巴普惠体"""
        try:
            # 优先使用阿里巴巴普惠体（完整中文支持）
            alibaba_font_path = self.fonts_dir / "阿里巴巴普惠体" / "ALIBABAPUHUITI-3-55-REGULAR.TTF"
            if alibaba_font_path.exists():
                pdfmetrics.registerFont(TTFont("CN", str(alibaba_font_path)))
                print(f"[OK] Font registered: CN (阿里巴巴普惠体)")
            else:
                # 备用：back_standard.ttf
                fallback_path = self.fonts_dir / "back_standard.ttf"
                if fallback_path.exists():
                    pdfmetrics.registerFont(TTFont("CN", str(fallback_path)))
                    print(f"[OK] Font registered: CN (back_standard)")
                else:
                    print(f"[WARN] No Chinese font found!")
        except Exception as e:
            print(f"[WARN] Font registration failed: {e}")
            import traceback
            traceback.print_exc()
    
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
        c.drawString(rx + 5, sy - 38, "物流单号：")
        c.drawString(rx + 75, sy - 38, s.tracking_number)
        
        # Info box
        c.setStrokeColor(GRAY)
        c.setLineWidth(0.5)
        c.rect(rx, sy - 170, 230, 130, stroke=1)
        
        # Address lines
        c.setFillColor(colors.black)
        self._font(c, 10)
        lines = [
            ("国家：", s.recipient_country),
            ("收件人名：", s.recipient_name),
            ("收件省州：", s.recipient_state),
            ("收件城市：", s.recipient_city),
            ("收件邮编：", s.recipient_postal_code),
            ("收件地址：", s.recipient_address),
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

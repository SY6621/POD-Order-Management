# -*- coding: utf-8 -*-
"""
SVG Template to PDF Service
Pixel-perfect PDF generation using SVG template
"""

import re
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
from io import BytesIO

from svglib.svglib import svg2rlg
from svglib import fonts
from reportlab.graphics import renderPDF
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from src.config.settings import settings, BASE_DIR


class SVGPDFService:
    """Generate PDF by filling SVG template with order data"""
    
    # Placeholder mappings: SVG text -> data field
    PLACEHOLDERS = {
        # Order Info
        "3891559803": "order_id",
        "John Smith": "customer_name",
        "2026-02-01": "order_date",
        "2026-02-03": "ship_date",
        
        # Product Info
        "骨头形": "shape",
        "骨头形": "shape",
        "金色": "color",
        "大": "size",
        "抛光": "craft",
        
        # Customization
        "ALice": "front_text",
        "F-04": "front_font",
        "0412345678": "back_text",
        
        # SKU
        "B-E01A": "sku",
        
        # Shipping
        "04123456780412345678": "tracking_number",
        "Demi Brooker": "recipient_name",
        "3/1A Salisbury Rd": "recipient_address",
        "2029;Rose Bay": "postal_city",
        "AU": "country_code",
        "Australia": "country",
        "Trish Weeden": "recipient_name_info",
        "TAS": "state",
        "YOUNGTOWN": "city",
        "7249": "postal_code",
        "36 Jubilee Rd": "address",
        
        # Dimensions
        "45 mm": "width_label",
        "26 mm": "height_label",
    }
    
    def __init__(self):
        self.output_dir = settings.OUTPUT_DIR
        self.fonts_dir = settings.FONTS_DIR
        # Get template path
        self.template_path = BASE_DIR / "src" / "模版-设计图-校对文档-快递面单V2.svg"
        settings.ensure_output_dir()
        self._register_fonts()
    
    def _register_fonts(self):
        """Register Alibaba PuHuiTi fonts and custom fonts for PDF generation"""
        try:
            # Alibaba PuHuiTi font paths
            alibaba_dir = self.fonts_dir / "阿里巴巴普惠体"
            
            # Font files (note: filenames are uppercase)
            alibaba_fonts = {
                'AlibabaPuHuiTi-Regular': 'ALIBABAPUHUITI-3-55-REGULAR.TTF',
                'AlibabaPuHuiTi-Medium': 'ALIBABAPUHUITI-3-65-MEDIUM.TTF',
                'AlibabaPuHuiTi-SemiBold': 'ALIBABAPUHUITI-3-75-SEMIBOLD.TTF',
                'AlibabaPuHuiTi-Heavy': 'ALIBABAPUHUITI-3-105-HEAVY.TTF',
            }
            
            # Register Alibaba fonts
            for font_name, font_file in alibaba_fonts.items():
                font_path = alibaba_dir / font_file
                if font_path.exists():
                    pdfmetrics.registerFont(TTFont(font_name, str(font_path)))
                    fonts.register_font(font_name, str(font_path))
                    print(f"[OK] Registered {font_name}")
                else:
                    print(f"[WARN] Font not found: {font_path}")
            
            # Map original SVG fonts to Alibaba fonts
            regular_path = str(alibaba_dir / 'ALIBABAPUHUITI-3-55-REGULAR.TTF')
            medium_path = str(alibaba_dir / 'ALIBABAPUHUITI-3-65-MEDIUM.TTF')
            semibold_path = str(alibaba_dir / 'ALIBABAPUHUITI-3-75-SEMIBOLD.TTF')
            heavy_path = str(alibaba_dir / 'ALIBABAPUHUITI-3-105-HEAVY.TTF')
            
            # Map all original fonts to Alibaba fonts
            font_mappings = {
                # Title fonts -> Medium
                'MicrosoftYaHeiLight': medium_path,
                'MicrosoftYaHei': regular_path,
                'MicrosoftYaHeiUI': regular_path,
                'MicrosoftYaHeiUILight': regular_path,
                # Section headers -> SemiBold
                'DingTalk-JinBuTi': semibold_path,
                # SKU -> Heavy
                'Swiss721BT-Heavy': heavy_path,
                # Other fonts
                'AdobeSongStd-Light-GBpc-EUC-H': regular_path,
            }
            
            for font_name, font_path in font_mappings.items():
                try:
                    pdfmetrics.registerFont(TTFont(font_name, font_path))
                    fonts.register_font(font_name, font_path)
                except:
                    pass  # Already registered
            
            print("[OK] All fonts mapped to Alibaba PuHuiTi")
            
            # Register custom project fonts (F-04, back_standard, etc.)
            self._register_custom_fonts()
                
        except Exception as e:
            print(f"[WARN] Font registration failed: {e}")
            import traceback
            traceback.print_exc()
    
    def _register_custom_fonts(self):
        """Register custom project fonts for effect image text"""
        font_mappings = {
            # Front fonts (keep F-04 for effect image)
            'F-04': 'F-04.ttf',
            # Back font
            'back_standard': 'back_standard.ttf',
            # Map RetroAngela to F-04
            'RetroAngela': 'F-04.ttf',
            # Map GenJyuuGothic to back_standard for phone numbers
            'GenJyuuGothic-P-Heavy': 'back_standard.ttf',
        }
        
        registered_count = 0
        for font_name, font_file in font_mappings.items():
            font_path = self.fonts_dir / font_file
            if font_path.exists():
                try:
                    pdfmetrics.registerFont(TTFont(font_name, str(font_path)))
                    fonts.register_font(font_name, str(font_path))
                    registered_count += 1
                except Exception as e:
                    pass  # May already be registered
            else:
                print(f"[WARN] Font file not found: {font_path}")
        
        print(f"[OK] Registered {registered_count} custom fonts (F-04, back_standard)")
    
    def _load_template(self) -> str:
        """Load SVG template content"""
        with open(self.template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _apply_font_styles(self, svg_content: str) -> str:
        """
        Apply Alibaba PuHuiTi font styles to all text elements.
        Replace all original fonts with Alibaba PuHuiTi series.
        """
            
        # === 1. 主标题: MicrosoftYaHeiLight 41.2px -> AlibabaPuHuiTi-Medium 40px ===
        svg_content = svg_content.replace(
            "font-family=\"'MicrosoftYaHeiLight'\" font-size=\"41.2062px\"",
            "font-family=\"'AlibabaPuHuiTi-Medium'\" font-size=\"40px\""
        )
            
        # === 2. SKU编号: Swiss721BT-Heavy 26.3px -> AlibabaPuHuiTi-Heavy 26.3px (红色) ===
        svg_content = svg_content.replace(
            "font-family=\"'Swiss721BT-Heavy'\" font-size=\"26.2986px\"",
            "font-family=\"'AlibabaPuHuiTi-Heavy'\" font-size=\"26.3px\""
        )
            
        # === 3. 栏目标题: DingTalk-JinBuTi 14px -> AlibabaPuHuiTi-SemiBold 14px (正体) ===
        svg_content = svg_content.replace(
            "font-family=\"'DingTalk-JinBuTi'\" font-size=\"14px\"",
            "font-family=\"'AlibabaPuHuiTi-SemiBold'\" font-size=\"14px\""
        )
            
        # === 4. 正文内容: MicrosoftYaHeiUI 11px -> AlibabaPuHuiTi-Regular 12px ===
        svg_content = svg_content.replace(
            "font-family=\"'MicrosoftYaHeiUI'\" font-size=\"11px\"",
            "font-family=\"'AlibabaPuHuiTi-Regular'\" font-size=\"12px\""
        )
            
        # === 5. MicrosoftYaHeiUILight -> AlibabaPuHuiTi-Regular ===
        svg_content = svg_content.replace(
            "font-family=\"'MicrosoftYaHeiUILight'\"",
            "font-family=\"'AlibabaPuHuiTi-Regular'\""
        )
            
        # === 6. 尺寸标注: 17px ===
        svg_content = svg_content.replace(
            "font-family=\"'MicrosoftYaHeiUI'\" font-size=\"17.0079px\"",
            "font-family=\"'AlibabaPuHuiTi-Regular'\" font-size=\"17px\""
        )
            
        # === 7. AdobeSongStd -> AlibabaPuHuiTi-Regular ===
        svg_content = svg_content.replace(
            "font-family=\"'AdobeSongStd-Light-GBpc-EUC-H'\"",
            "font-family=\"'AlibabaPuHuiTi-Regular'\""
        )
            
        # === 8. 背面号码: GenJyuuGothic-P-Heavy -> back_standard ===
        # Keep as-is, already mapped to back_standard in _register_fonts
            
        # === 9. 效果图文字: RetroAngela -> F-04 ===
        # Keep as-is, already mapped to F-04 in _register_fonts
            
        # === 10. 面单样版: MicrosoftYaHeiUI 49.8712px -> AlibabaPuHuiTi-Regular 49.9px ===
        svg_content = svg_content.replace(
            "font-family=\"'MicrosoftYaHeiUI'\" font-size=\"49.8712px\"",
            "font-family=\"'AlibabaPuHuiTi-Regular'\" font-size=\"49.9px\""
        )
            
        # === 11. 面单尺寸: MicrosoftYaHeiUI 26.4836px -> AlibabaPuHuiTi-Regular 26.5px ===
        svg_content = svg_content.replace(
            "font-family=\"'MicrosoftYaHeiUI'\" font-size=\"26.4836px\"",
            "font-family=\"'AlibabaPuHuiTi-Regular'\" font-size=\"26.5px\""
        )
            
        print("[OK] Applied Alibaba PuHuiTi font styles to all elements")
        return svg_content
    
    def _fill_template(self, svg_content: str, data: Dict[str, Any]) -> str:
        """Replace placeholders in SVG with actual data and apply font styles"""
        
        # Step 1: Apply font style modifications
        svg_content = self._apply_font_styles(svg_content)
        
        # Step 2: Build replacement map
        replacements = {
            # Order Info
            "3891559803": str(data.get("order_id", "3891559803")),
            "John Smith": str(data.get("customer_name", "John Smith")),
            "2026-02-01": str(data.get("order_date", "2026-02-01")),
            "2026-02-03": str(data.get("ship_date", "2026-02-03")),
            
            # Product Info (Chinese)
            ">骨头形<": f">{data.get('shape', '骨头形')}<",
            ">骨头型<": f">{data.get('shape', '骨头形')}<",
            ">金色<": f">{data.get('color', '金色')}<",
            ">大<": f">{data.get('size', '大')}<",
            ">抛光<": f">{data.get('craft', '抛光')}<",
            
            # Customization
            ">ALice<": f">{data.get('front_text', 'ALice')}<",
            ">F-04<": f">{data.get('front_font', 'F-04')}<",
            ">0412345678<": f">{data.get('back_text', '0412345678')}<",
            
            # SKU (with color preserved)
            ">B-E01A<": f">{data.get('sku', 'B-E01A')}<",
            
            # Shipping Label - tracking number
            ">04123456780412345678<": f">{data.get('tracking_number', data.get('order_id', '')[:20])}<",
            
            # Shipping info section
            ">Australia<": f">{data.get('country', 'Australia')}<",
            ">Trish Weeden<": f">{data.get('recipient_name', 'Trish Weeden')}<",
            ">TAS<": f">{data.get('state', 'TAS')}<",
            ">YOUNGTOWN<": f">{data.get('city', 'YOUNGTOWN')}<",
            ">7249<": f">{data.get('postal_code', '7249')}<",
            ">36 Jubilee Rd<": f">{data.get('address', '36 Jubilee Rd')}<",
            
            # Postlink label
            ">Demi Brooker<": f">{data.get('recipient_name', 'Demi Brooker')}<",
            ">3/1A Salisbury Rd<": f">{data.get('recipient_address', '3/1A Salisbury Rd')}<",
            ">2029;Rose Bay<": f">{data.get('postal_city', '2029;Rose Bay')}<",
            ">AU<": f">{data.get('country_code', 'AU')}<",
            
            # Dimensions
            ">45 mm<": f">{data.get('width_mm', 45)} mm<",
            ">26 mm<": f">{data.get('height_mm', 26)} mm<",
        }
        
        result = svg_content
        for old, new in replacements.items():
            result = result.replace(old, new)
        
        return result
    
    def generate_pdf(self, order_data) -> Optional[Path]:
        """Generate PDF from SVG template with order data"""
        
        try:
            # Prepare data dictionary
            data = self._prepare_data(order_data)
            
            # Load and fill template
            svg_content = self._load_template()
            filled_svg = self._fill_template(svg_content, data)
            
            # Save temporary SVG
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_svg_path = self.output_dir / f"temp_{order_data.order_id}_{timestamp}.svg"
            pdf_path = self.output_dir / f"POD_{order_data.order_id}_{timestamp}.pdf"
            
            with open(temp_svg_path, 'w', encoding='utf-8') as f:
                f.write(filled_svg)
            
            # Convert SVG to PDF
            drawing = svg2rlg(str(temp_svg_path))
            if drawing:
                renderPDF.drawToFile(drawing, str(pdf_path))
                print(f"[OK] PDF generated: {pdf_path.name}")
                
                # Clean up temp SVG
                temp_svg_path.unlink()
                
                return pdf_path
            else:
                print("[ERROR] Failed to parse SVG")
                return None
                
        except Exception as e:
            print(f"[ERROR] PDF generation failed: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _prepare_data(self, order_data) -> Dict[str, Any]:
        """Prepare data dictionary from OrderData object"""
        shipping = order_data.shipping
        
        return {
            "order_id": order_data.order_id,
            "customer_name": order_data.customer_name,
            "order_date": order_data.order_date,
            "ship_date": order_data.ship_date,
            
            "shape": order_data.shape,
            "color": order_data.color,
            "size": order_data.size,
            "craft": order_data.craft,
            
            "front_text": order_data.front_text,
            "front_font": order_data.front_font,
            "back_text": order_data.back_text,
            
            "sku": order_data.sku,
            
            "tracking_number": shipping.tracking_number,
            "recipient_name": shipping.recipient_name,
            "recipient_address": shipping.recipient_address,
            "country": shipping.recipient_country,
            "country_code": shipping.recipient_country_code,
            "state": shipping.recipient_state,
            "city": shipping.recipient_city,
            "postal_code": shipping.recipient_postal_code,
            "address": shipping.recipient_address,
            "postal_city": f"{shipping.recipient_postal_code};{shipping.recipient_city}",
            
            "width_mm": order_data.width_mm,
            "height_mm": order_data.height_mm,
        }
    
    def generate_from_raw_data(self, raw_data: Dict[str, Any]) -> Optional[Path]:
        """Generate PDF from raw data dictionary"""
        from src.services.shipping_service import shipping_service
        order_data = shipping_service.create_order_data(raw_data)
        shipping_service.create_shipping_label(order_data)
        return self.generate_pdf(order_data)


svg_pdf_service = SVGPDFService()

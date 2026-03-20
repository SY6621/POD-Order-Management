# -*- coding: utf-8 -*-
"""
SVG Template to PDF Service
Pixel-perfect PDF generation using SVG template
"""

import re
import base64
import requests
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


# ============================================================
# 效果图区域定义（黑色框内的坐标）
# ============================================================

# 黑色框的位置和尺寸
BLACK_BOX = {
    "x": 225.5,
    "y": 265.9,
    "width": 331.7,
    "height": 212.6,
}

# 正面效果图区域（黑色框左半部分）
FRONT_AREA = {
    "x": 225.5,
    "y": 265.9,
    "width": 171.8,  # 到中间 x=397.3
    "height": 150,   # 上半部分，偏上
}

# 背面效果图区域（黑色框右半部分）
BACK_AREA = {
    "x": 397.3,
    "y": 265.9,
    "width": 160,
    "height": 150,
}


# ============================================================
# 各形状的尺寸数据（毫米 -> 像素换算：1mm ≈ 2.83px）
# ============================================================

# 形状尺寸配置（像素值，按照实际显示效果调整）
SHAPE_SIZES = {
    # 圆形
    "Circle": {
        "L": {"width_mm": 32, "height_mm": 32, "scale": 1.4},   # 大号
        "S": {"width_mm": 23, "height_mm": 23, "scale": 1.0},   # 小号
    },
    # 心形
    "Heart": {
        "L": {"width_mm": 32, "height_mm": 30, "scale": 1.4},
        "S": {"width_mm": 23, "height_mm": 21, "scale": 1.0},
    },
    # 骨头形
    "Bone": {
        "L": {"width_mm": 45, "height_mm": 26, "scale": 1.0},
        "S": {"width_mm": 28, "height_mm": 16, "scale": 0.62},
    },
}


# ============================================================
# 效果图形状 Path 数据（从模板 SVG 提取）
# ============================================================

# 形状 Path 数据
SHAPE_PATHS = {
    # 心形 (Heart) - G 系列
    "Heart": {
        "d": "M69.8686 14.0786C68.5094 14.8158 64.5094 17.3092 62.1553 18.8983 47.5075 28.7844 36.1069 40.7415 30.2145 52.3956 25.9707 60.7907 24.5971 68.7719 26.1031 76.3129 26.9495 80.555 28.7402 84.437 31.4827 87.963 32.3107 89.0291 34.2221 91.0242 35.3058 91.9573 38.7692 94.9346 42.7311 96.8275 46.8524 97.4693 48.0892 97.6603 50.9553 97.6586 52.6629 97.4662 55.98 97.0889 58.8903 96.243 61.4594 94.8977 64.0329 97.8106 67.2554 99.5443 70.7536 99.5443 74.2912 99.5443 77.5477 97.772 80.1351 94.7988 82.5721 96.0979 85.3194 96.9633 88.3412 97.3706 89.6519 97.5475 90.8787 97.6374 92.0486 97.6385 94.134 97.6408 96.0392 97.3613 97.9174 96.7924 103.7109 95.0369 109.3989 90.2472 112.7044 84.3412 114.5509 81.0442 115.5943 77.7268 116.1085 73.5415 116.2627 72.21 116.2627 68.1591 116.0768 66.6978 115.638 63.1244 114.8357 60.035 113.4584 56.552 107.6851 41.9811 92.8831 26.5946 73.489 14.9995L71.905 14.0522C71.4226 13.752 70.4282 13.7837 69.8686 14.0786ZM71.0152 95.0488C73.5985 95.0488 75.6924 92.9548 75.6924 90.3716 75.6924 87.7884 73.5985 85.6945 71.0152 85.6945 68.432 85.6945 66.3381 87.7884 66.3381 90.3716 66.3381 92.9548 68.432 95.0488 71.0152 95.0488",
        "viewbox_width": 142,
        "viewbox_height": 113,
        "text_y_offset": 75,  # 文字相对于形状中心的 Y 偏移
    },
    # 圆形 (Circle) - C 系列
    "Circle": {
        "d": "M70.8656 86.5749C68.2826 86.5749 66.1887 88.6689 66.1887 91.2521 66.1887 93.835 68.2826 95.9298 70.8656 95.9298 73.4488 95.9298 75.5427 93.835 75.5427 91.2521 75.5427 88.6689 73.4488 86.5749 70.8656 86.5749ZM70.8656 102.331C45.6608 102.331 25.2286 81.898 25.2286 56.6923 25.2286 31.4872 45.6608 11.0551 70.8656 11.0551 96.0707 11.0551 116.5037 31.4872 116.5037 56.6923 116.5037 81.898 96.0707 102.331 70.8656 102.331",
        "viewbox_width": 142,
        "viewbox_height": 113,
        "text_y_offset": 60,
    },
    # 骨头形 (Bone) - E 系列 - 使用绝对坐标
    "Bone": {
        "d": "M276.3,369.9c0.9-0.8,0.9-2.1,0-2.9c-4.2-3.8-6.6-9.2-6.5-15.1c0.2-10.9,9.4-19.8,20.9-20.1c9.2-0.2,16.3,4,19.1,9.9c0.3,0.9,1.2,1.5,2.2,1.5h6.9c1.1,0,2.2-0.7,2.8-1.7c2.8-4.9,7-8.1,11.8-8.1c4.7,0,9,3.1,11.8,8.1c0.6,1,1.6,1.7,2.8,1.7h6.9c1,0,1.9-0.6,2.2-1.5c2.9-5.8,9.9-10.1,19.1-9.9c11.4,0.2,20.7,9.2,20.9,20.1c0.1,6-2.5,11.4-6.5,15.1c-0.9,0.8-0.9,2.1,0,2.9c4.2,3.8,6.6,9.1,6.5,15.1c-0.2,10.9-9.6,19.8-20.9,20.1c-6,0.2-17.2-4.5-20.1-11.2c-0.3-0.9-1.2-1.5-2.2-1.5h-19.6h-4.3h-17c-1,0-1.9,0.6-2.2,1.5c-2.9,6.9-14.2,11.5-20.1,11.2c-11.4-0.3-20.7-9.2-20.9-20.1C269.7,379,272.3,373.8,276.3,369.9z M333.6,337.7c2.8,0,4.9,2.6,4.4,5.5c-0.3,1.7-1.6,3-3.3,3.4c-3,0.8-5.7-1.5-5.7-4.4C329.1,339.7,331.1,337.7,333.6,337.7",
        "is_absolute": True,
        "viewbox_width": 128,
        "viewbox_height": 75,
        "text_y_offset": 45,
    },
}

# 颜色映射（英文 -> 填充色）
COLOR_FILLS = {
    "Silver": "#9f9fa0",
    "Gold": "#ebcd7b",
    "RoseGold": "#dabf9b",
    "Black": "#231916",
    # 中文映射
    "银色": "#9f9fa0",
    "钢本色": "#9f9fa0",
    "金色": "#ebcd7b",
    "玫瑰金": "#dabf9b",
    "黑色": "#231916",
}


class SVGPDFService:
    """Generate PDF by filling SVG template with order data"""
    
    # Placeholder mappings: {{PLACEHOLDER}} -> data field
    PLACEHOLDERS = {
        # 订单信息
        "{{ORDER_ID}}": "order_id",
        "{{ORDER_DATE}}": "order_date",
        "{{SHIP_DATE}}": "ship_date",
        
        # 产品规格
        "{{SHAPE}}": "shape",
        "{{COLOR}}": "color",
        "{{SIZE}}": "size",
        "{{CRAFT}}": "craft",
        "{{SKU}}": "sku",
        
        # 定制内容
        "{{FRONT_TEXT}}": "front_text",
        "{{FRONT_FONT}}": "front_font",
        "{{BACK_TEXT}}": "back_text",
        
        # 效果图
        "{{EFFECT_FRONT_TEXT}}": "front_text",
        "{{EFFECT_BACK_TEXT}}": "back_text",
        
        # 物流信息
        "{{TRACKING_NUMBER}}": "tracking_number",
        "{{COUNTRY}}": "country",
        "{{RECIPIENT_NAME}}": "recipient_name",
        "{{STATE}}": "state",
        "{{CITY}}": "city",
        "{{POSTAL_CODE}}": "postal_code",
        "{{ADDRESS}}": "address",
        
        # 尺寸
        "{{WIDTH_MM}}": "width_mm",
        "{{HEIGHT_MM}}": "height_mm",
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
    
    def _get_effect_shape_svg(self, shape: str, color: str, position: str = "front", size: str = "L") -> Dict[str, Any]:
        """
        生成效果图形状的 SVG 元素，自动居中在指定区域
        
        Args:
            shape: 形状名称 (Heart/Circle/Bone 或 心形/圆形/骨头形)
            color: 颜色名称 (Silver/Gold/RoseGold/Black 或中文)
            position: front 或 back
            size: L 或 S
        
        Returns:
            包含 SVG 元素和边界框信息的字典
        """
        # 标准化形状名称
        shape_map = {
            "心形": "Heart", "Heart": "Heart",
            "圆形": "Circle", "Circle": "Circle",
            "骨头形": "Bone", "Bone": "Bone", "骨形": "Bone",
        }
        shape_key = shape_map.get(shape, "Bone")
        
        # 标准化尺寸
        size_key = "L" if size.upper() in ["L", "大"] else "S"
        
        # 获取颜色填充
        fill_color = COLOR_FILLS.get(color, "#E5C87A")
        
        # 获取形状 path 数据
        shape_data = SHAPE_PATHS.get(shape_key, SHAPE_PATHS["Bone"])
        path_d = shape_data["d"]
        is_absolute = shape_data.get("is_absolute", False)
        
        # 获取形状的视口尺寸
        viewbox_width = shape_data.get("viewbox_width", 142)
        viewbox_height = shape_data.get("viewbox_height", 113)
        text_y_offset = shape_data.get("text_y_offset", 60)
        
        # 获取缩放比例 - 统一使用更大的比例使所有形状大小相近
        # 骨头形作为基准 (scale=1.0)，圆形和心形需要放大到相似视觉大小
        shape_size = SHAPE_SIZES.get(shape_key, SHAPE_SIZES["Bone"]).get(size_key, {})
        base_scale = shape_size.get("scale", 1.0)
        
        # 统一视觉大小：圆形和心形需要额外放大
        if shape_key in ["Circle", "Heart"]:
            scale = base_scale * 1.6  # 额外放大 1.6 倍
        else:
            scale = base_scale
        
        # 确定目标区域
        if position == "front":
            area = FRONT_AREA
        else:
            area = BACK_AREA
        
        # 计算居中位置（在区域内水平居中、垂直居中偏上）
        area_center_x = area["x"] + area["width"] / 2
        area_center_y = area["y"] + area["height"] / 2 - 10  # 稍微偏上
        
        # 计算缩放后的尺寸
        scaled_width = viewbox_width * scale
        scaled_height = viewbox_height * scale
        
        # 计算平移量使形状居中
        translate_x = area_center_x - scaled_width / 2
        translate_y = area_center_y - scaled_height / 2
        
        # 生成 SVG 元素
        if is_absolute:
            # 骨头形已经是绝对坐标，保持原有逻辑
            if position == "back":
                # 背面需要调整 x 坐标（向右移动 134.7）
                path_d = self._adjust_path_x(path_d, 134.7)
            svg_element = f'<g><path fill-rule="evenodd" fill="{fill_color}" d="{path_d}"/></g>'
            # 骨头形的边界框（基于原始坐标）
            bbox = {
                "x": 276.3 if position == "front" else 276.3 + 134.7,
                "y": 337.7,
                "width": 128,
                "height": 75,
            }
        else:
            # 心形和圆形需要计算居中位置
            svg_element = f'<g transform="translate({translate_x}, {translate_y}) scale({scale})"><path fill-rule="evenodd" fill="{fill_color}" d="{path_d}"/></g>'
            # 计算边界框（用于尺寸标注）
            bbox = {
                "x": translate_x,
                "y": translate_y,
                "width": scaled_width,
                "height": scaled_height,
            }
        
        # 计算文字居中位置
        text_x = area_center_x
        text_y = translate_y + (scaled_height / 2) + (text_y_offset * scale / viewbox_height * scaled_height * 0.3)
        
        return {
            "svg": svg_element,
            "bbox": bbox,
            "text_x": text_x,
            "text_y": text_y,
            "scale": scale,
        }
    
    def _adjust_path_x(self, path_d: str, offset: float) -> str:
        """调整 path 的 x 坐标"""
        # 简单的正则替换 M 后的第一个数字
        def adjust_coords(match):
            x = float(match.group(1))
            return f"M{x + offset},"
        return re.sub(r'M(\d+\.?\d*),', adjust_coords, path_d)
    
    def _generate_dimension_lines(self, bbox: Dict[str, float], width_mm: int, height_mm: int) -> tuple:
        """
        生成尺寸标注线 SVG
        
        Args:
            bbox: 形状的边界框 {"x", "y", "width", "height"}
            width_mm: 宽度毫米值
            height_mm: 高度毫米值
        
        Returns:
            (宽度标注线 SVG, 高度标注线 SVG)
        """
        x, y, w, h = bbox["x"], bbox["y"], bbox["width"], bbox["height"]
        
        # 标注线偏移量
        offset = 15
        tick = 3
        
        # 宽度标注线（水平，在形状上方）
        width_y = y - offset
        width_text_x = x + w / 2 - 15  # 文字居中
        width_text_y = width_y - 5
        
        width_svg = f'''<g>
            <line fill="none" stroke="#E71F19" stroke-width="0.5" x1="{x}" y1="{width_y}" x2="{x + w}" y2="{width_y}"/>
            <line fill="none" stroke="#E71F19" stroke-width="0.5" x1="{x}" y1="{width_y - tick}" x2="{x}" y2="{width_y + tick}"/>
            <line fill="none" stroke="#E71F19" stroke-width="0.5" x1="{x + w}" y1="{width_y - tick}" x2="{x + w}" y2="{width_y + tick}"/>
            <text transform="matrix(1 0 0 1 {width_text_x} {width_text_y})" fill="#E71F19" font-family="'AlibabaPuHuiTi-Regular'" font-size="14px">{width_mm} mm</text>
        </g>'''
        
        # 高度标注线（垂直，在形状左侧）
        height_x = x - offset
        height_text_x = height_x - 20
        height_text_y = y + h / 2 + 5  # 文字居中
        
        height_svg = f'''<g>
            <line fill="none" stroke="#E71F19" stroke-width="0.5" x1="{height_x}" y1="{y}" x2="{height_x}" y2="{y + h}"/>
            <line fill="none" stroke="#E71F19" stroke-width="0.5" x1="{height_x - tick}" y1="{y}" x2="{height_x + tick}" y2="{y}"/>
            <line fill="none" stroke="#E71F19" stroke-width="0.5" x1="{height_x - tick}" y1="{y + h}" x2="{height_x + tick}" y2="{y + h}"/>
            <text transform="matrix(0 -1 1 0 {height_text_x} {height_text_y})" fill="#E71F19" font-family="'AlibabaPuHuiTi-Regular'" font-size="14px">{height_mm} mm</text>
        </g>'''
        
        return width_svg, height_svg
    
    def _get_product_photo_base64(self, sku: str, size: str = "L") -> str:
        """
        从 Supabase Storage 获取产品实拍图并转为 base64
        
        Args:
            sku: SKU 编码 (如 B-G01B)
            size: 尺寸 L/S
        
        Returns:
            base64 编码的图片数据（含 data:image/jpeg;base64, 前缀）
        """
        try:
            from PIL import Image
            
            # 确定目录
            size_dir = "large" if size.upper() in ["L", "大"] else "small"
            
            # 构建 Supabase Storage URL
            photo_url = f"{settings.SUPABASE_URL}/storage/v1/object/public/photos/{size_dir}/{sku}.jpg"
            
            print(f"[INFO] Loading product photo: {photo_url}")
            
            # 下载图片
            response = requests.get(photo_url, timeout=15)
            if response.status_code == 200:
                # 检查是否是 JPEG 2000 格式（文件头以 \x00\x00\x00 或 jP 开始）
                content = response.content
                is_jp2 = content[:4] == b'\x00\x00\x00\x0c' or content[:2] == b'jP'
                
                if is_jp2:
                    print(f"[INFO] Converting JPEG 2000 to standard JPEG...")
                    # 使用 Pillow 转换格式
                    img = Image.open(BytesIO(content))
                    # 转换为 RGB 模式（如果需要）
                    if img.mode in ('RGBA', 'P', 'LA'):
                        img = img.convert('RGB')
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # 保存为标准 JPEG
                    buffer = BytesIO()
                    img.save(buffer, format='JPEG', quality=90)
                    content = buffer.getvalue()
                    print(f"[OK] Converted to JPEG: {len(content) / 1024:.1f} KB")
                
                # 转为 base64
                photo_base64 = base64.b64encode(content).decode('utf-8')
                print(f"[OK] Product photo loaded: {sku}.jpg ({len(content) / 1024:.1f} KB)")
                return f"data:image/jpeg;base64,{photo_base64}"
            else:
                print(f"[WARN] Failed to load photo: {response.status_code}")
                return self._get_placeholder_image()
                
        except Exception as e:
            print(f"[ERROR] Failed to load product photo: {e}")
            import traceback
            traceback.print_exc()
            return self._get_placeholder_image()
    
    def _get_placeholder_image(self) -> str:
        """返回占位图片（灰色方块）"""
        # 1x1 灰色 JPEG 的 base64
        return "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/wAALCAABAAEBAREA/8QAFAABAAAAAAAAAAAAAAAAAAAACf/EABQQAQAAAAAAAAAAAAAAAAAAAAD/2gAIAQEAAD8AVN//2Q=="
    
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
        
        # Step 2: 获取形状和尺寸信息
        shape = data.get("shape", "骨头形")
        color = data.get("color", "金色")
        size = data.get("size", "L")
        
        # 标准化形状和尺寸
        shape_map = {
            "心形": "Heart", "Heart": "Heart",
            "圆形": "Circle", "Circle": "Circle",
            "骨头形": "Bone", "Bone": "Bone", "骨形": "Bone",
        }
        shape_key = shape_map.get(shape, "Bone")
        size_key = "L" if str(size).upper() in ["L", "大"] else "S"
        
        # 获取形状的尺寸数据
        shape_size = SHAPE_SIZES.get(shape_key, SHAPE_SIZES["Bone"]).get(size_key, {})
        width_mm = data.get("width_mm") or shape_size.get("width_mm", 45)
        height_mm = data.get("height_mm") or shape_size.get("height_mm", 26)
        
        # Step 3: 获取效果图SVG（优先从 production_documents 读取设计器SVG）
        effect_svg_url = data.get("effect_svg_url", "")
        if effect_svg_url:
            # 使用设计器生成的SVG
            print(f"[INFO] 使用设计器SVG: {effect_svg_url}")
            front_shape_data, back_shape_data = self._get_designer_svg(effect_svg_url, shape, color, size)
        else:
            # 动态生成形状
            print(f"[INFO] 动态生成形状: {shape}/{color}/{size}")
            front_shape_data = self._get_effect_shape_svg(shape, color, "front", size)
            back_shape_data = self._get_effect_shape_svg(shape, color, "back", size)
        
        # 生成尺寸标注线（仅正面需要）
        width_lines, height_lines = self._generate_dimension_lines(
            front_shape_data["bbox"], width_mm, height_mm
        )
        
        # Step 4: 获取产品实拍图
        sku = data.get("sku", "B-E01A")
        # 从 SKU 提取基础编码（去掉颜色后缀取前6位，如 B-E01A -> B-E01A）
        # 实际上需要根据形状和颜色组合来确定实拍图
        sku_base = sku[:6] if len(sku) >= 6 else sku
        photo_base64 = self._get_product_photo_base64(sku_base, size)
        
        # 生成居中的效果图文字
        front_text = str(data.get("front_text", ""))
        back_text = str(data.get("back_text", ""))
        
        # 正面文字 - 居中在形状内
        front_text_svg = f'<text x="{front_shape_data["text_x"]}" y="{front_shape_data["text_y"]}" text-anchor="middle" fill="#333333" font-family="\'RetroAngela\'" font-size="39.637px">{front_text}</text>'
        
        # 背面文字 - 居中在形状内
        back_text_svg = f'<text x="{back_shape_data["text_x"]}" y="{back_shape_data["text_y"]}" text-anchor="middle" fill="#333333" font-family="\'GenJyuuGothic-P-Heavy\'" font-size="17.9641px">{back_text}</text>'
        
        # Step 5: Build replacement map using {{PLACEHOLDER}} format
        replacements = {
            # 效果图形状
            "{{EFFECT_FRONT_SHAPE}}": front_shape_data["svg"],
            "{{EFFECT_BACK_SHAPE}}": back_shape_data["svg"],
            
            # 效果图文字（居中）
            "{{EFFECT_FRONT_TEXT}}": front_text_svg,
            "{{EFFECT_BACK_TEXT}}": back_text_svg,
            
            # 尺寸标注线
            "{{WIDTH_DIMENSION_LINES}}": width_lines,
            "{{HEIGHT_DIMENSION_LINES}}": height_lines,
            
            # 实拍图
            "{{PRODUCT_PHOTO_BASE64}}": photo_base64,
            
            # 订单信息
            "{{ORDER_ID}}": str(data.get("order_id", "")),
            "{{ORDER_DATE}}": str(data.get("order_date", "")),
            "{{SHIP_DATE}}": str(data.get("ship_date", "")),
            "{{CUSTOMER_NAME}}": str(data.get("customer_name", "")),
            
            # 产品规格（中文）
            "{{SHAPE}}": str(data.get("shape", "")),
            "{{COLOR}}": str(data.get("color", "")),
            "{{SIZE}}": str(data.get("size", "")),
            "{{CRAFT}}": str(data.get("craft", "抛光")),
            
            # SKU
            "{{SKU}}": str(data.get("sku", "")),
            
            # 定制内容
            "{{FRONT_TEXT}}": front_text,
            "{{FRONT_FONT}}": str(data.get("front_font", "")),
            "{{BACK_TEXT}}": back_text,
            
            # 物流信息
            "{{TRACKING_NUMBER}}": str(data.get("tracking_number", "")),
            "{{COUNTRY}}": str(data.get("country", "")),
            "{{RECIPIENT_NAME}}": str(data.get("recipient_name", "")),
            "{{STATE}}": str(data.get("state", "")),
            "{{CITY}}": str(data.get("city", "")),
            "{{POSTAL_CODE}}": str(data.get("postal_code", "")),
            "{{ADDRESS}}": str(data.get("address", "")),
        }
        
        result = svg_content
        for placeholder, value in replacements.items():
            if placeholder in result:
                result = result.replace(placeholder, value)
                # 对于长值只显示前30个字符
                display_value = value[:50] + "..." if len(str(value)) > 50 else value
                print(f"[OK] Replaced {placeholder} → {display_value}")
        
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
            
            # 新增：设计器SVG URL（从外部传入）
            "effect_svg_url": getattr(order_data, 'effect_svg_url', ''),
        }
    
    def generate_from_raw_data(self, raw_data: Dict[str, Any]) -> Optional[Path]:
        """Generate PDF from raw data dictionary"""
        from src.services.shipping_service import shipping_service
        
        # 保存 effect_svg_url（create_order_data 会丢失这个字段）
        effect_svg_url = raw_data.get("effect_svg_url", "")
        
        order_data = shipping_service.create_order_data(raw_data)
        
        # 恢复 effect_svg_url
        order_data.effect_svg_url = effect_svg_url
        
        shipping_service.create_shipping_label(order_data)
        return self.generate_pdf(order_data)
    
    def _get_designer_svg(self, effect_svg_url: str, shape: str, color: str, size: str) -> tuple:
        """
        从设计器SVG URL读取并解析正反面效果图
        
        Returns:
            (front_shape_data, back_shape_data) 格式与 _get_effect_shape_svg 相同
        """
        try:
            # 下载SVG内容
            response = requests.get(effect_svg_url, timeout=30)
            if response.status_code != 200:
                print(f"[WARN] 无法下载设计器SVG: {effect_svg_url}")
                # 回退到动态生成
                return (
                    self._get_effect_shape_svg(shape, color, "front", size),
                    self._get_effect_shape_svg(shape, color, "back", size)
                )
            
            svg_content = response.text
            print(f"[OK] 下载设计器SVG成功: {len(svg_content)} 字符")
            
            # 解析SVG获取正反面（假设设计器SVG包含正反面）
            # 这里简化处理：将整个SVG作为正面，背面动态生成
            # 实际应该根据设计器SVG结构解析
            
            # 获取默认形状数据用于定位
            front_default = self._get_effect_shape_svg(shape, color, "front", size)
            back_default = self._get_effect_shape_svg(shape, color, "back", size)
            
            # 将设计器SVG嵌入到正面区域
            # 注意：这里需要根据实际SVG结构调整大小和位置
            front_svg = f'<g transform="translate({front_default["bbox"][0]}, {front_default["bbox"][1]}) scale(0.8)">{svg_content}</g>'
            
            front_shape_data = {
                "svg": front_svg,
                "bbox": front_default["bbox"],
                "text_x": front_default["text_x"],
                "text_y": front_default["text_y"],
            }
            
            return front_shape_data, back_default
            
        except Exception as e:
            print(f"[ERROR] 读取设计器SVG失败: {e}")
            # 回退到动态生成
            return (
                self._get_effect_shape_svg(shape, color, "front", size),
                self._get_effect_shape_svg(shape, color, "back", size)
            )
    
    def _download_shipping_label(self, tracking_number: str) -> Optional[str]:
        """
        下载4PX物流面单PDF并转为base64
        
        Returns:
            base64编码的PDF内容，失败返回None
        """
        try:
            from src.services.shipping_service import shipping_service
            
            # 获取面单URL
            label_url = shipping_service.get_label_url(tracking_number)
            if not label_url:
                print(f"[WARN] 无法获取面单URL: {tracking_number}")
                return None
            
            print(f"[INFO] 下载面单: {label_url}")
            
            # 下载PDF
            response = requests.get(label_url, timeout=30)
            if response.status_code != 200:
                print(f"[WARN] 下载面单失败: {response.status_code}")
                return None
            
            # 转为base64
            pdf_base64 = base64.b64encode(response.content).decode('utf-8')
            print(f"[OK] 面单下载成功: {len(pdf_base64)} 字符")
            return pdf_base64
            
        except Exception as e:
            print(f"[ERROR] 下载面单失败: {e}")
            return None


svg_pdf_service = SVGPDFService()

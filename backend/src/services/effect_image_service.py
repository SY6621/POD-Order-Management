# -*- coding: utf-8 -*-
"""Effect image generation service with font embedding + Supabase Storage upload"""

import base64
from pathlib import Path
from datetime import datetime

from src.config.settings import settings
from src.services.template_service import template_service


class EffectImageService:
    TEXT_AREAS = {
        "bone": {"large": (70, 57), "small": (54, 57)},
        "heart": {"large": (70, 57), "small": (54, 57)},
        "circle": {"large": (55, 45), "small": (42, 45)},
    }
    
    FONT_SIZES = {
        "large": {"front": 14, "back": 10},
        "small": {"front": 10, "back": 8},
    }
    
    def __init__(self):
        self.fonts_dir = settings.FONTS_DIR
        self.output_dir = settings.OUTPUT_DIR
        settings.ensure_output_dir()
        self._font_cache = {}
    
    def _load_font_base64(self, font_path):
        if not font_path.exists():
            return None
        if str(font_path) in self._font_cache:
            return self._font_cache[str(font_path)]
        with open(font_path, "rb") as f:
            font_data = base64.b64encode(f.read()).decode("ascii")
        self._font_cache[str(font_path)] = font_data
        return font_data
    
    def _get_font_file(self, font_code):
        code = font_code.upper().replace(" ", "")
        for ext in [".ttf", ".otf"]:
            font_path = self.fonts_dir / f"{code}{ext}"
            if font_path.exists():
                print(f"[OK] Font found: {font_path.name}")
                return font_path
        default_font = self.fonts_dir / "F-01.ttf"
        if default_font.exists():
            print(f"[WARN] Font {font_code} not found, using F-01")
            return default_font
        return None
    
    def _get_font_format(self, font_path):
        ext = font_path.suffix.lower()
        if ext == ".ttf":
            return "truetype"
        elif ext == ".otf":
            return "opentype"
        return "truetype"
    
    def _create_font_style(self, font_path, font_name):
        font_base64 = self._load_font_base64(font_path)
        if not font_base64:
            return ""
        font_format = self._get_font_format(font_path)
        ext = font_path.suffix.lower().replace(".", "")
        return f'''
  <defs>
    <style type="text/css">
      @font-face {{
        font-family: '{font_name}';
        src: url('data:font/{ext};base64,{font_base64}') format('{font_format}');
      }}
    </style>
  </defs>'''
    
    def generate_and_upload(self, order: dict) -> dict:
        """
        一键处理：根据订单信息生成正面+背面效果图并上传到 Supabase Storage。
        返回 {"effect_image_url": str, "effect_image_back_url": str}
        """
        from src.services.database_service import db

        etsy_id = order.get("etsy_order_id", "unknown")
        shape = order.get("product_shape", "Heart")
        color = order.get("product_color", "Gold")
        size = order.get("product_size", "Large")
        front_text = order.get("front_text", "")
        back_text = order.get("back_text", "")
        font_code = order.get("font_code") or "F-01"

        result = self.generate_effect_svg(
            shape=shape, color=color, size=size,
            text_front=front_text, text_back=back_text,
            font_code=font_code, order_id=etsy_id
        )
        if not result:
            print(f"❌ 效果图生成失败: 订单 {etsy_id}")
            return {}

        front_path, back_path = result
        order_id = order.get("id")
        update_data = {}

        # 上传正面 SVG
        front_url = db.upload_file("effect-images", front_path, f"{etsy_id}_front.svg")
        if front_url:
            update_data["effect_image_url"] = front_url
            print(f"✅ 正面效果图 URL: {front_url}")

        # 上传背面 SVG（如果有背面模板且有背面文字）
        back_url = None
        if back_path:
            back_url = db.upload_file("effect-images", back_path, f"{etsy_id}_back.svg")
            if back_url:
                update_data["effect_image_back_url"] = back_url
                print(f"✅ 背面效果图 URL: {back_url}")

        # 一次性将所有 URL 写回 orders 表
        if update_data and order_id:
            db.update("orders", {"id": order_id}, update_data)
            print(f"✅ 效果图 URL 已写入数据库")

        return {
            "effect_image_url": front_url,
            "effect_image_back_url": back_url,
            "svg_front_path": front_path,
            "svg_back_path": back_path
        }

    def generate_effect_svg(self, shape, color, size, text_front, text_back="", font_code="F-01", order_id=""):
        front_template = template_service.get_template_content(shape, color, size, "F")
        back_template = template_service.get_template_content(shape, color, size, "B")
        if not front_template:
            print("[ERROR] Front template not found")
            return None
        shape_lower = shape.lower()
        size_lower = size.lower()
        text_pos = self.TEXT_AREAS.get(shape_lower, {}).get(size_lower, (50, 50))
        font_size_front = self.FONT_SIZES.get(size_lower, {}).get("front", 12)
        font_size_back = self.FONT_SIZES.get(size_lower, {}).get("back", 10)
        front_font_path = self._get_font_file(font_code)
        back_font_path = self.fonts_dir / "back_standard.ttf"
        front_svg = self._add_text_with_font(front_template, text_front, text_pos, font_size_front, front_font_path, f"CustomFont_{font_code}")
        back_svg = None
        if back_template and text_back:
            back_svg = self._add_text_with_font(back_template, text_back, text_pos, font_size_back, back_font_path, "BackFont")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        order_prefix = f"{order_id}_" if order_id else ""
        front_filename = f"{order_prefix}{shape}_{color}_{size}_front_{timestamp}.svg"
        front_path = self.output_dir / front_filename
        front_path.write_text(front_svg, encoding="utf-8")
        print(f"[OK] Front SVG saved: {front_filename}")
        back_path = None
        if back_svg:
            back_filename = f"{order_prefix}{shape}_{color}_{size}_back_{timestamp}.svg"
            back_path = self.output_dir / back_filename
            back_path.write_text(back_svg, encoding="utf-8")
            print(f"[OK] Back SVG saved: {back_filename}")
        return (front_path, back_path)
    
    def _add_text_with_font(self, svg_content, text, position, font_size, font_path, font_name):
        x, y = position
        font_style = ""
        font_family = "sans-serif"
        if font_path and font_path.exists():
            font_style = self._create_font_style(font_path, font_name)
            font_family = font_name
        text_element = f'''
  <text x="{x}" y="{y}" font-size="{font_size}" font-family="'{font_family}', sans-serif" text-anchor="middle" dominant-baseline="middle" fill="#333333">{text}</text>
'''
        if font_style:
            svg_tag_end = svg_content.find(">") + 1
            svg_with_font = svg_content[:svg_tag_end] + font_style + svg_content[svg_tag_end:]
        else:
            svg_with_font = svg_content
        svg_final = svg_with_font.replace("</svg>", f"{text_element}</svg>")
        return svg_final


effect_image_service = EffectImageService()
# -*- coding: utf-8 -*-
"""Template loading service"""

import os
from pathlib import Path
from typing import Optional, Dict, List
from src.config.settings import settings


class TemplateService:
    """SVG template loading service"""
    
    SHAPE_MAP = {
        "bone": "E",
        "heart": "G", 
        "circle": "C",
    }
    
    COLOR_MAP = {
        "silver": "A",
        "gold": "B",
        "rose gold": "C",
        "rosegold": "C",
        "black": "D",
        # 支持直接传入颜色代码
        "a": "A",
        "b": "B",
        "c": "C",
        "d": "D",
        "g": "B",  # G 表示 Gold
        "s": "A",  # S 表示 Silver
    }
    
    # 颜色代码到模板文件名的映射
    COLOR_NAME_MAP = {
        "A": "Silver",
        "B": "Gold",
        "C": "RoseGold",
        "D": "Black",
    }
    
    SIZE_MAP = {
        "large": ("01", "L"),
        "small": ("02", "S"),
    }
    
    def __init__(self):
        self.templates_dir = settings.TEMPLATES_DIR
        self.large_dir = self.templates_dir / "B不锈钢_模版_大号"
        self.small_dir = self.templates_dir / "B不锈钢_模版_小号"
    
    def get_template_path(self, shape: str, color: str, size: str, side: str = "F") -> Optional[Path]:
        """
        Get SVG template path by product attributes
        
        Args:
            shape: bone, heart, circle
            color: silver, gold, rose gold, black
            size: large, small
            side: F (front) or B (back)
        
        Returns:
            Path to SVG template file
        """
        shape_lower = shape.lower().strip()
        color_lower = color.lower().strip()
        size_lower = size.lower().strip()
        
        shape_code = self.SHAPE_MAP.get(shape_lower)
        color_code = self.COLOR_MAP.get(color_lower)
        size_info = self.SIZE_MAP.get(size_lower)
        
        if not all([shape_code, color_code, size_info]):
            print(f"[ERROR] Invalid params: shape={shape}, color={color}, size={size}")
            return None
        
        size_num, size_letter = size_info
        
        # Build filename: B-E01A_Bone_Silver - L-F.svg
        # 使用 COLOR_NAME_MAP 获取正确的颜色名称
        color_name = self.COLOR_NAME_MAP.get(color_code, "Silver")
        
        shape_name = shape.title()
        filename = f"B-{shape_code}{size_num}{color_code}_{shape_name}_{color_name} - {size_letter}-{side}.svg"
        
        # Select directory
        template_dir = self.large_dir if size_lower == "large" else self.small_dir
        template_path = template_dir / filename
        
        if template_path.exists():
            print(f"[OK] Template found: {filename}")
            return template_path
        else:
            print(f"[ERROR] Template not found: {filename}")
            return None
    
    def get_template_content(self, shape: str, color: str, size: str, side: str = "F") -> Optional[str]:
        """Get SVG template content"""
        path = self.get_template_path(shape, color, size, side)
        if path:
            return path.read_text(encoding="utf-8")
        return None
    
    def list_available_templates(self) -> List[Dict]:
        """List all available templates"""
        templates = []
        
        for dir_path in [self.large_dir, self.small_dir]:
            if dir_path.exists():
                for f in dir_path.glob("*.svg"):
                    templates.append({
                        "filename": f.name,
                        "path": str(f),
                        "size": "large" if "大号" in str(dir_path) else "small"
                    })
        
        return templates


template_service = TemplateService()
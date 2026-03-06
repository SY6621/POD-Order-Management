# -*- coding: utf-8 -*-
"""
SVG 模板重构脚本
将逐字符拆分的文本合并为整体文本块，并使用 {{PLACEHOLDER}} 格式的占位符

用途：修复 PDF 生成时文本无法替换的问题
"""

import re
from pathlib import Path

# 源文件和目标文件路径
BACKEND_DIR = Path(__file__).parent.parent
SRC_SVG = BACKEND_DIR / "src" / "模版-设计图-校对文档-快递面单V2_backup.svg"
DST_SVG = BACKEND_DIR / "src" / "模版-设计图-校对文档-快递面单V2.svg"


def read_svg(path: Path) -> str:
    """读取 SVG 文件内容"""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def write_svg(path: Path, content: str):
    """写入 SVG 文件"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def replace_single_text(content: str, old_text: str, new_text: str) -> str:
    """替换整体文本块的内容（保留 XML 结构）"""
    # 匹配 >old_text</text> 格式
    pattern = f'>{re.escape(old_text)}</text>'
    replacement = f'>{new_text}</text>'
    return content.replace(pattern, replacement)


def remove_char_by_char_text(content: str, start_line: int, end_line: int) -> tuple:
    """
    删除指定行范围内的逐字符文本元素
    返回 (新内容, 删除的行数)
    """
    lines = content.split('\n')
    # 注意：行号从 1 开始，列表索引从 0 开始
    del lines[start_line - 1:end_line]
    return '\n'.join(lines), end_line - start_line + 1


def insert_text_element(content: str, after_line: int, text_element: str) -> str:
    """在指定行后插入文本元素"""
    lines = content.split('\n')
    lines.insert(after_line, text_element)
    return '\n'.join(lines)


def create_text_element(
    text: str,
    x: float,
    y: float,
    font_family: str = "AlibabaPuHuiTi-Regular",
    font_size: str = "11px",
    fill: str = None,
    transform_scale: tuple = (1, 1)
) -> str:
    """创建 SVG text 元素"""
    fill_attr = f' fill="{fill}"' if fill else ''
    scale_x, scale_y = transform_scale
    return f'\t<text transform="matrix({scale_x} 0 0 {scale_y} {x} {y})"{fill_attr} font-family="\'{font_family}\'" font-size="{font_size}">{text}</text>'


def refactor_svg():
    """主函数：重构 SVG 模板"""
    print("=" * 60)
    print("SVG 模板重构脚本")
    print("=" * 60)
    
    # 读取源文件
    content = read_svg(SRC_SVG)
    print(f"[1] 读取源文件: {SRC_SVG}")
    print(f"    原始行数: {len(content.splitlines())}")
    
    # ===== 步骤 2: 替换整体文本块为占位符 =====
    print("\n[2] 替换整体文本块为占位符...")
    
    replacements = [
        # 产品信息区
        ("骨头形", "{{SHAPE}}"),
        ("金色", "{{COLOR}}"),
        (">大</text>", ">{{SIZE}}</text>"),  # 特殊处理，避免误替换
        ("抛光", "{{CRAFT}}"),
        
        # 定制内容区
        ("ALice", "{{FRONT_TEXT}}"),
        (">F-04</text>", ">{{FRONT_FONT}}</text>"),  # 特殊处理
        ("0412345678", "{{BACK_TEXT}}"),
        
        # 订单信息区
        ("3891559803", "{{ORDER_ID}}"),
        ("2026-02-03", "{{SHIP_DATE}}"),
        ("2026-02-01", "{{ORDER_DATE}}"),
        
        # 效果图区域
        (">Alice</text>", ">{{EFFECT_FRONT_TEXT}}</text>"),  # RetroAngela 字体
        ("13999926688", "{{EFFECT_BACK_TEXT}}"),
        
        # 物流单号（整体文本）
        ("04123456780412345678", "{{TRACKING_NUMBER}}"),
    ]
    
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            print(f"    ✓ '{old}' → '{new}'")
        else:
            print(f"    ✗ 未找到: '{old}'")
    
    # ===== 步骤 3: 处理逐字符拆分的 SKU =====
    print("\n[3] 处理逐字符拆分的 SKU (B-E01A)...")
    
    # SKU 在行 1601-1606，需要删除这 6 行并插入一个整体文本元素
    # 原始位置：transform="matrix(1 0 0 1 250.5892 117.6251)"
    sku_pattern = r'<text transform="matrix\(1 0 0 1 250\.5892 117\.6251\)"[^>]*>B</text>\n\t<text[^>]*>-</text>\n\t<text[^>]*>E</text>\n\t<text[^>]*>0</text>\n\t<text[^>]*>1</text>\n\t<text[^>]*>A</text>'
    
    sku_replacement = '\t<text transform="matrix(1 0 0 1 250.5892 117.6251)" fill="#E60012" font-family="\'AlibabaPuHuiTi-Heavy\'" font-size="26.3px">{{SKU}}</text>'
    
    content, count = re.subn(sku_pattern, sku_replacement, content)
    if count > 0:
        print(f"    ✓ SKU 已合并为整体文本块")
    else:
        print(f"    ✗ SKU 模式未匹配，尝试备用方案...")
        # 备用：直接字符串替换
        old_sku = '''<text transform="matrix(1 0 0 1 250.5892 117.6251)" fill="#E60012" font-family="'Swiss721BT-Heavy'" font-size="26.2986px">B</text>
	<text transform="matrix(1 0 0 1 270.7757 117.6251)" fill="#E60012" font-family="'Swiss721BT-Heavy'" font-size="26.2986px">-</text>
	<text transform="matrix(1 0 0 1 280.3802 117.6251)" fill="#E60012" font-family="'Swiss721BT-Heavy'" font-size="26.2986px">E</text>
	<text transform="matrix(1 0 0 1 298.473 117.6251)" fill="#E60012" font-family="'Swiss721BT-Heavy'" font-size="26.2986px">0</text>
	<text transform="matrix(1 0 0 1 314.5101 117.6251)" fill="#E60012" font-family="'Swiss721BT-Heavy'" font-size="26.2986px">1</text>
	<text transform="matrix(1 0 0 1 330.5482 117.6251)" fill="#E60012" font-family="'Swiss721BT-Heavy'" font-size="26.2986px">A</text>'''
        
        new_sku = '\t<text transform="matrix(1 0 0 1 250.5892 117.6251)" fill="#E60012" font-family="\'AlibabaPuHuiTi-Heavy\'" font-size="26.3px">{{SKU}}</text>'
        
        if old_sku in content:
            content = content.replace(old_sku, new_sku)
            print(f"    ✓ SKU 已通过备用方案合并")
        else:
            print(f"    ✗ SKU 备用方案也未匹配")
    
    # ===== 步骤 4: 处理物流信息区域 =====
    print("\n[4] 处理物流信息区域（逐字符文本）...")
    
    # 定义物流信息的字符序列和替换
    logistics_replacements = [
        # 国家 Australia (行 1623-1631)
        (
            "Australia",
            "1623-1631",
            "410.1428",
            "669.8733",
            "{{COUNTRY}}",
            "AlibabaPuHuiTi-Regular",
            "11px",
            None
        ),
        # 收件人 Trish Weeden (行 1637-1648)
        (
            "Trish Weeden",
            "1637-1648",
            "432.1428",
            "686.8733",
            "{{RECIPIENT_NAME}}",
            "AlibabaPuHuiTi-Regular",
            "11px",
            None
        ),
        # 省州 TAS (行 1654-1656)
        (
            "TAS",
            "1654-1656",
            "432.1428",
            "703.8733",
            "{{STATE}}",
            "AlibabaPuHuiTi-Regular",
            "11px",
            None
        ),
        # 城市 YOUNGTOWN (行 1662-1670)
        (
            "YOUNGTOWN",
            "1662-1670",
            "432.1428",
            "720.8733",
            "{{CITY}}",
            "AlibabaPuHuiTi-Regular",
            "11px",
            None
        ),
        # 邮编 7249 (行 1676-1679)
        (
            "7249",
            "1676-1679",
            "432.1428",
            "737.8733",
            "{{POSTAL_CODE}}",
            "AlibabaPuHuiTi-Regular",
            "11px",
            None
        ),
        # 地址 36 Jubilee Rd (行 1685-1697)
        (
            "36 Jubilee Rd",
            "1685-1697",
            "432.1428",
            "754.8733",
            "{{ADDRESS}}",
            "AlibabaPuHuiTi-Regular",
            "11px",
            None
        ),
    ]
    
    # 对于每个物流字段，找到第一个字符的文本元素，替换为整体文本，删除后续字符
    for text, line_range, x, y, placeholder, font, size, fill in logistics_replacements:
        # 构建要查找的模式 - 查找第一个字符
        first_char = text[0]
        # 创建新的整体文本元素
        fill_attr = f' fill="{fill}"' if fill else ''
        new_element = f'\t\t<text transform="matrix(1 0 0 1 {x} {y})"{fill_attr} font-family="\'{font}\'" font-size="{size}">{placeholder}</text>'
        
        # 使用正则表达式匹配整个字符序列
        # 逐字符的格式: <text ...>A</text> <text ...>u</text> ...
        chars_pattern_parts = []
        for char in text:
            if char == ' ':
                chars_pattern_parts.append(r'<text[^>]*> </text>')
            else:
                chars_pattern_parts.append(f'<text[^>]*>{re.escape(char)}</text>')
        
        # 允许中间有换行和制表符
        chars_pattern = r'[\s\t\n]*'.join(chars_pattern_parts)
        
        content_new, count = re.subn(chars_pattern, new_element, content)
        if count > 0:
            content = content_new
            print(f"    ✓ {text} → {placeholder}")
        else:
            print(f"    ✗ 未找到: {text}")
    
    # ===== 步骤 5: 写入新文件 =====
    print(f"\n[5] 写入新文件: {DST_SVG}")
    write_svg(DST_SVG, content)
    print(f"    新文件行数: {len(content.splitlines())}")
    
    print("\n" + "=" * 60)
    print("SVG 模板重构完成！")
    print("=" * 60)
    
    # 打印占位符清单
    print("\n占位符清单：")
    placeholders = re.findall(r'\{\{[A-Z_]+\}\}', content)
    for p in sorted(set(placeholders)):
        print(f"  - {p}")


if __name__ == "__main__":
    refactor_svg()

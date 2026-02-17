# -*- coding: utf-8 -*-
"""
PDF转SVG完整转换脚本
功能：转换PDF到SVG，自动识别颜色和形状，添加白色背景，按SKU规则命名
"""

import re
from pathlib import Path
import fitz  # PyMuPDF


# 颜色代码映射
COLOR_MAP = {
    "9f9fa0": ("A", "Silver"),
    "ebcd7b": ("B", "Gold"),
    "dabf9b": ("C", "RoseGold"),
    "231916": ("D", "Black"),
}

# 形状识别规则（根据SVG文件大小或路径复杂度）
# 圆形路径较简单，骨形最复杂，心形中等
SHAPE_THRESHOLDS = {
    "Circle": (0, 1000),      # < 1KB
    "Bone": (1500, 2500),     # 1.5-2.5KB
    "Heart": (1000, 1500),    # 1-1.5KB
}

SHAPE_CODE_MAP = {
    "Circle": "C",
    "Bone": "E",
    "Heart": "G",
}


def detect_color(svg_content: str) -> tuple:
    """检测SVG中的填充颜色"""
    match = re.search(r'fill="#([0-9a-fA-F]{6})"', svg_content)
    if match:
        color_hex = match.group(1).lower()
        if color_hex in COLOR_MAP:
            return COLOR_MAP[color_hex]
    return ("X", "Unknown")


def detect_shape(svg_content: str) -> str:
    """根据路径复杂度检测形状"""
    # 计算path的d属性长度
    match = re.search(r'd="([^"]+)"', svg_content)
    if match:
        path_length = len(match.group(1))
        if path_length < 400:
            return "Circle"
        elif path_length > 800:
            return "Bone"
        else:
            return "Heart"
    return "Unknown"


def add_white_background(svg_content: str) -> str:
    """为SVG添加白色矩形背景"""
    # 提取viewBox尺寸
    viewbox_match = re.search(r'viewBox="([^"]+)"', svg_content)
    if viewbox_match:
        viewbox = viewbox_match.group(1)
        parts = viewbox.split()
        if len(parts) == 4:
            width = parts[2]
            height = parts[3]
            
            # 创建白色背景矩形
            white_rect = f'<rect x="0" y="0" width="{width}" height="{height}" fill="#FFFFFF"/>\n'
            
            # 在第一个<g>标签前插入白色背景
            svg_content = re.sub(
                r'(<svg[^>]*>)',
                rf'\1\n{white_rect}',
                svg_content
            )
    
    return svg_content


def clean_svg(svg_content: str) -> str:
    """清理SVG代码，移除冗余内容"""
    # 移除inkscape命名空间属性
    svg_content = re.sub(r'\s*xmlns:inkscape="[^"]*"', '', svg_content)
    svg_content = re.sub(r'\s*inkscape:[a-z]+="[^"]*"', '', svg_content)
    
    # 移除空的属性
    svg_content = re.sub(r'\s+>', '>', svg_content)
    
    return svg_content


def convert_pdf_to_svg(pdf_path: Path, output_dir: Path, size_code: str, size_label: str):
    """
    转换单个PDF文件到SVG
    
    Args:
        pdf_path: PDF文件路径
        output_dir: 输出目录
        size_code: 规格代码 (01=大, 02=小)
        size_label: 规格标签 (L=大, S=小)
    """
    doc = fitz.open(pdf_path)
    
    print(f"\n📄 处理: {pdf_path.name}")
    print(f"   页数: {len(doc)}")
    print("-" * 60)
    
    # 用于跟踪每种外观+颜色的页面计数（区分正反面）
    shape_color_count = {}
    
    results = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        svg_content = page.get_svg_image()
        
        # 检测颜色和形状
        color_code, color_name = detect_color(svg_content)
        shape_name = detect_shape(svg_content)
        shape_code = SHAPE_CODE_MAP.get(shape_name, "X")
        
        # 跟踪正反面
        key = f"{shape_code}{color_code}"
        if key not in shape_color_count:
            shape_color_count[key] = 0
        shape_color_count[key] += 1
        
        # 确定正反面标识
        face = "F" if shape_color_count[key] % 2 == 1 else "B"
        
        # 清理SVG并添加白色背景
        svg_content = clean_svg(svg_content)
        svg_content = add_white_background(svg_content)
        
        # 生成文件名
        # 格式: B-C01A_Circle_Silver - L-F.svg
        sku = f"B-{shape_code}{size_code}{color_code}"
        filename = f"{sku}_{shape_name}_{color_name} - {size_label}-{face}.svg"
        
        # 保存文件
        output_path = output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        file_size = output_path.stat().st_size / 1024
        print(f"   ✅ 页{page_num+1:2d} -> {filename} ({file_size:.1f}KB)")
        
        results.append({
            "sku": sku,
            "shape": shape_name,
            "color": color_name,
            "size": size_label,
            "face": "Front" if face == "F" else "Back",
            "filename": filename
        })
    
    doc.close()
    return results


def main():
    """主函数"""
    # 配置路径
    src_dir = Path(r"d:\ETSY_Order_Automation\backend\src")
    output_dir = Path(r"d:\ETSY_Order_Automation\backend\assets\templates")
    
    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("PDF转SVG批量转换")
    print("=" * 60)
    
    all_results = []
    
    # 处理大号PDF
    large_pdf = src_dir / "B不锈钢外观模版-正反面-大.pdf"
    if large_pdf.exists():
        results = convert_pdf_to_svg(large_pdf, output_dir, "01", "L")
        all_results.extend(results)
    else:
        print(f"❌ 文件不存在: {large_pdf}")
    
    # 处理小号PDF
    small_pdf = src_dir / "B不锈钢外观模版-正反面-小.pdf"
    if small_pdf.exists():
        results = convert_pdf_to_svg(small_pdf, output_dir, "02", "S")
        all_results.extend(results)
    else:
        print(f"❌ 文件不存在: {small_pdf}")
    
    # 生成CSV对照表
    print("\n" + "=" * 60)
    print("生成CSV对照表")
    print("=" * 60)
    
    csv_path = Path(r"d:\ETSY_Order_Automation\backend\assets\sku_data\不锈钢牌_SVG对照表.csv")
    with open(csv_path, 'w', encoding='utf-8-sig') as f:
        f.write("SKU,外观,颜色,规格,正反面,SVG文件名\n")
        for r in all_results:
            f.write(f"{r['sku']},{r['shape']},{r['color']},{r['size']},{r['face']},{r['filename']}\n")
    
    print(f"✅ CSV对照表已生成: {csv_path}")
    
    # 统计
    print("\n" + "=" * 60)
    print("转换完成统计")
    print("=" * 60)
    print(f"   总计生成: {len(all_results)} 个SVG文件")
    print(f"   大号文件: {len([r for r in all_results if r['size'] == 'L'])} 个")
    print(f"   小号文件: {len([r for r in all_results if r['size'] == 'S'])} 个")
    print("=" * 60)


if __name__ == "__main__":
    main()

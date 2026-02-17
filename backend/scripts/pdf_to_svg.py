# -*- coding: utf-8 -*-
"""
PDF转SVG转换脚本
功能：将PDF矢量模板文件转换为单独的SVG文件，按工厂SKU编码规则命名
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

import fitz  # PyMuPDF


def pdf_to_svg(pdf_path: Path, output_dir: Path, sku_prefix: str = None) -> list:
    """
    将PDF文件转换为SVG格式
    
    Args:
        pdf_path: PDF文件路径
        output_dir: SVG输出目录
        sku_prefix: SKU前缀（用于命名，如不提供则使用页码）
        
    Returns:
        list: 生成的SVG文件路径列表
    """
    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 打开PDF文件
    doc = fitz.open(pdf_path)
    
    generated_files = []
    
    print(f"\n📄 PDF文件: {pdf_path.name}")
    print(f"   总页数: {len(doc)}")
    print(f"   输出目录: {output_dir}\n")
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # 获取页面的SVG内容
        svg_content = page.get_svg_image()
        
        # 确定输出文件名
        if sku_prefix:
            # 如果提供了SKU前缀，使用SKU命名
            output_filename = f"{sku_prefix}_page{page_num + 1}.svg"
        else:
            # 否则使用页码命名
            output_filename = f"page_{page_num + 1}.svg"
        
        output_path = output_dir / output_filename
        
        # 写入SVG文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        file_size = output_path.stat().st_size / 1024
        print(f"   ✅ 页面 {page_num + 1} -> {output_filename} ({file_size:.1f} KB)")
        generated_files.append(output_path)
    
    doc.close()
    
    return generated_files


def convert_pet_tag_template(pdf_path: Path, output_dir: Path) -> dict:
    """
    转换宠物牌模板PDF，按外观类型拆分并命名
    
    PDF文件说明：B不锈钢外观模版-正反面-大.pdf
    包含多种外观的正反面模板
    
    Args:
        pdf_path: PDF文件路径
        output_dir: SVG输出目录
        
    Returns:
        dict: 转换结果统计
    """
    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 打开PDF文件
    doc = fitz.open(pdf_path)
    
    print("=" * 60)
    print("宠物牌模板 PDF -> SVG 转换")
    print("=" * 60)
    print(f"\n📄 源文件: {pdf_path.name}")
    print(f"   总页数: {len(doc)}")
    print(f"   输出目录: {output_dir}")
    
    # 外观代码映射（根据PDF内容可能需要调整）
    # 假设PDF中按以下顺序排列外观：
    # 页面顺序可能是：圆形、骨形、心形等的正反面
    shape_codes = {
        "C": "圆形",
        "E": "骨形", 
        "G": "心形",
    }
    
    results = {
        "total_pages": len(doc),
        "generated_files": [],
        "errors": []
    }
    
    print("\n" + "-" * 60)
    print("开始转换...")
    print("-" * 60)
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        try:
            # 获取页面的SVG内容
            svg_content = page.get_svg_image()
            
            # 临时文件名（后续可根据实际内容重命名）
            output_filename = f"template_page_{page_num + 1}.svg"
            output_path = output_dir / output_filename
            
            # 写入SVG文件
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            
            file_size = output_path.stat().st_size / 1024
            print(f"   ✅ 页面 {page_num + 1:2d} -> {output_filename} ({file_size:.1f} KB)")
            results["generated_files"].append(str(output_path))
            
        except Exception as e:
            error_msg = f"页面 {page_num + 1} 转换失败: {e}"
            print(f"   ❌ {error_msg}")
            results["errors"].append(error_msg)
    
    doc.close()
    
    print("\n" + "=" * 60)
    print(f"转换完成！成功: {len(results['generated_files'])} 个, 失败: {len(results['errors'])} 个")
    print("=" * 60)
    
    return results


def main():
    """主函数"""
    # 配置路径
    pdf_path = Path(r"d:\ETSY_Order_Automation\backend\src\B不锈钢外观模版-正反面-大.pdf")
    output_dir = Path(r"d:\ETSY_Order_Automation\backend\assets\templates")
    
    # 检查PDF文件是否存在
    if not pdf_path.exists():
        print(f"❌ PDF文件不存在: {pdf_path}")
        return
    
    # 执行转换
    results = convert_pet_tag_template(pdf_path, output_dir)
    
    # 显示后续操作提示
    print("\n📋 后续操作建议:")
    print("-" * 60)
    print("1. 检查生成的SVG文件内容，确认各页面对应的外观类型")
    print("2. 根据外观类型重命名文件为标准SKU格式：")
    print("   - B-C01A.svg (圆形-大-银色)")
    print("   - B-E01A.svg (骨形-大-银色)")
    print("   - B-G01A.svg (心形-大-银色)")
    print("3. 如需其他颜色版本，复制并修改文件名后缀：")
    print("   - A=银色, B=金色, C=玫瑰金, D=黑色")
    print("-" * 60)


if __name__ == "__main__":
    main()

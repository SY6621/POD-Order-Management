"""生成可在浏览器预览效果图的 HTML 文件，内嵌字体 + SVG"""
import sys, io, base64
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')

from pathlib import Path
from src.services.database_service import db
from src.services.effect_template_service import (
    generate_effect_image_for_order,
    _build_config_from_order,
    generate_effect_image,
    _get_font_b64,
)

ETSY_ID = '3986891868'
order   = db.get_order_by_etsy_id(ETSY_ID)
config  = _build_config_from_order(order)

# 读取生成的 SVG 内容
svg_content = generate_effect_image(config)

# 字体 base64
f04_b64  = _get_font_b64("F-04.ttf")
back_b64 = _get_font_b64("back_standard.ttf")

# 生成 HTML：用 <style> 在 HTML 层声明字体，确保字体被浏览器加载
html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>效果图预览 — {ETSY_ID}</title>
<style>
  /* 在 HTML 层声明字体，确保嵌入 SVG 也能渲染 */
  @font-face {{
    font-family: 'F-04';
    src: url('data:font/truetype;base64,{f04_b64}') format('truetype');
    font-weight: normal;
    font-style: normal;
  }}
  @font-face {{
    font-family: 'back_standard';
    src: url('data:font/truetype;base64,{back_b64}') format('truetype');
    font-weight: normal;
    font-style: normal;
  }}
  body {{
    background: #f1f5f9;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px;
    font-family: Arial, sans-serif;
  }}
  .card {{
    background: #fff;
    border-radius: 16px;
    padding: 32px 40px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
    max-width: 700px;
    width: 100%;
  }}
  h2 {{ color: #334155; margin-bottom: 4px; font-size: 18px; }}
  .meta {{ color: #64748b; font-size: 13px; margin-bottom: 24px; }}
  .svg-wrap {{
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    display: flex;
    justify-content: center;
    padding: 16px;
  }}
  .caption {{
    margin-top: 12px;
    text-align: center;
    font-size: 12px;
    color: #64748b;
    line-height: 1.8;
  }}
  .caption strong {{ color: #334155; }}
  .tag {{
    display: inline-block;
    background: #f0fdf4;
    color: #16a34a;
    border: 1px solid #bbf7d0;
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 11px;
    font-weight: 600;
    margin-left: 6px;
  }}
</style>
</head>
<body>
<div class="card">
  <h2>效果图预览 <span class="tag">Order #{ETSY_ID}</span></h2>
  <div class="meta">
    客户：{order.get('customer_name', '')} &nbsp;|&nbsp;
    外观：{config.shape} &nbsp;|&nbsp;
    颜色：{config.color} &nbsp;|&nbsp;
    大小：{config.size}
  </div>

  <div class="svg-wrap">
    {svg_content}
  </div>

  <div class="caption">
    <strong>Front:</strong> {config.front.text} &nbsp;|&nbsp;
    <strong>Font:</strong> {config.front.font_family} &nbsp;|&nbsp;
    <strong>Phone:</strong> {config.back.phone_number}
    <br>
    <span style="color:#94a3b8;">Effect Image</span> &nbsp;|&nbsp;
    <strong>Size: 32×30 mm</strong>
  </div>
</div>
</body>
</html>"""

out = Path('output/preview_{}.html'.format(ETSY_ID))
out.write_text(html, encoding='utf-8')
print(f'✅ 预览 HTML 已生成: {out}')

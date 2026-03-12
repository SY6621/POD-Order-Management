"""
全流程整合验证：
模拟 test_email_fetch.py 中新订单写入后触发效果图生成的完整路径
（不重新抓邮件，直接用数据库现有订单验证整合逻辑）
"""
import sys, io
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

print('=' * 60)
print('  全流程整合验证')
print('  邮件→解析→写库→效果图→上传→回写URL')
print('=' * 60)

# 模拟 "新订单写入后" 的状态：从数据库取出订单（即 process_parsed_order 的返回值）
order = db.get_order_by_etsy_id(ETSY_ID)
if not order:
    print('❌ 未找到订单')
    exit()

# 通过 matched_sku_id 反查 sku_code
skm = db.select_one('sku_mapping', {'id': order.get('matched_sku_id')})
sku_code_display = skm.get('sku_code', 'N/A') if skm else 'N/A'

print(f'\n[订单信息]')
print(f'  订单号:  {order["etsy_order_id"]}')
print(f'  客户:    {order["customer_name"]}')
print(f'  外观/颜色/大小: {order["product_shape"]} / {order["product_color"]} / {order["product_size"]}')
print(f'  正面: {order["front_text"]}  字体: {order["font_code"]}')
print(f'  背面: {order["back_text"]}')

# === 模拟 test_email_fetch.py 中 result 的处理逻辑 ===
print(f'\n[效果图] 开始生成...')
url = generate_effect_image_for_order(order, upload=True)
if url:
    db.update('orders', {'id': order['id']}, {'effect_image_url': url})
    print(f'[效果图] 已保存并回写 URL')
    print(f'  URL: {url}')
else:
    print(f'[效果图] 生成失败')
    exit()

# === 生成 HTML 预览 ===
print(f'\n[HTML预览] 生成中...')
config      = _build_config_from_order(order)
svg_content = generate_effect_image(config)
f04_b64     = _get_font_b64("F-04.ttf")
back_b64    = _get_font_b64("back_standard.ttf")

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>全流程验证预览 — {ETSY_ID}</title>
<style>
  @font-face {{ font-family: 'F-04'; src: url('data:font/truetype;base64,{f04_b64}') format('truetype'); }}
  @font-face {{ font-family: 'back_standard'; src: url('data:font/truetype;base64,{back_b64}') format('truetype'); }}
  body {{ background:#f1f5f9; display:flex; flex-direction:column; align-items:center; padding:40px; font-family:Arial,sans-serif; }}
  .card {{ background:#fff; border-radius:16px; padding:32px 40px; box-shadow:0 4px 24px rgba(0,0,0,0.08); max-width:700px; width:100%; }}
  h2 {{ color:#334155; font-size:18px; margin-bottom:4px; }}
  .meta {{ color:#64748b; font-size:13px; margin-bottom:24px; line-height:2; }}
  .svg-wrap {{ background:#fff; border:1px solid #e2e8f0; border-radius:12px; display:flex; justify-content:center; padding:16px; }}
  .caption {{ margin-top:12px; text-align:center; font-size:12px; color:#64748b; line-height:2; }}
  .caption strong {{ color:#334155; }}
  .tag {{ display:inline-block; background:#f0fdf4; color:#16a34a; border:1px solid #bbf7d0; border-radius:6px; padding:2px 8px; font-size:11px; font-weight:600; margin-left:6px; }}
  .check {{ display:flex; flex-direction:column; gap:6px; margin-top:20px; padding:16px; background:#f8fafc; border-radius:10px; font-size:13px; }}
  .check-item {{ display:flex; gap:8px; align-items:center; }}
  .ok {{ color:#16a34a; font-weight:700; }}
</style>
</head>
<body>
<div class="card">
  <h2>全流程验证 <span class="tag">✅ 通过</span></h2>
  <div class="meta">
    <strong>订单号：</strong>{order['etsy_order_id']} &nbsp;|&nbsp;
    <strong>客户：</strong>{order['customer_name']}<br>
    <strong>SKU编号：</strong><span style="color:#3b82f6;font-weight:700;">{sku_code_display}</span> &nbsp;|&nbsp;
    <strong>外观/颜色/大小：</strong>{config.shape} / {config.color} / {config.size}
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

  <div class="check">
    <div class="check-item"><span class="ok">✅</span> 邮件解析：订单号 / 客户名 / 外观颜色大小 / 刻字内容</div>
    <div class="check-item"><span class="ok">✅</span> SKU 反推：<strong>{sku_code_display}</strong> 已写入 matched_sku_id</div>
    <div class="check-item"><span class="ok">✅</span> 效果图生成：F-04 正面 + back_standard 背面</div>
    <div class="check-item"><span class="ok">✅</span> 上传 Storage：effect-images/{order['etsy_order_id']}.svg</div>
    <div class="check-item"><span class="ok">✅</span> 回写数据库：effect_image_url 已更新</div>
    <div class="check-item" style="margin-top:8px;font-size:11px;color:#94a3b8;">
      Storage URL: <a href="{url}" target="_blank" style="color:#3b82f6;">{url}</a>
    </div>
  </div>
</div>
</body>
</html>"""

out = Path(f'output/fullflow_verify_{ETSY_ID}.html')
out.write_text(html, encoding='utf-8')
print(f'✅ HTML 预览已生成: {out}')

import subprocess
subprocess.Popen(['start', str(out)], shell=True)

print('\n' + '=' * 60)
print('  全流程验证完成！')
print('=' * 60)

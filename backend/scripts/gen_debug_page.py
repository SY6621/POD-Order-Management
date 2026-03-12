# -*- coding: utf-8 -*-
"""
生成效果图调试网页
- 内嵌 F-04 和 back_standard 字体
- 实时调整：字号、Y位置、行间距
- 支持心形/圆形/骨头形 + 4种颜色
- 调整完成后截图/记录参数给 AI 写入代码
"""
import base64
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

FONTS_DIR  = Path(__file__).parent.parent / "assets" / "fonts"
OUTPUT_DIR = Path(__file__).parent.parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

def load_b64(filename):
    p = FONTS_DIR / filename
    if p.exists():
        return base64.b64encode(p.read_bytes()).decode("ascii")
    return ""

print("正在加载字体文件（请稍候）...")
f04_b64  = load_b64("F-04.ttf")
back_b64 = load_b64("back_standard.ttf")
print(f"F-04: {len(f04_b64)//1024} KB (base64)")
print(f"back_standard: {len(back_b64)//1024} KB (base64)")

# SVG path 数据
HEART_L_PATH = "M69.8686 14.0786C68.5094 14.8158 64.5094 17.3092 62.1553 18.8983 47.5075 28.7844 36.1069 40.7415 30.2145 52.3956 25.9707 60.7907 24.5971 68.7719 26.1031 76.3129 26.9495 80.555 28.7402 84.437 31.4827 87.963 32.3107 89.0291 34.2221 91.0242 35.3058 91.9573 38.7692 94.9346 42.7311 96.8275 46.8524 97.4693 48.0892 97.6603 50.9553 97.6586 52.6629 97.4662 55.98 97.0889 58.8903 96.243 61.4594 94.8977 64.0329 97.8106 67.2554 99.5443 70.7536 99.5443 74.2912 99.5443 77.5477 97.772 80.1351 94.7988 82.5721 96.0979 85.3194 96.9633 88.3412 97.3706 89.6519 97.5475 90.8787 97.6374 92.0486 97.6385 94.134 97.6408 96.0392 97.3613 97.9174 96.7924 103.7109 95.0369 109.3989 90.2472 112.7044 84.3412 114.5509 81.0442 115.5943 77.7268 116.1085 73.5415 116.2627 72.21 116.2627 68.1591 116.0768 66.6978 115.638 63.1244 114.8357 60.035 113.4584 56.552 107.6851 41.9811 92.8831 26.5946 73.489 14.9995L71.905 14.0522C71.4226 13.752 70.4282 13.7837 69.8686 14.0786ZM71.0152 95.0488C73.5985 95.0488 75.6924 92.9548 75.6924 90.3716 75.6924 87.7884 73.5985 85.6945 71.0152 85.6945 68.432 85.6945 66.3381 87.7884 66.3381 90.3716 66.3381 92.9548 68.432 95.0488 71.0152 95.0488"
CIRCLE_L_PATH = "M70.8656 86.5749C68.2826 86.5749 66.1887 88.6689 66.1887 91.2521 66.1887 93.835 68.2826 95.9298 70.8656 95.9298 73.4488 95.9298 75.5427 93.835 75.5427 91.2521 75.5427 88.6689 73.4488 86.5749 70.8656 86.5749ZM70.8656 102.331C45.6608 102.331 25.2286 81.898 25.2286 56.6923 25.2286 31.4872 45.6608 11.0551 70.8656 11.0551 96.0707 11.0551 116.5037 31.4872 116.5037 56.6923 116.5037 81.898 96.0707 102.331 70.8656 102.331"
BONE_L_PATH   = "M13.6145 55.2305C14.5142 56.0177 14.5142 57.3676 13.6145 58.155 9.4527 61.9792 6.9783 67.3781 7.0906 73.2271 7.3157 84.1377 16.539 93.0234 28.0117 93.361 37.2351 93.5858 44.3214 89.3117 47.1334 83.4627 47.4707 82.5627 48.3707 82.0006 49.3829 82.0006H56.2442C57.369 82.0006 58.4935 82.6753 59.0562 83.6878 61.8681 88.6368 66.0297 91.7861 70.8664 91.7861 75.5904 91.7861 79.8647 88.6368 82.6767 83.6878 83.2391 82.6753 84.2513 82.0006 85.4887 82.0006H92.3499C93.3622 82.0006 94.2622 82.5627 94.5995 83.4627 97.524 89.3117 104.4978 93.5858 113.7209 93.361 125.0813 93.136 134.4172 84.1377 134.642 73.2271 134.7545 67.2656 132.1676 61.8667 128.1183 58.155 127.2183 57.3676 127.2183 56.0177 128.1183 55.2305 132.2799 51.406 134.7545 46.1197 134.642 40.1581 134.4172 29.2476 125.0813 20.3618 113.7209 20.0245 107.7596 19.7994 96.5117 24.5237 93.5872 31.2724 93.2496 32.1721 92.3499 32.7345 91.3377 32.7345H71.7661 67.4921 50.5077C49.4955 32.7345 48.5955 32.1721 48.2581 31.2724 45.3336 24.4111 34.0858 19.7994 28.1242 20.0245 16.7638 20.3618 7.4282 29.2476 7.2031 40.1581 6.9783 46.1197 9.5652 51.406 13.6145 55.2305ZM70.8664 87.5075C73.6784 87.5075 75.8154 84.9203 75.253 81.9958 74.9157 80.3086 73.6784 78.9591 71.9912 78.6214 68.9542 77.8343 66.2547 80.0838 66.2547 83.0083 66.3673 85.4827 68.3918 87.5075 70.8664 87.5075"

COLOR_MAP = {
    "RoseGold": "#dabf9b",
    "Gold":     "#ebcd7b",
    "Silver":   "#9f9fa0",
    "Black":    "#231916",
}

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>效果图调试工具</title>
<style>
  @font-face {{
    font-family: 'F-04';
    src: url('data:font/truetype;base64,{f04_b64}') format('truetype');
  }}
  @font-face {{
    font-family: 'back_standard';
    src: url('data:font/truetype;base64,{back_b64}') format('truetype');
  }}
  * {{ box-sizing: border-box; }}
  body {{ background: #f0f0f0; font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
  h2 {{ color: #333; margin-bottom: 16px; }}
  .layout {{ display: flex; gap: 24px; align-items: flex-start; }}
  .preview-area {{
    background: repeating-conic-gradient(#ccc 0% 25%, #fff 0% 50%) 0 0 / 20px 20px;
    border: 1px solid #aaa; padding: 20px; min-width: 500px; min-height: 200px;
    display: flex; align-items: center; justify-content: center;
  }}
  .controls {{ background: #fff; border: 1px solid #ddd; padding: 20px; border-radius: 8px; min-width: 320px; }}
  .ctrl-group {{ margin-bottom: 14px; }}
  .ctrl-group label {{ display: block; font-size: 12px; color: #666; margin-bottom: 4px; font-weight: bold; }}
  .ctrl-group input[type=range] {{ width: 100%; }}
  .ctrl-group .val {{ font-size: 13px; color: #e44; font-weight: bold; display: inline-block; min-width: 40px; }}
  select, input[type=text] {{ width: 100%; padding: 5px; margin-top: 4px; border: 1px solid #ccc; border-radius: 4px; }}
  .section-title {{ font-size: 13px; font-weight: bold; color: #333; margin: 16px 0 8px; border-bottom: 1px solid #eee; padding-bottom: 4px; }}
  .params-output {{ background: #f8f8f8; border: 1px solid #ddd; padding: 12px; border-radius: 6px; margin-top: 16px; font-size: 12px; white-space: pre-wrap; font-family: monospace; }}
  button {{ background: #4a90d9; color: #fff; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; margin-top: 8px; }}
  button:hover {{ background: #357abd; }}
</style>
</head>
<body>
<h2>🎨 效果图调试工具 — 调整满意后截图发给 AI</h2>
<div class="layout">

  <!-- 预览区 -->
  <div>
    <div class="preview-area">
      <svg id="main-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 133" width="640" height="266">
        <defs>
          <style id="embedded-fonts">
            @font-face {{ font-family: 'F-04'; src: url('data:font/truetype;base64,{f04_b64}') format('truetype'); }}
            @font-face {{ font-family: 'back_standard'; src: url('data:font/truetype;base64,{back_b64}') format('truetype'); }}
          </style>
        </defs>
        <!-- 外框 -->
        <rect x="0.5" y="0.5" width="319" height="132" fill="none" stroke="#ccc" stroke-width="0.5"/>
        <!-- 正面形状 -->
        <path id="front-shape" transform="matrix(1,0,0,-1,0,113.3858)" fill="#dabf9b" fill-rule="evenodd"
              d="{HEART_L_PATH}" transform-origin="70.87 56.69"/>
        <g transform="translate(10,10)">
          <path id="front-path" transform="matrix(1,0,0,-1,0,113.3858)" fill="#dabf9b" fill-rule="evenodd"
                d="{HEART_L_PATH}"/>
          <text id="front-text" x="70.87" y="54" dominant-baseline="middle" text-anchor="middle"
                font-family="F-04, sans-serif" font-size="23" fill="#333333">Alice</text>
        </g>
        <!-- 正面标签 -->
        <text x="81.87" y="130" font-family="Arial,sans-serif" font-size="7" fill="#999" text-anchor="middle">正面</text>
        <!-- 背面形状 -->
        <g transform="translate(169.73,10)">
          <path id="back-path" transform="matrix(1,0,0,-1,0,113.3858)" fill="#dabf9b" fill-rule="evenodd"
                d="{HEART_L_PATH}"/>
          <text id="back-text1" x="70.87" y="46" dominant-baseline="middle" text-anchor="middle"
                font-family="back_standard, Arial, sans-serif" font-size="14" fill="#333333">If Lost</text>
          <text id="back-text2" x="70.87" y="62" dominant-baseline="middle" text-anchor="middle"
                font-family="back_standard, Arial, sans-serif" font-size="14" fill="#333333">13999926688</text>
        </g>
        <!-- 背面标签 -->
        <text x="240.6" y="130" font-family="Arial,sans-serif" font-size="7" fill="#999" text-anchor="middle">背面</text>
      </svg>
    </div>
    <div class="params-output" id="params-out">当前参数（调整后自动更新）：
正面字号: 23px  |  Y: 54
背面字号: 14px  |  文字Y: 46  |  电话Y: 62
颜色: RoseGold #dabf9b</div>
  </div>

  <!-- 控制面板 -->
  <div class="controls">
    <div class="section-title">形状 & 颜色</div>
    <div class="ctrl-group">
      <label>形状</label>
      <select id="shape" onchange="updateShape()">
        <option value="heart">心形</option>
        <option value="circle">圆形</option>
        <option value="bone">骨头形</option>
      </select>
    </div>
    <div class="ctrl-group">
      <label>颜色</label>
      <select id="color" onchange="updateColor()">
        <option value="RoseGold">玫瑰金 RoseGold</option>
        <option value="Gold">金色 Gold</option>
        <option value="Silver">银色 Silver</option>
        <option value="Black">黑色 Black</option>
      </select>
    </div>

    <div class="section-title">正面文字</div>
    <div class="ctrl-group">
      <label>正面内容</label>
      <input type="text" id="front-content" value="Alice" oninput="updateFrontText()">
    </div>
    <div class="ctrl-group">
      <label>正面字号 <span class="val" id="fs-val">23</span> px</label>
      <input type="range" id="front-size" min="6" max="40" value="23" step="0.5" oninput="updateFrontSize()">
    </div>
    <div class="ctrl-group">
      <label>正面 Y 位置 <span class="val" id="fy-val">54</span> px</label>
      <input type="range" id="front-y" min="20" max="90" value="54" step="0.5" oninput="updateFrontY()">
    </div>

    <div class="section-title">背面文字</div>
    <div class="ctrl-group">
      <label>背面文字内容</label>
      <input type="text" id="back-content1" value="If Lost" oninput="updateBackText()">
    </div>
    <div class="ctrl-group">
      <label>背面电话号码</label>
      <input type="text" id="back-content2" value="13999926688" oninput="updateBackText()">
    </div>
    <div class="ctrl-group">
      <label>背面字号 <span class="val" id="bs-val">14</span> px</label>
      <input type="range" id="back-size" min="5" max="30" value="14" step="0.5" oninput="updateBackSize()">
    </div>
    <div class="ctrl-group">
      <label>背面文字 Y <span class="val" id="by1-val">46</span> px</label>
      <input type="range" id="back-y1" min="20" max="90" value="46" step="0.5" oninput="updateBackY()">
    </div>
    <div class="ctrl-group">
      <label>背面电话 Y <span class="val" id="by2-val">62</span> px</label>
      <input type="range" id="back-y2" min="20" max="90" value="62" step="0.5" oninput="updateBackY()">
    </div>

    <button onclick="copyParams()">📋 复制当前参数</button>
    <div style="font-size:11px;color:#888;margin-top:8px;">调整到满意后，截图发给 AI 确认参数</div>
  </div>
</div>

<script>
const PATHS = {{
  heart:  "{HEART_L_PATH}",
  circle: "{CIRCLE_L_PATH}",
  bone:   "{BONE_L_PATH}"
}};
const COLORS = {{
  RoseGold: "#dabf9b", Gold: "#ebcd7b", Silver: "#9f9fa0", Black: "#231916"
}};
const TEXT_COLORS = {{
  RoseGold: "#333333", Gold: "#333333", Silver: "#333333", Black: "#cccccc"
}};

function updateShape() {{
  const s = document.getElementById("shape").value;
  const d = PATHS[s];
  document.getElementById("front-path").setAttribute("d", d);
  document.getElementById("back-path").setAttribute("d", d);
  updateParams();
}}

function updateColor() {{
  const c = document.getElementById("color").value;
  const fill = COLORS[c];
  const textFill = TEXT_COLORS[c];
  document.getElementById("front-path").setAttribute("fill", fill);
  document.getElementById("back-path").setAttribute("fill", fill);
  document.getElementById("front-text").setAttribute("fill", textFill);
  document.getElementById("back-text1").setAttribute("fill", textFill);
  document.getElementById("back-text2").setAttribute("fill", textFill);
  updateParams();
}}

function updateFrontText() {{
  document.getElementById("front-text").textContent = document.getElementById("front-content").value;
  updateParams();
}}

function updateFrontSize() {{
  const v = document.getElementById("front-size").value;
  document.getElementById("fs-val").textContent = v;
  document.getElementById("front-text").setAttribute("font-size", v);
  updateParams();
}}

function updateFrontY() {{
  const v = document.getElementById("front-y").value;
  document.getElementById("fy-val").textContent = v;
  document.getElementById("front-text").setAttribute("y", v);
  updateParams();
}}

function updateBackText() {{
  document.getElementById("back-text1").textContent = document.getElementById("back-content1").value;
  document.getElementById("back-text2").textContent = document.getElementById("back-content2").value;
  updateParams();
}}

function updateBackSize() {{
  const v = document.getElementById("back-size").value;
  document.getElementById("bs-val").textContent = v;
  document.getElementById("back-text1").setAttribute("font-size", v);
  document.getElementById("back-text2").setAttribute("font-size", v);
  updateParams();
}}

function updateBackY() {{
  const v1 = document.getElementById("back-y1").value;
  const v2 = document.getElementById("back-y2").value;
  document.getElementById("by1-val").textContent = v1;
  document.getElementById("by2-val").textContent = v2;
  document.getElementById("back-text1").setAttribute("y", v1);
  document.getElementById("back-text2").setAttribute("y", v2);
  updateParams();
}}

function updateParams() {{
  const fs  = document.getElementById("front-size").value;
  const fy  = document.getElementById("front-y").value;
  const bs  = document.getElementById("back-size").value;
  const by1 = document.getElementById("back-y1").value;
  const by2 = document.getElementById("back-y2").value;
  const color = document.getElementById("color").value;
  const shape = document.getElementById("shape").value;
  document.getElementById("params-out").textContent =
    `当前参数（发给 AI 写入代码）：\\n形状: ${{shape}} | 颜色: ${{color}}\\n正面字号: ${{fs}}px  |  Y: ${{fy}}\\n背面字号: ${{bs}}px  |  文字Y: ${{by1}}  |  电话Y: ${{by2}}`;
}}

function copyParams() {{
  const txt = document.getElementById("params-out").textContent;
  navigator.clipboard.writeText(txt).then(() => alert("参数已复制！"));
}}
</script>
</body>
</html>"""

out_path = OUTPUT_DIR / "effect_debug.html"
out_path.write_text(html, encoding="utf-8")
print(f"\n✅ 调试页面已生成：{out_path}")
print("请用浏览器打开此文件进行调整")

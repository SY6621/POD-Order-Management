# -*- coding: utf-8 -*-
"""
生成升级版效果图调试器（V2），并注入到 02_待确认订单.html
升级内容：
1. 背面文字/电话字号独立调整
2. 直接嵌入待确认订单HTML的效果图占位区
"""
import base64
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

FONTS_DIR   = Path(__file__).parent.parent / "assets" / "fonts"
OUTPUT_DIR  = Path(__file__).parent.parent / "output"
HTML_PATH   = Path(__file__).parent.parent / "tests" / "02_待确认订单.html"
OUTPUT_DIR.mkdir(exist_ok=True)

print("正在加载字体文件...")
f04_b64  = base64.b64encode((FONTS_DIR / "F-04.ttf").read_bytes()).decode("ascii")
back_b64 = base64.b64encode((FONTS_DIR / "back_standard.ttf").read_bytes()).decode("ascii")
print(f"  F-04: {len(f04_b64)//1024} KB | back_standard: {len(back_b64)//1024} KB")

HEART_L  = "M69.8686 14.0786C68.5094 14.8158 64.5094 17.3092 62.1553 18.8983 47.5075 28.7844 36.1069 40.7415 30.2145 52.3956 25.9707 60.7907 24.5971 68.7719 26.1031 76.3129 26.9495 80.555 28.7402 84.437 31.4827 87.963 32.3107 89.0291 34.2221 91.0242 35.3058 91.9573 38.7692 94.9346 42.7311 96.8275 46.8524 97.4693 48.0892 97.6603 50.9553 97.6586 52.6629 97.4662 55.98 97.0889 58.8903 96.243 61.4594 94.8977 64.0329 97.8106 67.2554 99.5443 70.7536 99.5443 74.2912 99.5443 77.5477 97.772 80.1351 94.7988 82.5721 96.0979 85.3194 96.9633 88.3412 97.3706 89.6519 97.5475 90.8787 97.6374 92.0486 97.6385 94.134 97.6408 96.0392 97.3613 97.9174 96.7924 103.7109 95.0369 109.3989 90.2472 112.7044 84.3412 114.5509 81.0442 115.5943 77.7268 116.1085 73.5415 116.2627 72.21 116.2627 68.1591 116.0768 66.6978 115.638 63.1244 114.8357 60.035 113.4584 56.552 107.6851 41.9811 92.8831 26.5946 73.489 14.9995L71.905 14.0522C71.4226 13.752 70.4282 13.7837 69.8686 14.0786ZM71.0152 95.0488C73.5985 95.0488 75.6924 92.9548 75.6924 90.3716 75.6924 87.7884 73.5985 85.6945 71.0152 85.6945 68.432 85.6945 66.3381 87.7884 66.3381 90.3716 66.3381 92.9548 68.432 95.0488 71.0152 95.0488"
CIRCLE_L = "M70.8656 86.5749C68.2826 86.5749 66.1887 88.6689 66.1887 91.2521 66.1887 93.835 68.2826 95.9298 70.8656 95.9298 73.4488 95.9298 75.5427 93.835 75.5427 91.2521 75.5427 88.6689 73.4488 86.5749 70.8656 86.5749ZM70.8656 102.331C45.6608 102.331 25.2286 81.898 25.2286 56.6923 25.2286 31.4872 45.6608 11.0551 70.8656 11.0551 96.0707 11.0551 116.5037 31.4872 116.5037 56.6923 116.5037 81.898 96.0707 102.331 70.8656 102.331"
BONE_L   = "M13.6145 55.2305C14.5142 56.0177 14.5142 57.3676 13.6145 58.155 9.4527 61.9792 6.9783 67.3781 7.0906 73.2271 7.3157 84.1377 16.539 93.0234 28.0117 93.361 37.2351 93.5858 44.3214 89.3117 47.1334 83.4627 47.4707 82.5627 48.3707 82.0006 49.3829 82.0006H56.2442C57.369 82.0006 58.4935 82.6753 59.0562 83.6878 61.8681 88.6368 66.0297 91.7861 70.8664 91.7861 75.5904 91.7861 79.8647 88.6368 82.6767 83.6878 83.2391 82.6753 84.2513 82.0006 85.4887 82.0006H92.3499C93.3622 82.0006 94.2622 82.5627 94.5995 83.4627 97.524 89.3117 104.4978 93.5858 113.7209 93.361 125.0813 93.136 134.4172 84.1377 134.642 73.2271 134.7545 67.2656 132.1676 61.8667 128.1183 58.155 127.2183 57.3676 127.2183 56.0177 128.1183 55.2305 132.2799 51.406 134.7545 46.1197 134.642 40.1581 134.4172 29.2476 125.0813 20.3618 113.7209 20.0245 107.7596 19.7994 96.5117 24.5237 93.5872 31.2724 93.2496 32.1721 92.3499 32.7345 91.3377 32.7345H71.7661 67.4921 50.5077C49.4955 32.7345 48.5955 32.1721 48.2581 31.2724 45.3336 24.4111 34.0858 19.7994 28.1242 20.0245 16.7638 20.3618 7.4282 29.2476 7.2031 40.1581 6.9783 46.1197 9.5652 51.406 13.6145 55.2305ZM70.8664 87.5075C73.6784 87.5075 75.8154 84.9203 75.253 81.9958 74.9157 80.3086 73.6784 78.9591 71.9912 78.6214 68.9542 77.8343 66.2547 80.0838 66.2547 83.0083 66.3673 85.4827 68.3918 87.5075 70.8664 87.5075"

# =====================================================
# 生成设计器 HTML 片段（用于嵌入待确认订单页）
# =====================================================
DESIGNER_BLOCK = f"""
<!-- ========== 效果图设计器 START ========== -->
<style>
  @font-face {{
    font-family: 'F-04';
    src: url('data:font/truetype;base64,{f04_b64}') format('truetype');
  }}
  @font-face {{
    font-family: 'back_standard';
    src: url('data:font/truetype;base64,{back_b64}') format('truetype');
  }}
  .designer-wrap {{ display: flex; flex-direction: column; gap: 12px; padding: 4px; }}
  .svg-preview {{
    background: #ffffff;
    border: 1px solid #e2e8f0; border-radius: 12px;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    padding: 12px; min-height: 160px; position: relative;
  }}
  .ctrl-row {{ display: flex; align-items: center; gap: 8px; font-size: 12px; color: #475569; }}
  .ctrl-row label {{ min-width: 80px; font-weight: 600; }}
  .ctrl-row input[type=range] {{ flex: 1; accent-color: #3b82f6; }}
  .ctrl-row .vnum {{ min-width: 36px; color: #e44; font-weight: 700; font-size: 12px; }}
  .ctrl-row input[type=text] {{ flex: 1; border: 1px solid #cbd5e1; border-radius: 6px; padding: 3px 8px; font-size: 12px; }}
  .ctrl-row select {{ border: 1px solid #cbd5e1; border-radius: 6px; padding: 3px 6px; font-size: 12px; }}
  .section-label {{ font-size: 11px; font-weight: 700; color: #94a3b8; letter-spacing: 0.5px; text-transform: uppercase; padding: 4px 0 2px; border-bottom: 1px solid #f1f5f9; }}
  .action-btns {{ display: flex; gap: 8px; }}
  .btn-primary {{ background: #3b82f6; color: #fff; border: none; padding: 7px 16px; border-radius: 8px; font-size: 12px; font-weight: 600; cursor: pointer; }}
  .btn-primary:hover {{ background: #2563eb; }}
  .btn-ghost {{ background: #f1f5f9; color: #475569; border: none; padding: 7px 14px; border-radius: 8px; font-size: 12px; cursor: pointer; }}
  .btn-ghost:hover {{ background: #e2e8f0; }}
  .params-chip {{ font-size: 10px; color: #64748b; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 4px 8px; margin-top: 4px; white-space: pre-wrap; font-family: monospace; }}
</style>

<div class="designer-wrap" id="ed-designer">
  <!-- SVG 预览 -->
  <div class="svg-preview">
    <svg id="ed-svg" xmlns="http://www.w3.org/2000/svg"
         viewBox="0 0 321 134" width="580" height="193">
      <defs>
        <style>
          @font-face {{ font-family: 'F-04'; src: url('data:font/truetype;base64,{f04_b64}') format('truetype'); }}
          @font-face {{ font-family: 'back_standard'; src: url('data:font/truetype;base64,{back_b64}') format('truetype'); }}
        </style>
      </defs>
      <!-- 外框 -->
      <rect x="0.5" y="0.5" width="320" height="133" fill="none" stroke="#e2e8f0" stroke-width="0.8"/>
      <!-- 正面 -->
      <g id="ed-front-g" transform="translate(10,10)">
        <path id="ed-fp" transform="matrix(1,0,0,-1,0,113.3858)"
              fill="#dabf9b" fill-rule="evenodd"
              d="{HEART_L}"/>
        <text id="ed-ft" x="70.87" y="54" dominant-baseline="middle"
              text-anchor="middle" font-family="'F-04',sans-serif"
              font-size="24" fill="#333">Alice</text>
      </g>
      <!-- 背面 -->
      <g id="ed-back-g" transform="translate(169.73,10)">
        <path id="ed-bp" transform="matrix(1,0,0,-1,0,113.3858)"
              fill="#dabf9b" fill-rule="evenodd"
              d="{HEART_L}"/>
        <!-- 背面文字（支持自动换行，由JS动态渲染tspan） -->
        <text id="ed-bt1" x="70.87" dominant-baseline="middle"
              text-anchor="middle" font-family="'back_standard',sans-serif"
              font-size="11" fill="#333"></text>
        <!-- 背面电话（不换行） -->
        <text id="ed-bt2" x="70.87" y="54" dominant-baseline="middle"
              text-anchor="middle" font-family="'back_standard',sans-serif"
              font-size="11" fill="#333">13999926688</text>
      </g>
      <!-- 标签 -->
      <text x="81.8" y="129" font-family="Arial" font-size="7" fill="#94a3b8" text-anchor="middle">Front</text>
      <text x="241"  y="129" font-family="Arial" font-size="7" fill="#94a3b8" text-anchor="middle">Back</text>
    </svg>
    <!-- 订制内容字段行 -->
    <div id="ed-caption" style="width:580px;display:flex;flex-direction:column;align-items:center;gap:2px;padding:8px 4px 0;">
      <div style="font-size:11px;color:#64748b;">
        <span style="color:#94a3b8;">Front:</span> <span id="cap-front" style="color:#334155;font-weight:600;">Alice</span>
        &nbsp;<span style="color:#cbd5e1;">|</span>&nbsp;
        <span style="color:#94a3b8;">Font:</span> <span style="color:#334155;">F-04</span>
        &nbsp;<span style="color:#cbd5e1;">|</span>&nbsp;
        <span style="color:#94a3b8;">Back:</span> <span id="cap-back" style="color:#334155;font-weight:600;">If Lost</span>
        &nbsp;<span style="color:#cbd5e1;">|</span>&nbsp;
        <span style="color:#94a3b8;">Phone:</span> <span id="cap-phone" style="color:#334155;font-weight:600;">13999926688</span>
      </div>
      <div style="font-size:11px;">
        <span style="color:#94a3b8;">Effect Image</span>
        &nbsp;<span style="color:#cbd5e1;">|</span>&nbsp;
        <span style="color:#334155;font-weight:700;">Size: 38&times;30 mm</span>
      </div>
    </div>
  </div>

  <!-- 控制面板 -->
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
    <!-- 左列：正面 -->
    <div style="display:flex;flex-direction:column;gap:6px;">
      <div class="section-label">正面</div>
      <div class="ctrl-row">
        <label>形状</label>
        <select id="ed-shape" onchange="edUpdate()">
          <option value="heart">心形</option>
          <option value="circle">圆形</option>
          <option value="bone">骨头形</option>
        </select>
      </div>
      <div class="ctrl-row">
        <label>颜色</label>
        <select id="ed-color" onchange="edUpdate()">
          <option value="RoseGold">玫瑰金</option>
          <option value="Gold">金色</option>
          <option value="Silver">银色</option>
          <option value="Black">黑色</option>
        </select>
      </div>
      <div class="ctrl-row">
        <label>正面文字</label>
        <input type="text" id="ed-fc" value="Alice" oninput="edUpdate()">
      </div>
      <div class="ctrl-row">
        <label>正面字号</label>
        <input type="range" id="ed-fs" min="6" max="40" value="24" step="0.5" oninput="edUpdate()">
        <span class="vnum" id="ed-fs-v">24</span>px
      </div>
      <div class="ctrl-row">
        <label>正面 Y</label>
        <input type="range" id="ed-fy" min="20" max="90" value="54" step="0.5" oninput="edUpdate()">
        <span class="vnum" id="ed-fy-v">54</span>
      </div>
    </div>

    <!-- 右列：背面 -->
    <div style="display:flex;flex-direction:column;gap:6px;">
      <div class="section-label">背面</div>
      <div class="ctrl-row">
        <label>背面文字</label>
        <input type="text" id="ed-bc1" value="If Lost" oninput="edUpdate()">
      </div>
      <div class="ctrl-row">
        <label>文字字号</label>
        <input type="range" id="ed-bs1" min="5" max="28" value="11" step="0.5" oninput="edUpdate()">
        <span class="vnum" id="ed-bs1-v">11</span>px
      </div>
      <div class="ctrl-row">
        <label>文字 Y</label>
        <input type="range" id="ed-by1" min="20" max="90" value="40.5" step="0.5" oninput="edUpdate()">
        <span class="vnum" id="ed-by1-v">40.5</span>
      </div>
      <div class="ctrl-row">
        <label>电话号码</label>
        <input type="text" id="ed-bc2" value="13999926688" oninput="edUpdate()">
      </div>
      <div class="ctrl-row">
        <label>电话字号</label>
        <input type="range" id="ed-bs2" min="5" max="28" value="11" step="0.5" oninput="edUpdate()">
        <span class="vnum" id="ed-bs2-v">11</span>px
      </div>
      <div class="ctrl-row">
        <label>电话 Y</label>
        <input type="range" id="ed-by2" min="20" max="90" value="54" step="0.5" oninput="edUpdate()">
        <span class="vnum" id="ed-by2-v">54</span>
      </div>
    </div>
  </div>

  <!-- 操作按钮 -->
  <div class="action-btns">
    <button class="btn-primary" onclick="edSendConfirm()">✅ 确认效果图</button>
    <button class="btn-ghost"   onclick="edCopyParams()">📋 复制参数</button>
    <button class="btn-ghost"   onclick="edDownload()">⬇ 下载 SVG</button>
  </div>
  <div class="params-chip" id="ed-params">当前参数：形状: heart | 颜色: RoseGold | 正面字号: 24px | Y: 54 | 背面文字字号: 11px | 文字Y: 40.5 | 电话字号: 11px | 电话Y: 54</div>
</div>

<script>
(function(){{
  const PATHS = {{
    heart:  "{HEART_L}",
    circle: "{CIRCLE_L}",
    bone:   "{BONE_L}"
  }};
  const COLORS = {{
    RoseGold:"#dabf9b", Gold:"#ebcd7b", Silver:"#9f9fa0", Black:"#231916"
  }};
  const TEXT_COLORS = {{
    RoseGold:"#333333", Gold:"#333333", Silver:"#333333", Black:"#cccccc"
  }};
  const VW = {{ heart:141.7323, circle:141.7323, bone:141.7323 }};

  // 最大文字宽度（L号 84px，SVG 坐标空间）
  const MAX_TEXT_W = 84.0;
  const TEXT_CX    = 70.87;

  /**
   * 自动换行核心函数
   * 将 textEl 的内容按 maxWidth 切分为多行 <tspan>，
   * 起始Y = startY，行间距 = fontSize * lineH。
   * 返回实际占用的总高度（便于外部对齐）。
   */
  function wrapSVGText(textEl, rawText, fontSize, startY, maxWidth, lineH) {{
    // 清空旧 tspan
    while (textEl.firstChild) textEl.removeChild(textEl.firstChild);
    textEl.setAttribute('font-size', fontSize);

    const svg    = document.getElementById('ed-svg');
    const ns     = 'http://www.w3.org/2000/svg';
    // 建一个临时测量用 tspan
    const probe  = document.createElementNS(ns, 'tspan');
    probe.setAttribute('visibility', 'hidden');
    textEl.appendChild(probe);

    const words = rawText.split(/\s+/).filter(w => w.length > 0);
    let lines = [];
    let cur   = '';
    for (const w of words) {{
      const test = cur ? cur + ' ' + w : w;
      probe.textContent = test;
      if (probe.getComputedTextLength() > maxWidth && cur) {{
        lines.push(cur);
        cur = w;
      }} else {{
        cur = test;
      }}
    }}
    if (cur) lines.push(cur);

    textEl.removeChild(probe);

    const lineSpacing = fontSize * lineH;
    // 多行时整体向上偏移，使视觉重心保持在 startY
    const totalH   = (lines.length - 1) * lineSpacing;
    const firstY   = startY - totalH / 2;

    lines.forEach((line, i) => {{
      const tspan = document.createElementNS(ns, 'tspan');
      tspan.setAttribute('x', TEXT_CX);
      tspan.setAttribute('y', parseFloat((firstY + i * lineSpacing).toFixed(2)));
      tspan.setAttribute('dominant-baseline', 'middle');
      tspan.textContent = line;
      textEl.appendChild(tspan);
    }});

    return totalH;
  }}

  window.edUpdate = function() {{
    const shape  = document.getElementById('ed-shape').value;
    const color  = document.getElementById('ed-color').value;
    const fill   = COLORS[color];
    const tFill  = TEXT_COLORS[color];
    const d      = PATHS[shape];

    document.getElementById('ed-fp').setAttribute('d', d);
    document.getElementById('ed-bp').setAttribute('d', d);
    document.getElementById('ed-fp').setAttribute('fill', fill);
    document.getElementById('ed-bp').setAttribute('fill', fill);

    // --- 正面 ---
    const fc = document.getElementById('ed-fc').value;
    const fs = parseFloat(document.getElementById('ed-fs').value);
    const fy = parseFloat(document.getElementById('ed-fy').value);
    document.getElementById('ed-fs-v').textContent = fs;
    document.getElementById('ed-fy-v').textContent = fy;
    const ft = document.getElementById('ed-ft');
    ft.setAttribute('fill', tFill);
    ft.setAttribute('font-family', "'F-04',sans-serif");
    wrapSVGText(ft, fc, fs, fy, MAX_TEXT_W, 1.3);

    // --- 背面文字（自动换行）---
    const bc1 = document.getElementById('ed-bc1').value;
    const bs1 = parseFloat(document.getElementById('ed-bs1').value);
    const by1 = parseFloat(document.getElementById('ed-by1').value);
    document.getElementById('ed-bs1-v').textContent = bs1;
    document.getElementById('ed-by1-v').textContent = by1;
    const bt1 = document.getElementById('ed-bt1');
    bt1.setAttribute('fill', tFill);
    bt1.setAttribute('font-family', "'back_standard',sans-serif");
    wrapSVGText(bt1, bc1, bs1, by1, MAX_TEXT_W, 1.3);

    // --- 背面电话（单行，不换行）---
    const bc2 = document.getElementById('ed-bc2').value;
    const bs2 = parseFloat(document.getElementById('ed-bs2').value);
    const by2 = parseFloat(document.getElementById('ed-by2').value);
    document.getElementById('ed-bs2-v').textContent = bs2;
    document.getElementById('ed-by2-v').textContent = by2;
    const bt2 = document.getElementById('ed-bt2');
    bt2.textContent = bc2;
    bt2.setAttribute('font-size', bs2);
    bt2.setAttribute('y', by2);
    bt2.setAttribute('fill', tFill);

    document.getElementById('ed-params').textContent =
      `当前参数：形状: ${{shape}} | 颜色: ${{color}} | 正面字号: ${{fs}}px | Y: ${{fy}} | 背面文字字号: ${{bs1}}px | 文字Y: ${{by1}} | 电话字号: ${{bs2}}px | 电话Y: ${{by2}}`;
    // 同步更新订制内容字段
    const capFront = document.getElementById('cap-front');
    const capBack  = document.getElementById('cap-back');
    const capPhone = document.getElementById('cap-phone');
    if (capFront) capFront.textContent = fc;
    if (capBack)  capBack.textContent  = bc1;
    if (capPhone) capPhone.textContent = bc2;
  }};

  window.edCopyParams = function() {{
    navigator.clipboard.writeText(document.getElementById('ed-params').textContent)
      .then(()=>alert('参数已复制！'));
  }};

  window.edSendConfirm = function() {{
    alert('效果图已确认！（此处将来连接后端API发送客户确认邮件）');
  }};

  window.edDownload = function() {{
    const svg = document.getElementById('ed-svg');
    const blob = new Blob([new XMLSerializer().serializeToString(svg)], {{type:'image/svg+xml'}});
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob);
    a.download = 'effect_image.svg'; a.click();
  }};

  // 页面加载完成后立即渲染初始状态
  document.addEventListener('DOMContentLoaded', function() {{
    window.edUpdate();
  }});
}})();
</script>
<!-- ========== 效果图设计器 END ========== -->
"""

# =====================================================
# 注入到 02_待确认订单.html
# =====================================================
print("\n正在注入到 02_待确认订单.html ...")
html = HTML_PATH.read_text(encoding="utf-8")

# 匹配策略1：原始空白占位符（首次注入）
OLD_BLOCK = '''                <!-- Large Preview Area -->
                <div class="border-2 border-dashed border-slate-200 rounded-xl bg-slate-50 min-h-[400px] flex flex-col items-center justify-center relative group">
                    <div class="text-center p-8">
                        <div class="w-20 h-20 bg-slate-200 rounded-full flex items-center justify-center mx-auto mb-4 text-slate-400">
                            <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>
                        </div>
                        <h3 class="text-lg font-bold text-slate-400 mb-1">600px 宽度效果图预览</h3>
                        <p class="text-sm text-slate-400">点击放大 / 右键另存为</p>
                    </div>
                    
                    <!-- Mock Content Overlay -->
                    <div class="absolute bottom-8 left-0 right-0 px-12 flex justify-between text-sm text-slate-500">
                        <div>
                            <p class="font-bold mb-1">订制内容</p>
                            <p>正面:</p>
                        </div>
                        <div>
                            <p class="mb-1">&nbsp;</p>
                            <p>正面字体:</p>
                        </div>
                        <div>
                            <p class="mb-1">&nbsp;</p>
                            <p>背面文字:</p>
                        </div>
                    </div>
                </div>'''

NEW_BLOCK = f'''                <!-- Effect Image Designer -->
                <div class="rounded-xl bg-white border border-slate-200 p-3">
                    {DESIGNER_BLOCK}
                </div>'''

import re

if OLD_BLOCK in html:
    html = html.replace(OLD_BLOCK, NEW_BLOCK)
    HTML_PATH.write_text(html, encoding="utf-8")
    print(f"  ✅ 首次注入成功 → {HTML_PATH}")
elif '<!-- ========== 效果图设计器 START ==========' in html:
    # 匹配策略2：已注入过，替换整个设计器区块
    pattern = r'<!-- ========== \u6548\u679c\u56fe\u8bbe\u8ba1\u5668 START ==========.*?<!-- ========== \u6548\u679c\u56fe\u8bbe\u8ba1\u5668 END ==========[\s\S]*?-->'
    # 构造新的设计器内容（不含外层 div）
    new_designer_content = DESIGNER_BLOCK.strip()
    new_html, n = re.subn(pattern, lambda m: new_designer_content, html, count=1, flags=re.DOTALL)
    if n > 0:
        HTML_PATH.write_text(new_html, encoding="utf-8")
        print(f"  ✅ 更新已注入的设计器 → {HTML_PATH}")
    else:
        print(f"  ❌ 正则替换失败，请检查标记")
else:
    print(f"  ❌ 未找到任何已知注入位置")


# 同时生成独立调试页
standalone_path = OUTPUT_DIR / "effect_debug_v2.html"
standalone_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>效果图设计器 V2</title>
<script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-100 p-8">
<h2 class="text-xl font-bold text-slate-700 mb-4">🎨 效果图设计器 V2 — 背面文字/电话独立字号</h2>
<div class="bg-white rounded-2xl shadow p-6 max-w-[700px]">
{DESIGNER_BLOCK}
</div>
</body>
</html>"""
standalone_path.write_text(standalone_html, encoding="utf-8")
print(f"  ✅ 独立版 → {standalone_path}")
print("\n完成！")

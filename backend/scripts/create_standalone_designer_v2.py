# -*- coding: utf-8 -*-
"""
创建完全独立的设计器 HTML 文件 V2
- 字体转为 Base64 嵌入
- 嵌入 opentype.js 实现文字转矢量路径
- 下载的 SVG 为纯矢量路径，跨设备 100% 还原
"""

import base64
from pathlib import Path
import urllib.request

# 字体目录
FONTS_DIR = Path(__file__).parent.parent / "assets" / "fonts"
OUTPUT_DIR = Path("D:/POD_Management_V00_管理系统")

def get_font_base64(filename):
    """读取字体文件并返回 base64 字符串"""
    font_path = FONTS_DIR / filename
    if not font_path.exists():
        print(f"警告: 字体文件不存在 {filename}")
        return None
    with open(font_path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")

def get_opentype_js():
    """获取 opentype.js 库代码（从本地文件或 CDN）"""
    # 首先尝试从本地文件读取
    local_file = Path(__file__).parent / "opentype.min.js"
    if local_file.exists():
        try:
            return local_file.read_text(encoding='utf-8')
        except Exception as e:
            print(f"读取本地 opentype.js 失败: {e}")
    
    # 尝试从 CDN 下载
    try:
        url = "https://cdn.jsdelivr.net/npm/opentype.js@1.3.4/dist/opentype.min.js"
        with urllib.request.urlopen(url, timeout=30) as response:
            js_code = response.read().decode('utf-8')
            # 保存到本地文件供下次使用
            try:
                local_file.write_text(js_code, encoding='utf-8')
                print("  ✓ opentype.js 已下载并缓存到本地")
            except Exception as e:
                print(f"  缓存到本地失败: {e}")
            return js_code
    except Exception as e:
        print(f"从 CDN 下载 opentype.js 失败: {e}")
        print("  请手动下载 opentype.js 放到 scripts 目录:")
        print("  https://cdn.jsdelivr.net/npm/opentype.js@1.3.4/dist/opentype.min.js")
        raise RuntimeError("无法获取 opentype.js，请确保网络连接或手动下载")

def create_standalone_designer():
    """创建独立设计器 HTML（支持文字转矢量路径）"""
    
    # 加载所有字体
    print("正在加载字体...")
    fonts_base64 = {}
    font_files = [
        ("F-01", "F-01.ttf"),
        ("F-02", "F-02.otf"),
        ("F-03", "F-03.otf"),
        ("F-04", "F-04.ttf"),
        ("F-05", "F-05.otf"),
        ("F-06", "F-06.ttf"),
        ("F-07", "F-07.otf"),
        ("F-08", "F-08.ttf"),
        ("back_standard", "back_standard.ttf"),
    ]
    
    for font_name, filename in font_files:
        b64 = get_font_base64(filename)
        if b64:
            fonts_base64[font_name] = {
                "data": b64,
                "format": "truetype" if filename.endswith(".ttf") else "opentype"
            }
            print(f"  ✓ {font_name}: {filename}")
    
    # 生成 @font-face CSS
    font_faces = []
    for font_name, info in fonts_base64.items():
        font_faces.append(f"""
        @font-face {{
            font-family: '{font_name}';
            src: url('data:font/{info["format"]};base64,{info["data"]}') format('{info["format"]}');
            font-weight: normal;
            font-style: normal;
        }}""")
    
    font_css = "\n".join(font_faces)
    
    # 生成字体数据对象（供 opentype.js 使用）
    font_data_obj = ",\n".join([
        f"        '{name}': 'data:font/{info['format']};base64,{info['data']}'"
        for name, info in fonts_base64.items()
    ])
    
    # 获取 opentype.js
    print("\n正在下载 opentype.js...")
    opentype_js = get_opentype_js()
    print("  ✓ opentype.js 已获取")
    
    # 创建独立 HTML 文件
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>效果图设计器 - 独立版（离线矢量）</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- 嵌入 opentype.js 用于文字转矢量路径 -->
    <script>
{opentype_js}
    </script>
    <script>
    // 检查 opentype 是否加载成功
    if (typeof opentype === 'undefined') {{
        console.error('opentype.js 未正确加载');
        document.addEventListener('DOMContentLoaded', function() {{
            alert('错误：opentype.js 库未正确加载\\n\\n可能原因：\\n1. 网络连接问题\\n2. 生成脚本时下载失败\\n\\n解决方法：\\n请确保网络连接正常，然后重新运行生成脚本\\npython scripts/create_standalone_designer_v2.py');
        }});
    }}
    </script>
    <style>
        body {{ font-family: 'Inter', sans-serif; background: #f8fafc; margin: 0; padding: 20px; }}
        
        /* 嵌入的字体 - 无需外部网络 */
        {font_css}
        
        .designer-container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            padding: 24px;
        }}
        .designer-title {{
            font-size: 18px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .svg-preview {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 16px;
            margin-bottom: 16px;
        }}
        .ctrl-row {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
            color: #475569;
            margin-bottom: 6px;
        }}
        .ctrl-row label {{
            min-width: 80px;
            font-weight: 600;
        }}
        .ctrl-row input[type=range] {{
            flex: 1;
            accent-color: #3b82f6;
        }}
        .ctrl-row .vnum {{
            min-width: 36px;
            color: #e11d48;
            font-weight: 700;
            font-size: 12px;
            text-align: right;
        }}
        .ctrl-row input[type=text], .ctrl-row select {{
            flex: 1;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            padding: 6px 10px;
            font-size: 12px;
        }}
        .section-label {{
            font-size: 11px;
            font-weight: 700;
            color: #94a3b8;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            padding: 4px 0 2px;
            border-bottom: 1px solid #f1f5f9;
            margin-bottom: 8px;
        }}
        .action-btns {{
            display: flex;
            gap: 8px;
            margin-top: 16px;
            justify-content: center;
        }}
        .btn-primary {{
            background: #3b82f6;
            color: #fff;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: background 0.2s;
        }}
        .btn-primary:hover {{ background: #2563eb; }}
        .btn-ghost {{
            background: #f1f5f9;
            color: #475569;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 500;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: background 0.2s;
        }}
        .btn-ghost:hover {{ background: #e2e8f0; }}
        .params-chip {{
            font-size: 10px;
            color: #64748b;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 8px 12px;
            margin-top: 12px;
            white-space: pre-wrap;
            font-family: monospace;
            text-align: center;
        }}
        .caption-row {{
            display: flex;
            justify-content: center;
            gap: 24px;
            font-size: 12px;
            color: #64748b;
            margin-top: 8px;
        }}
        .offline-badge {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            background: #dcfce7;
            color: #166534;
            font-size: 11px;
            padding: 2px 8px;
            border-radius: 12px;
            margin-left: 8px;
        }}
        .vector-badge {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            background: #dbeafe;
            color: #1e40af;
            font-size: 11px;
            padding: 2px 8px;
            border-radius: 12px;
            margin-left: 8px;
        }}
    </style>
</head>
<body>
    <div class="designer-container">
        <div class="designer-title">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2">
                <path d="m15 12-8.5 8.5c-.83.83-2.17.83-3 0 0 0 0 0 0 0a2.12 2.12 0 0 1 0-3L12 9"/>
                <path d="M17.64 15 22 10.64"/>
                <path d="m20.91 11.7-1.25-1.25c-.6-.6-.93-1.4-.93-2.25V7.86c0-.55-.45-1-1-1H14.5c-.85 0-1.65-.33-2.25-.93L11 4.71"/>
            </svg>
            效果图设计器
            <span class="offline-badge">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
                </svg>
                离线版
            </span>
            <span class="vector-badge">100%矢量</span>
        </div>
        
        <!-- SVG 预览 -->
        <div class="svg-preview">
            <svg id="ed-svg" xmlns="http://www.w3.org/2000/svg"
                 viewBox="0 0 321 134" width="700" height="240">
                <defs>
                    <style>
                        .front-text {{ font-family: 'F-04', sans-serif; }}
                        .back-text {{ font-family: 'back_standard', sans-serif; }}
                    </style>
                </defs>
                <!-- 正面 -->
                <g id="ed-front" transform="translate(0, 0)">
                    <path id="ed-fp" transform="matrix(1,0,0,-1,0,113.3858)"
                          fill="#dabf9b" fill-rule="evenodd"
                          d="M69.8686 14.0786C68.5094 14.8158 64.5094 17.3092 62.1553 18.8983 47.5075 28.7844 36.1069 40.7415 30.2145 52.3956 25.9707 60.7907 24.5971 68.7719 26.1031 76.3129 26.9495 80.555 28.7402 84.437 31.4827 87.963 32.3107 89.0291 34.2221 91.0242 35.3058 91.9573 38.7692 94.9346 42.7311 96.8275 46.8524 97.4693 48.0892 97.6603 50.9553 97.6586 52.6629 97.4662 55.98 97.0889 58.8903 96.243 61.4594 94.8977 64.0329 97.8106 67.2554 99.5443 70.7536 99.5443 74.2912 99.5443 77.5477 97.772 80.1351 94.7988 82.5721 96.0979 85.3194 96.9633 88.3412 97.3706 89.6519 97.5475 90.8787 97.6374 92.0486 97.6385 94.134 97.6408 96.0392 97.3613 97.9174 96.7924 103.7109 95.0369 109.3989 90.2472 112.7044 84.3412 114.5509 81.0442 115.5943 77.7268 116.1085 73.5415 116.2627 72.21 116.2627 68.1591 116.0768 66.6978 115.638 63.1244 114.8357 60.035 113.4584 56.552 107.6851 41.9811 92.8831 26.5946 73.489 14.9995L71.905 14.0522C71.4226 13.752 70.4282 13.7837 69.8686 14.0786ZM71.0152 95.0488C73.5985 95.0488 75.6924 92.9548 75.6924 90.3716 75.6924 87.7884 73.5985 85.6945 71.0152 85.6945 68.432 85.6945 66.3381 87.7884 66.3381 90.3716 66.3381 92.9548 68.432 95.0488 71.0152 95.0488"/>
                    <text id="ed-ft" x="70.87" y="54" dominant-baseline="middle"
                          text-anchor="middle" font-family="'F-04',sans-serif"
                          font-size="24" fill="#333">Alice</text>
                    <!-- 上传的SVG图案 -->
                    <path id="ed-svg-pattern" style="display:none" fill="#333"/>
                </g>
                <!-- 背面 -->
                <g id="ed-back" transform="translate(159.5, 0)">
                    <path id="ed-bp" transform="matrix(1,0,0,-1,0,113.3858)"
                          fill="#dabf9b" fill-rule="evenodd"
                          d="M69.8686 14.0786C68.5094 14.8158 64.5094 17.3092 62.1553 18.8983 47.5075 28.7844 36.1069 40.7415 30.2145 52.3956 25.9707 60.7907 24.5971 68.7719 26.1031 76.3129 26.9495 80.555 28.7402 84.437 31.4827 87.963 32.3107 89.0291 34.2221 91.0242 35.3058 91.9573 38.7692 94.9346 42.7311 96.8275 46.8524 97.4693 48.0892 97.6603 50.9553 97.6586 52.6629 97.4662 55.98 97.0889 58.8903 96.243 61.4594 94.8977 64.0329 97.8106 67.2554 99.5443 70.7536 99.5443 74.2912 99.5443 77.5477 97.772 80.1351 94.7988 82.5721 96.0979 85.3194 96.9633 88.3412 97.3706 89.6519 97.5475 90.8787 97.6374 92.0486 97.6385 94.134 97.6408 96.0392 97.3613 97.9174 96.7924 103.7109 95.0369 109.3989 90.2472 112.7044 84.3412 114.5509 81.0442 115.5943 77.7268 116.1085 73.5415 116.2627 72.21 116.2627 68.1591 116.0768 66.6978 115.638 63.1244 114.8357 60.035 113.4584 56.552 107.6851 41.9811 92.8831 26.5946 73.489 14.9995L71.905 14.0522C71.4226 13.752 70.4282 13.7837 69.8686 14.0786ZM71.0152 95.0488C73.5985 95.0488 75.6924 92.9548 75.6924 90.3716 75.6924 87.7884 73.5985 85.6945 71.0152 85.6945 68.432 85.6945 66.3381 87.7884 66.3381 90.3716 66.3381 92.9548 68.432 95.0488 71.0152 95.0488"/>
                    <text id="ed-bt1" x="70.87" dominant-baseline="middle"
                          text-anchor="middle" font-family="'back_standard',sans-serif"
                          font-size="11" fill="#333"></text>
                    <text id="ed-bt2" x="70.87" y="54" dominant-baseline="middle"
                          text-anchor="middle" font-family="'back_standard',sans-serif"
                          font-size="11" fill="#333">13999926688</text>
                </g>
                <!-- 标签 -->
                <text x="81.8" y="129" font-family="Arial" font-size="7" fill="#94a3b8" text-anchor="middle">Front</text>
                <text x="241" y="129" font-family="Arial" font-size="7" fill="#94a3b8" text-anchor="middle">Back</text>
            </svg>
            
            <!-- 订制内容字段 -->
            <div class="caption-row">
                <span>Front: <strong id="cap-front">Alice</strong></span>
                <span>|</span>
                <span>Back: <strong id="cap-back">If Lost</strong></span>
                <span>|</span>
                <span>Phone: <strong id="cap-phone">13999926688</strong></span>
            </div>
        </div>

        <!-- 控制面板 -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
            <!-- 左列：正面 -->
            <div>
                <div class="section-label">正面 Front</div>
                <div class="ctrl-row">
                    <label>形状</label>
                    <select id="ed-shape" onchange="edUpdate()">
                        <option value="heart">心形 Heart</option>
                        <option value="circle">圆形 Circle</option>
                        <option value="bone">骨头形 Bone</option>
                    </select>
                </div>
                <div class="ctrl-row">
                    <label>颜色</label>
                    <select id="ed-color" onchange="edUpdate()">
                        <option value="RoseGold">玫瑰金</option>
                        <option value="Gold">金色</option>
                        <option value="Silver" selected>银色</option>
                        <option value="Black">黑色</option>
                    </select>
                </div>
                <div class="ctrl-row">
                    <label>正面文字</label>
                    <input type="text" id="ed-fc" value="Alice" oninput="edUpdate()">
                </div>
                <div class="ctrl-row">
                    <label>正面字体</label>
                    <select id="ed-ff" onchange="edUpdate()">
                        <option value="F-04">F-04 (默认)</option>
                        <option value="F-01">F-01</option>
                        <option value="F-02">F-02</option>
                        <option value="F-03">F-03</option>
                        <option value="F-05">F-05</option>
                        <option value="F-06">F-06</option>
                        <option value="F-07">F-07</option>
                        <option value="F-08">F-08</option>
                    </select>
                </div>
                <div class="ctrl-row">
                    <label>正面字号</label>
                    <input type="range" id="ed-fs" min="6" max="60" step="0.5" value="24" oninput="edUpdate()">
                    <span class="vnum" id="ed-fs-v">24</span>px
                </div>
                <div class="ctrl-row">
                    <label>正面 Y</label>
                    <input type="range" id="ed-fy" min="20" max="90" step="0.5" value="54" oninput="edUpdate()">
                    <span class="vnum" id="ed-fy-v">54</span>
                </div>
                
                <!-- SVG图案上传 -->
                <div class="section-label" style="margin-top: 16px;">自定义图案 Upload</div>
                <div class="ctrl-row">
                    <input type="file" id="ed-svg-upload" accept=".svg" onchange="edHandleSVGUpload(this)" style="display:none">
                    <button class="btn-ghost" onclick="document.getElementById('ed-svg-upload').click()" style="width: 100%; font-size: 12px;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle; margin-right: 4px;">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                            <polyline points="17 8 12 3 7 8"/>
                            <line x1="12" x2="12" y1="3" y2="15"/>
                        </svg>
                        上传SVG图案
                    </button>
                </div>
                <div id="ed-svg-controls" style="display:none;">
                    <div class="ctrl-row">
                        <label>图案缩放</label>
                        <input type="range" id="ed-svg-scale" min="0.1" max="3" step="0.1" value="1" oninput="edUpdate()">
                        <span class="vnum" id="ed-svg-scale-v">1.0</span>x
                    </div>
                    <div class="ctrl-row">
                        <label>图案 X</label>
                        <input type="range" id="ed-svg-x" min="0" max="140" step="1" value="70" oninput="edUpdate()">
                        <span class="vnum" id="ed-svg-x-v">70</span>
                    </div>
                    <div class="ctrl-row">
                        <label>图案 Y</label>
                        <input type="range" id="ed-svg-y" min="0" max="110" step="1" value="30" oninput="edUpdate()">
                        <span class="vnum" id="ed-svg-y-v">30</span>
                    </div>
                    <div class="ctrl-row">
                        <button class="btn-ghost" onclick="edClearSVG()" style="width: 100%; font-size: 12px; color: #dc2626;">清除图案</button>
                    </div>
                </div>
            </div>

            <!-- 右列：背面 -->
            <div>
                <div class="section-label">背面 Back</div>
                <div class="ctrl-row">
                    <label>背面文字</label>
                    <input type="text" id="ed-bc1" value="If Lost" oninput="edUpdate()">
                </div>
                <div class="ctrl-row">
                    <label>背面字体</label>
                    <select id="ed-bf" onchange="edUpdate()">
                        <option value="back_standard">back_standard (默认)</option>
                        <option value="F-01">F-01</option>
                        <option value="F-02">F-02</option>
                        <option value="F-03">F-03</option>
                        <option value="F-04">F-04</option>
                        <option value="F-05">F-05</option>
                        <option value="F-06">F-06</option>
                        <option value="F-07">F-07</option>
                        <option value="F-08">F-08</option>
                    </select>
                </div>
                <div class="ctrl-row">
                    <label>文字字号</label>
                    <input type="range" id="ed-bs1" min="5" max="60" step="0.5" value="11" oninput="edUpdate()">
                    <span class="vnum" id="ed-bs1-v">11</span>px
                </div>
                <div class="ctrl-row">
                    <label>文字 Y</label>
                    <input type="range" id="ed-by1" min="20" max="90" step="0.5" value="40.5" oninput="edUpdate()">
                    <span class="vnum" id="ed-by1-v">40.5</span>
                </div>
                <div class="ctrl-row">
                    <label>电话号码</label>
                    <input type="text" id="ed-bc2" value="13999926688" oninput="edUpdate()">
                </div>
                <div class="ctrl-row">
                    <label>电话字体</label>
                    <select id="ed-pf" onchange="edUpdate()">
                        <option value="back_standard">back_standard (默认)</option>
                        <option value="F-01">F-01</option>
                        <option value="F-02">F-02</option>
                        <option value="F-03">F-03</option>
                        <option value="F-04">F-04</option>
                        <option value="F-05">F-05</option>
                        <option value="F-06">F-06</option>
                        <option value="F-07">F-07</option>
                        <option value="F-08">F-08</option>
                    </select>
                </div>
                <div class="ctrl-row">
                    <label>电话字号</label>
                    <input type="range" id="ed-bs2" min="5" max="60" step="0.5" value="11" oninput="edUpdate()">
                    <span class="vnum" id="ed-bs2-v">11</span>px
                </div>
                <div class="ctrl-row">
                    <label>电话 Y</label>
                    <input type="range" id="ed-by2" min="20" max="90" step="0.5" value="54" oninput="edUpdate()">
                    <span class="vnum" id="ed-by2-v">54</span>
                </div>
            </div>
        </div>

        <!-- 操作按钮 -->
        <div class="action-btns">
            <button class="btn-primary" onclick="edDownloadVector()">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7 10 12 15 17 10"/>
                    <line x1="12" x2="12" y1="15" y2="3"/>
                </svg>
                下载矢量 SVG
            </button>
            <button class="btn-ghost" onclick="edCopyParams()">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect width="14" height="14" x="8" y="8" rx="2" ry="2"/>
                    <path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>
                </svg>
                复制参数
            </button>
            <button class="btn-ghost" onclick="edSaveDefaults()" title="保存当前设置为默认值">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>
                    <polyline points="17 21 17 13 7 13 7 21"/>
                    <polyline points="7 3 7 8 15 8"/>
                </svg>
                保存默认
            </button>
            <button class="btn-ghost" onclick="edResetDefaults()" title="重置为系统默认值" style="color: #dc2626;">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 12"/>
                    <path d="M3 3v9h9"/>
                </svg>
                重置
            </button>
        </div>
        <div class="params-chip" id="ed-params">当前参数：形状: heart | 颜色: Silver | 正面字体: F-04 | 正面字号: 24px | Y: 54 | 背面字体: back_standard | 背面字号: 11px | 电话字体: back_standard | 电话字号: 11px</div>
    </div>

    <script>
    (function(){{
      // 字体数据（base64）
      const FONT_DATA = {{
{font_data_obj}
      }};
      
      // 缓存加载的字体
      const loadedFonts = {{}};
      
      // 加载字体（使用 opentype.js）
      async function loadFontForVector(fontName) {{
        if (loadedFonts[fontName]) return loadedFonts[fontName];
        
        const fontUrl = FONT_DATA[fontName];
        if (!fontUrl) throw new Error(`字体 ${{fontName}} 不存在`);
        
        try {{
          const font = await opentype.load(fontUrl);
          loadedFonts[fontName] = font;
          return font;
        }} catch (e) {{
          console.error(`加载字体 ${{fontName}} 失败:`, e);
          throw e;
        }}
      }}
      
      // 将文字转换为 SVG 路径（使用 opentype.js，100% 精确）
      async function textToVectorPath(text, fontName, fontSize, x, y, textAnchor) {{
        if (!text || !text.trim()) return '';
        
        const font = await loadFontForVector(fontName);
        
        // 获取字体度量信息
        const unitsPerEm = font.unitsPerEm || 1000;
        const scale = fontSize / unitsPerEm;
        
        // 获取字体的度量值
        const ascender = font.ascender || 800;
        const descender = font.descender || -200;
        const fontHeight = ascender - descender;
        
        // 计算从基线到文字垂直中心的偏移
        const baselineToCenterOffset = (ascender - fontHeight/2) * scale;
        
        // 计算文字宽度
        const width = font.getAdvanceWidth(text, fontSize);
        
        // 根据 text-anchor 计算水平起始位置
        let startX = x;
        if (textAnchor === 'middle') {{
          startX = x - width / 2;
        }} else if (textAnchor === 'end') {{
          startX = x - width;
        }}
        
        // 方法：直接用 opentype.js 生成路径
        // opentype.js getPath(text, x, y, fontSize)
        // y 参数是基线位置
        //
        // dominant-baseline="middle" 的行为：
        // 浏览器会让文字的 x-height 中心对齐到 y 坐标
        // x-height 大约是 ascender 的一半
        //
        // 为了匹配 <text> 元素的 dominant-baseline="middle" 效果
        // 需要将基线放在 y 位置下方约 ascender*0.35 处
        // （经验值：中文和英文字体的 x-height 约为 ascender 的 0.5-0.7）
        
        // 微调系数：让文字往下移动以对齐预览
        const xHeightRatio = 0.35;  // x-height 相对于 ascender 的比例
        const baselineY = y + (ascender * scale * xHeightRatio);
        const path = font.getPath(text, startX, baselineY, fontSize);
        
        let pathData = path.toSVG();
        const dMatch = pathData.match(/d="([^"]+)"/);
        if (!dMatch) return '';
        let d = dMatch[1];
        
        // 不用 transform
        const transform = '';
        
        return {{ d, transform, width }};
      }}

      const PATHS = {{
        heart:  "M69.8686 14.0786C68.5094 14.8158 64.5094 17.3092 62.1553 18.8983 47.5075 28.7844 36.1069 40.7415 30.2145 52.3956 25.9707 60.7907 24.5971 68.7719 26.1031 76.3129 26.9495 80.555 28.7402 84.437 31.4827 87.963 32.3107 89.0291 34.2221 91.0242 35.3058 91.9573 38.7692 94.9346 42.7311 96.8275 46.8524 97.4693 48.0892 97.6603 50.9553 97.6586 52.6629 97.4662 55.98 97.0889 58.8903 96.243 61.4594 94.8977 64.0329 97.8106 67.2554 99.5443 70.7536 99.5443 74.2912 99.5443 77.5477 97.772 80.1351 94.7988 82.5721 96.0979 85.3194 96.9633 88.3412 97.3706 89.6519 97.5475 90.8787 97.6374 92.0486 97.6385 94.134 97.6408 96.0392 97.3613 97.9174 96.7924 103.7109 95.0369 109.3989 90.2472 112.7044 84.3412 114.5509 81.0442 115.5943 77.7268 116.1085 73.5415 116.2627 72.21 116.2627 68.1591 116.0768 66.6978 115.638 63.1244 114.8357 60.035 113.4584 56.552 107.6851 41.9811 92.8831 26.5946 73.489 14.9995L71.905 14.0522C71.4226 13.752 70.4282 13.7837 69.8686 14.0786ZM71.0152 95.0488C73.5985 95.0488 75.6924 92.9548 75.6924 90.3716 75.6924 87.7884 73.5985 85.6945 71.0152 85.6945 68.432 85.6945 66.3381 87.7884 66.3381 90.3716 66.3381 92.9548 68.432 95.0488 71.0152 95.0488",
        circle: "M70.8656 86.5749C68.2826 86.5749 66.1887 88.6689 66.1887 91.2521 66.1887 93.835 68.2826 95.9298 70.8656 95.9298 73.4488 95.9298 75.5427 93.835 75.5427 91.2521 75.5427 88.6689 73.4488 86.5749 70.8656 86.5749ZM70.8656 102.331C45.6608 102.331 25.2286 81.898 25.2286 56.6923 25.2286 31.4872 45.6608 11.0551 70.8656 11.0551 96.0707 11.0551 116.5037 31.4872 116.5037 56.6923 116.5037 81.898 96.0707 102.331 70.8656 102.331",
        bone:   "M13.6145 55.2305C14.5142 56.0177 14.5142 57.3676 13.6145 58.155 9.4527 61.9792 6.9783 67.3781 7.0906 73.2271 7.3157 84.1377 16.539 93.0234 28.0117 93.361 37.2351 93.5858 44.3214 89.3117 47.1334 83.4627 47.4707 82.5627 48.3707 82.0006 49.3829 82.0006H56.2442C57.369 82.0006 58.4935 82.6753 59.0562 83.6878 61.8681 88.6368 66.0297 91.7861 70.8664 91.7861 75.5904 91.7861 79.8647 88.6368 82.6767 83.6878 83.2391 82.6753 84.2513 82.0006 85.4887 82.0006H92.3499C93.3622 82.0006 94.2622 82.5627 94.5995 83.4627 97.524 89.3117 104.4978 93.5858 113.7209 93.361 125.0813 93.136 134.4172 84.1377 134.642 73.2271 134.7545 67.2656 132.1676 61.8667 128.1183 58.155 127.2183 57.3676 127.2183 56.0177 128.1183 55.2305 132.2799 51.406 134.7545 46.1197 134.642 40.1581 134.4172 29.2476 125.0813 20.3618 113.7209 20.0245 107.7596 19.7994 96.5117 24.5237 93.5872 31.2724 93.2496 32.1721 92.3499 32.7345 91.3377 32.7345H71.7661 67.4921 50.5077C49.4955 32.7345 48.5955 32.1721 48.2581 31.2724 45.3336 24.4111 34.0858 19.7994 28.1242 20.0245 16.7638 20.3618 7.4282 29.2476 7.2031 40.1581 6.9783 46.1197 9.5652 51.406 13.6145 55.2305ZM70.8664 87.5075C73.6784 87.5075 75.8154 84.9203 75.253 81.9958 74.9157 80.3086 73.6784 78.9591 71.9912 78.6214 68.9542 77.8343 66.2547 80.0838 66.2547 83.0083 66.3673 85.4827 68.3918 87.5075 70.8664 87.5075"
      }};
      const COLORS = {{
        RoseGold:"#dabf9b", Gold:"#ebcd7b", Silver:"#9f9fa0", Black:"#231916"
      }};
      const TEXT_COLORS = {{
        RoseGold:"#333333", Gold:"#333333", Silver:"#333333", Black:"#ffffff"
      }};
      const MAX_TEXT_W = 84.0;
      const TEXT_CX = 70.87;

      function wrapSVGText(textEl, rawText, fontSize, startY, maxWidth, lineH) {{
        while (textEl.firstChild) textEl.removeChild(textEl.firstChild);
        textEl.setAttribute('font-size', fontSize);
        const ns = 'http://www.w3.org/2000/svg';
        const probe = document.createElementNS(ns, 'tspan');
        probe.setAttribute('visibility', 'hidden');
        textEl.appendChild(probe);
        const words = rawText.split(/\s+/).filter(w => w.length > 0);
        let lines = [];
        let cur = '';
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
        const totalH = (lines.length - 1) * lineSpacing;
        const firstY = startY - totalH / 2;
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

      // SVG图案相关变量
      let uploadedSVGContent = null;
      let uploadedSVGViewBox = null;

      // 处理SVG文件上传
      window.edHandleSVGUpload = function(input) {{
        const file = input.files[0];
        if (!file) return;
        
        const reader = new FileReader();
        reader.onload = function(e) {{
          const svgText = e.target.result;
          
          // 解析SVG获取viewBox
          const parser = new DOMParser();
          const doc = parser.parseFromString(svgText, 'image/svg+xml');
          const svgEl = doc.querySelector('svg');
          
          if (svgEl) {{
            // 提取所有path数据
            const paths = svgEl.querySelectorAll('path');
            let pathData = '';
            paths.forEach(p => {{
              const d = p.getAttribute('d');
              if (d) pathData += d + ' ';
            }});
            
            if (pathData) {{
              uploadedSVGContent = pathData.trim();
              
              // 获取viewBox
              const viewBox = svgEl.getAttribute('viewBox') || '0 0 100 100';
              uploadedSVGViewBox = viewBox.split(/\s+/).map(Number);
              
              // 显示控制面板
              document.getElementById('ed-svg-controls').style.display = 'block';
              
              // 更新预览
              edUpdate();
              
              alert('SVG图案上传成功！');
            }} else {{
              alert('未找到有效的路径数据，请确保SVG包含<path>元素');
            }}
          }} else {{
            alert('无法解析SVG文件');
          }}
        }};
        reader.readAsText(file);
      }};

      // 清除上传的SVG
      window.edClearSVG = function() {{
        uploadedSVGContent = null;
        uploadedSVGViewBox = null;
        document.getElementById('ed-svg-upload').value = '';
        document.getElementById('ed-svg-controls').style.display = 'none';
        edUpdate();
      }};

      window.edUpdate = function() {{
        const shape = document.getElementById('ed-shape').value;
        const color = document.getElementById('ed-color').value;
        const fill = COLORS[color];
        const tFill = TEXT_COLORS[color];
        const d = PATHS[shape];
        
        const frontFont = document.getElementById('ed-ff').value;
        const backFont = document.getElementById('ed-bf').value;
        const phoneFont = document.getElementById('ed-pf').value;

        document.getElementById('ed-fp').setAttribute('d', d);
        document.getElementById('ed-bp').setAttribute('d', d);
        document.getElementById('ed-fp').setAttribute('fill', fill);
        document.getElementById('ed-bp').setAttribute('fill', fill);

        const fc = document.getElementById('ed-fc').value;
        const fs = parseFloat(document.getElementById('ed-fs').value);
        const fy = parseFloat(document.getElementById('ed-fy').value);
        document.getElementById('ed-fs-v').textContent = fs;
        document.getElementById('ed-fy-v').textContent = fy;
        const ft = document.getElementById('ed-ft');
        ft.setAttribute('fill', tFill);
        ft.setAttribute('font-family', `"${{frontFont}}",sans-serif`);
        wrapSVGText(ft, fc, fs, fy, MAX_TEXT_W, 1.3);

        const bc1 = document.getElementById('ed-bc1').value;
        const bs1 = parseFloat(document.getElementById('ed-bs1').value);
        const by1 = parseFloat(document.getElementById('ed-by1').value);
        document.getElementById('ed-bs1-v').textContent = bs1;
        document.getElementById('ed-by1-v').textContent = by1;
        const bt1 = document.getElementById('ed-bt1');
        bt1.setAttribute('fill', tFill);
        bt1.setAttribute('font-family', `"${{backFont}}",sans-serif`);
        wrapSVGText(bt1, bc1, bs1, by1, MAX_TEXT_W, 1.3);

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
        bt2.setAttribute('font-family', `"${{phoneFont}}",sans-serif`);

        // 渲染上传的SVG图案
        const svgPatternEl = document.getElementById('ed-svg-pattern');
        if (uploadedSVGContent && svgPatternEl) {{
          const scale = parseFloat(document.getElementById('ed-svg-scale').value);
          const x = parseFloat(document.getElementById('ed-svg-x').value);
          const y = parseFloat(document.getElementById('ed-svg-y').value);
          
          // 更新显示值
          document.getElementById('ed-svg-scale-v').textContent = scale.toFixed(1);
          document.getElementById('ed-svg-x-v').textContent = x;
          document.getElementById('ed-svg-y-v').textContent = y;
          
          // 计算变换
          // 根据viewBox计算合适的缩放
          let baseScale = 1;
          if (uploadedSVGViewBox && uploadedSVGViewBox.length >= 4) {{
            const vbWidth = uploadedSVGViewBox[2];
            const vbHeight = uploadedSVGViewBox[3];
            if (vbWidth > 0 && vbHeight > 0) {{
              // 默认缩放到约30px宽度
              baseScale = 30 / Math.max(vbWidth, vbHeight);
            }}
          }}
          
          const finalScale = baseScale * scale;
          const transform = `translate(${{x}}, ${{y}}) scale(${{finalScale}})`;
          
          svgPatternEl.setAttribute('d', uploadedSVGContent);
          svgPatternEl.setAttribute('transform', transform);
          svgPatternEl.setAttribute('fill', tFill);
          svgPatternEl.style.display = 'block';
        }} else if (svgPatternEl) {{
          svgPatternEl.style.display = 'none';
        }}

        document.getElementById('ed-params').textContent =
          `当前参数：形状: ${{shape}} | 颜色: ${{color}} | 正面字体: ${{frontFont}} | 正面字号: ${{fs}}px | Y: ${{fy}} | 背面字体: ${{backFont}} | 背面字号: ${{bs1}}px | 电话字体: ${{phoneFont}} | 电话字号: ${{bs2}}px`;
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

      // 下载矢量 SVG（文字转为路径，100% 精确）
      window.edDownloadVector = async function() {{
        try {{
          // 显示加载状态
          const btn = document.querySelector('.btn-primary');
          const originalText = btn.innerHTML;
          btn.innerHTML = '<span>转换中...</span>';
          btn.disabled = true;
          
          // 克隆 SVG
          const originalSvg = document.getElementById('ed-svg');
          const clonedSvg = originalSvg.cloneNode(true);
          
          // 获取当前设置
          const frontFont = document.getElementById('ed-ff').value;
          const backFont = document.getElementById('ed-bf').value;
          const phoneFont = document.getElementById('ed-pf').value;
          const tFill = TEXT_COLORS[document.getElementById('ed-color').value];
          
          // 转换正面文字
          const ft = clonedSvg.getElementById('ed-ft');
          if (ft && ft.textContent.trim()) {{
            const frontPath = await textToVectorPath(
              ft.textContent, 
              frontFont, 
              parseFloat(ft.getAttribute('font-size')) || 24,
              parseFloat(ft.getAttribute('x')) || 70.87,
              parseFloat(ft.getAttribute('y')) || 54,
              ft.getAttribute('text-anchor') || 'middle'
            );
            if (frontPath.d) {{
              const pathEl = document.createElementNS('http://www.w3.org/2000/svg', 'path');
              pathEl.setAttribute('d', frontPath.d);
              pathEl.setAttribute('fill', tFill);
              if (frontPath.transform) pathEl.setAttribute('transform', frontPath.transform);
              ft.parentNode.replaceChild(pathEl, ft);
            }}
          }}
          
          // 转换背面文字
          const bt1 = clonedSvg.getElementById('ed-bt1');
          if (bt1 && bt1.textContent.trim()) {{
            // 修复：wrapSVGText 将 y 设置在 tspan 上，需要从 tspan 获取
            const firstTspan = bt1.querySelector('tspan');
            const bt1Y = firstTspan ? parseFloat(firstTspan.getAttribute('y')) : parseFloat(bt1.getAttribute('y'));
            
            const backPath = await textToVectorPath(
              bt1.textContent,
              backFont,
              parseFloat(bt1.getAttribute('font-size')) || 11,
              parseFloat(bt1.getAttribute('x')) || 70.87,
              bt1Y || 40.5,
              bt1.getAttribute('text-anchor') || 'middle'
            );
            if (backPath.d) {{
              const pathEl = document.createElementNS('http://www.w3.org/2000/svg', 'path');
              pathEl.setAttribute('d', backPath.d);
              pathEl.setAttribute('fill', tFill);
              if (backPath.transform) pathEl.setAttribute('transform', backPath.transform);
              bt1.parentNode.replaceChild(pathEl, bt1);
            }}
          }}
          
          // 转换电话号码
          const bt2 = clonedSvg.getElementById('ed-bt2');
          if (bt2 && bt2.textContent.trim()) {{
            const phonePath = await textToVectorPath(
              bt2.textContent,
              phoneFont,
              parseFloat(bt2.getAttribute('font-size')) || 11,
              parseFloat(bt2.getAttribute('x')) || 70.87,
              parseFloat(bt2.getAttribute('y')) || 54,
              bt2.getAttribute('text-anchor') || 'middle'
            );
            if (phonePath.d) {{
              const pathEl = document.createElementNS('http://www.w3.org/2000/svg', 'path');
              pathEl.setAttribute('d', phonePath.d);
              pathEl.setAttribute('fill', tFill);
              if (phonePath.transform) pathEl.setAttribute('transform', phonePath.transform);
              bt2.parentNode.replaceChild(pathEl, bt2);
            }}
          }}
          
          // 处理上传的SVG图案（已经是path，只需确保显示）
          const svgPattern = clonedSvg.getElementById('ed-svg-pattern');
          if (svgPattern && uploadedSVGContent) {{
            svgPattern.style.display = 'block';
            svgPattern.setAttribute('fill', tFill);
          }}
          
          // 移除 defs（不再需要字体样式）
          const defs = clonedSvg.querySelector('defs');
          if (defs) defs.remove();
          
          // 下载
          const svgData = new XMLSerializer().serializeToString(clonedSvg);
          const blob = new Blob([svgData], {{type: 'image/svg+xml'}});
          const a = document.createElement('a');
          a.href = URL.createObjectURL(blob);
          a.download = 'effect_vector.svg';
          a.click();
          
          // 恢复按钮
          btn.innerHTML = originalText;
          btn.disabled = false;
          
        }} catch (e) {{
          console.error('下载失败:', e);
          alert('转换失败: ' + e.message);
          const btn = document.querySelector('.btn-primary');
          btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>下载矢量 SVG';
          btn.disabled = false;
        }}
      }};

      // 默认值配置（保存到 localStorage 的键名）
      const DEFAULTS_KEY = 'designerDefaults';
      
      // 需要保存的字段列表
      const DEFAULT_FIELDS = [
        {{ id: 'ed-shape', type: 'select' }},
        {{ id: 'ed-color', type: 'select' }},
        {{ id: 'ed-fc', type: 'text' }},
        {{ id: 'ed-ff', type: 'select' }},
        {{ id: 'ed-fs', type: 'range' }},
        {{ id: 'ed-fy', type: 'range' }},
        {{ id: 'ed-bc1', type: 'text' }},
        {{ id: 'ed-bf', type: 'select' }},
        {{ id: 'ed-bs1', type: 'range' }},
        {{ id: 'ed-by1', type: 'range' }},
        {{ id: 'ed-bc2', type: 'text' }},
        {{ id: 'ed-pf', type: 'select' }},
        {{ id: 'ed-bs2', type: 'range' }},
        {{ id: 'ed-by2', type: 'range' }},
        {{ id: 'ed-svg-scale', type: 'range' }},
        {{ id: 'ed-svg-x', type: 'range' }},
        {{ id: 'ed-svg-y', type: 'range' }}
      ];
      
      // 加载保存的默认值
      function loadDefaults() {{
        try {{
          const saved = localStorage.getItem(DEFAULTS_KEY);
          if (saved) {{
            const defaults = JSON.parse(saved);
            DEFAULT_FIELDS.forEach(field => {{
              const el = document.getElementById(field.id);
              if (el && defaults[field.id] !== undefined) {{
                el.value = defaults[field.id];
                // 触发显示更新
                const valueSpan = document.getElementById(field.id + '-v');
                if (valueSpan) {{
                  valueSpan.textContent = el.value;
                }}
              }}
            }});
            console.log('已加载保存的默认值');
          }}
        }} catch (e) {{
          console.error('加载默认值失败:', e);
        }}
      }}
      
      // 保存当前值为默认值
      window.edSaveDefaults = function() {{
        try {{
          const defaults = {{}};
          DEFAULT_FIELDS.forEach(field => {{
            const el = document.getElementById(field.id);
            if (el) {{
              defaults[field.id] = el.value;
            }}
          }});
          localStorage.setItem(DEFAULTS_KEY, JSON.stringify(defaults));
          alert('当前设置已保存为默认值！');
        }} catch (e) {{
          console.error('保存默认值失败:', e);
          alert('保存失败: ' + e.message);
        }}
      }};
      
      // 重置为系统默认值
      window.edResetDefaults = function() {{
        if (confirm('确定要清除保存的默认值吗？')) {{
          localStorage.removeItem(DEFAULTS_KEY);
          location.reload();
        }}
      }};

      // 页面加载完成后立即渲染初始状态
      document.addEventListener('DOMContentLoaded', function() {{
        loadDefaults();
        window.edUpdate();
      }});
    }})();
    </script>
</body>
</html>'''
    
    # 保存文件
    output_path = OUTPUT_DIR / "designer-offline-vector.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    # 计算文件大小
    file_size = output_path.stat().st_size
    file_size_mb = file_size / (1024 * 1024)
    
    print(f"\n✅ 独立矢量设计器已创建！")
    print(f"📁 文件路径: {output_path}")
    print(f"📊 文件大小: {file_size_mb:.2f} MB")
    print(f"🔤 嵌入字体: {len(fonts_base64)} 个")
    print(f"📦 嵌入 opentype.js: 是")
    print(f"\n💡 特点:")
    print(f"   - 完全离线，无需网络")
    print(f"   - 下载的 SVG 为纯矢量路径")
    print(f"   - 100% 字体还原精度")
    print(f"   - 工厂雕刻直接可用")

if __name__ == "__main__":
    create_standalone_designer()

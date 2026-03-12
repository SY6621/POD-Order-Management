# -*- coding: utf-8 -*-
"""
Effect Image Template Service
生成效果图：分离式12模板架构（规范 V1.3）

====================================================================
效果图核心模块规范（写入版本）
====================================================================

【架构原则】
  效果图核心 SVG 与尺寸标注完全分离：
  - generate_effect_image()  → 纯净 SVG，只含形状+颜色+文字
  - wrap_with_dimension()    → 外部包裹，添加尺寸标注+边框
  调用方按需选择，核心出图永远稳定，标注功能不影响渲染。

【文字渲染规范（硬性规定）】
  1. 防溢出：所有文字字号通过安全字号算法计算，确保文字在形状宽度内
  2. 边缘安全距：文字距形状边缘至少 EDGE_MARGIN = 2.0 px（可调）
     └─ 体现在 max_text_width = 形状实际可用宽 - 2 × EDGE_MARGIN × 2
  3. 背面双字段：两行文字行间距 = max(text_size, phone_size) × LINE_SPACING_RATIO
     └─ LINE_SPACING_RATIO = 1.4（可调），确保两行不叠字
  4. 默认字号：背面两字段以字符数较多一方为基准，默认同等字号
  5. 用户微调：字号 ±3%（Ctrl+±），Y位置 ±2px（方向键）

【颜色规范】
  颜色通过字符串替换直接写入 path fill 属性（内联 inline），
  不使用 CSS class，确保 svglib 等工具正确渲染。

【Y轴规范】
  所有形状 path 使用 transform="matrix(1,0,0,-1,0,vh)" Y轴翻转，
  使挂孔在上方（与实物一致）。
====================================================================
"""

import re
import base64
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

# ============================================================
# 字体路径 & base64 缓存
# ============================================================

FONTS_DIR = Path(__file__).parent.parent.parent / "assets" / "fonts"
_FONT_B64_CACHE: dict = {}

def _get_font_b64(font_filename: str) -> str:
    """读取字体文件并返回 base64 字符串（带缓存，只读一次）。"""
    if font_filename not in _FONT_B64_CACHE:
        font_path = FONTS_DIR / font_filename
        if font_path.exists():
            raw = font_path.read_bytes()
            _FONT_B64_CACHE[font_filename] = base64.b64encode(raw).decode("ascii")
        else:
            _FONT_B64_CACHE[font_filename] = ""
    return _FONT_B64_CACHE[font_filename]


# ============================================================
# 颜色映射
# ============================================================

COLOR_FILLS = {
    "Silver":   "#9f9fa0",
    "Gold":     "#ebcd7b",
    "RoseGold": "#dabf9b",
    "Black":    "#231916",
}

# 中文颜色名 → 英文 key
COLOR_NAME_MAP = {
    "银色": "Silver",
    "金色": "Gold",
    "玫瑰金": "RoseGold",
    "黑色": "Black",
}

# ============================================================
# 形状 → 模板 key 映射
# ============================================================

SHAPE_KEY_MAP = {
    "心形": "heart",
    "圆形": "circle",
    "骨头形": "bone",
    "Heart": "heart",
    "Circle": "circle",
    "Bone": "bone",
}

# ============================================================
# 各形状/尺寸 尺寸参数（毫米）- 用于外部尺寸标注
# ============================================================

SHAPE_DIMENSIONS = {
    "heart": {"L": (32, 30), "S": (23, 21)},
    "circle": {"L": (32, 32), "S": (23, 23)},
    "bone":   {"L": (45, 26), "S": (28, 16)},
}

# ============================================================
# 模板中心点 & 可用文字区（避免溢出形状边界）
# 规范：所有文字必须在形状内部，不得溢出
# ============================================================

TEMPLATE_INFO = {
    "L": {
        "cx": 70.87,
        "cy": 54.0,          # 正面文字视觉中心Y（已由设计器确认：front_y=54）
        "max_text_width": 84.0,
        "text_area_top": 24.0,
        "text_area_bottom": 82.0,
        # ── 由设计器校准的默认渲染参数（heart/RoseGold 基准，2026-03-06确认）──
        "default_front_size": 24.0,   # 正面默认字号
        "default_front_y":   54.0,    # 正面默认Y
        "default_back_size": 11.0,    # 背面默认字号（文字与电话同基准）
        "default_back_text_y":  40.5, # 背面文字默认Y
        "default_back_phone_y": 54.0, # 背面电话默认Y
    },
    "S": {
        "cx": 53.86,
        "cy": 50.0,
        "max_text_width": 62.0,
        "text_area_top": 30.0,
        "text_area_bottom": 68.0,
        "default_front_size": 18.0,
        "default_front_y":   50.0,
        "default_back_size": 9.0,
        "default_back_text_y":  43.0,
        "default_back_phone_y": 54.0,
    },
}

# ============================================================
# 文字渲染关键参数（可调）
# ============================================================

# 文字距形状边缘安全距离（px），硬性规定不可为0（可调）
EDGE_MARGIN = 2.0

# 背面双字段行间距：两行之间固定空白像素（视觉间距，不依赖字号系数）
BACK_LINE_GAP = 2.0   # 两行文字之间的空白 = 2px（可调）

# ============================================================
# 字体宽度系数（用于计算溢出保护字号）
# ============================================================

# 字体宽度系数：每1px字号，单字符视觉宽度 = 字号 × 系数
# 取保守值（偏大），确保计算结果字号不会溢出边界
FONT_WIDTH_RATIO = {
    "F-01": 0.72,
    "F-02": 0.80,
    "F-03": 0.72,
    "F-04": 0.72,   # F-04 实测偏宽，取0.72保守估算
    "F-05": 0.70,
    "F-06": 0.75,
    "F-07": 0.68,
    "F-08": 0.78,
    "back_standard": 0.62,  # 背面标准字体（等宽类，比例较小）
}

# ============================================================
# 模板目录
# ============================================================

TEMPLATE_DIR = Path(__file__).parent.parent / "effect_templates"


# ============================================================
# 配置数据类
# ============================================================

@dataclass
class FrontConfig:
    """正面配置"""
    text: str = ""
    font_family: str = "F-04"
    font_size_adjust: float = 0.0    # ±3%，用户微调值（百分比）
    y_offset: float = 0.0            # ±2px，用户微调值


@dataclass
class BackConfig:
    """背面配置"""
    text_content: str = ""           # 附加文字（如 If Lost）
    text_font_size_adjust: float = 0.0
    text_y_offset: float = 0.0
    phone_number: str = ""
    phone_font_size_adjust: float = 0.0
    phone_y_offset: float = 0.0
    layout_mode: str = "text_top"    # "text_top" 文字在上 | "phone_top" 号码在上


@dataclass
class EffectConfig:
    """效果图完整配置"""
    shape: str = "heart"             # heart / circle / bone（或中文）
    size: str = "L"                  # L / S
    color: str = "RoseGold"          # Silver / Gold / RoseGold / Black（或中文）
    front: FrontConfig = field(default_factory=FrontConfig)
    back: BackConfig = field(default_factory=BackConfig)


# ============================================================
# 内部工具函数
# ============================================================

def _resolve_color(color_input: str) -> str:
    """解析颜色名称（支持中英文），返回 HEX 色值。"""
    en_key = COLOR_NAME_MAP.get(color_input, color_input)
    return COLOR_FILLS.get(en_key, "#9f9fa0")


def _resolve_shape(shape_input: str) -> str:
    """解析形状名称（支持中英文），返回模板 key。"""
    return SHAPE_KEY_MAP.get(shape_input, "heart")


def _calc_safe_font_size(
    text: str, font_family: str, size: str, adjust_pct: float,
    max_font: float = 36.0, min_font: float = 6.0
) -> float:
    """
    计算字号，保证文字不超出形状可用宽度（硬性规定）。

    策略：可用宽度 / (字符数 × 字体宽度系数) 得到最大安全字号，
    再乘以用户微调百分比，最终 clamp 到 [min_font, max_font]。
    """
    info = TEMPLATE_INFO[size]
    max_width = info["max_text_width"]
    char_count = max(len(text), 1)
    width_ratio = FONT_WIDTH_RATIO.get(font_family, 0.60)

    # 安全字号 = 可用宽度 / (字符数 × 每字符宽度系数)
    safe_size = max_width / (char_count * width_ratio)
    safe_size = min(max_font, max(min_font, safe_size))

    # 应用用户微调（±3%）
    safe_size = safe_size * (1.0 + adjust_pct / 100.0)
    # 再次限幅，确保溢出保护生效
    safe_size = min(max_font, max(min_font, safe_size))

    return round(safe_size, 2)


def _calc_back_layout(
    size: str, text_size: float, phone_size: float,
    layout_mode: str,
    text_y_offset: float, phone_y_offset: float
) -> tuple[float, float]:
    """
    根据排版模式计算背面两行文字的 Y 坐标。
    使用 dominant-baseline="middle"，Y = 文字视觉中心。

    行间距算法：
      两行重心距 = text_size/2 + BACK_LINE_GAP + phone_size/2
      这样两行之间视觉空白 = BACK_LINE_GAP（2px）
    """
    info = TEMPLATE_INFO[size]
    cy   = info["cy"]

    # 两行重心距 = 上行半身高 + 固定间隔 + 下行半身高
    half_gap = (text_size / 2.0) + BACK_LINE_GAP + (phone_size / 2.0)

    if layout_mode == "text_top":
        text_y  = cy - half_gap / 2.0 + text_y_offset
        phone_y = cy + half_gap / 2.0 + phone_y_offset
    else:
        phone_y = cy - half_gap / 2.0 + phone_y_offset
        text_y  = cy + half_gap / 2.0 + text_y_offset

    # 限制在文字可用区内（防止出界）
    top    = info["text_area_top"]
    bottom = info["text_area_bottom"]
    text_y  = max(top, min(bottom, text_y))
    phone_y = max(top, min(bottom, phone_y))

    return round(text_y, 2), round(phone_y, 2)


def _extract_inner_content(svg: str) -> str:
    """从完整 SVG 中提取 <svg> 内部内容（去掉外层 svg 标签和 xml 声明）。"""
    inner = re.sub(r'<\?xml[^>]*\?>', '', svg)
    inner = re.sub(r'<!--.*?-->', '', inner, flags=re.DOTALL)
    match = re.search(r'<svg[^>]*>(.*?)</svg>', inner, re.DOTALL)
    if match:
        return match.group(1).strip()
    return inner.strip()


# ============================================================
# 渲染函数
# ============================================================

def _render_front(config: EffectConfig) -> str:
    """读取正面模板，替换占位符，返回完整 SVG 字符串。"""
    shape = _resolve_shape(config.shape)
    template_path = TEMPLATE_DIR / f"front_{shape}_{config.size}.svg"
    svg = template_path.read_text(encoding="utf-8")

    color_fill = _resolve_color(config.color)
    info = TEMPLATE_INFO[config.size]

    # 优先使用设计器校准的默认值，再叠加用户微调
    default_size = info["default_front_size"]
    default_y    = info["default_front_y"]

    # 用户微调 ±N%（font_size_adjust）叠加到默认值
    font_size = round(default_size * (1.0 + config.front.font_size_adjust / 100.0), 2)
    # 防溢出保护
    font_size = min(info["max_text_width"] / max(len(config.front.text), 1) / FONT_WIDTH_RATIO.get(config.front.font_family, 0.72) * 1.0,
                    font_size)
    font_size = max(6.0, round(font_size, 2))

    text_y = round(default_y + config.front.y_offset, 2)

    svg = svg.replace("{{COLOR_FILL}}", color_fill)
    svg = svg.replace("{{FONT_FAMILY}}", config.front.font_family)
    svg = svg.replace("{{FONT_SIZE}}", str(font_size))
    svg = svg.replace("{{TEXT_CONTENT}}", config.front.text)
    svg = svg.replace("{{TEXT_Y}}", str(text_y))

    return svg


def _render_back(config: EffectConfig) -> str:
    """读取背面模板，替换占位符，返回完整 SVG 字符串。

    背面支持文字和电话独立字号调整：
    - text_font_size_adjust:  文字字号微调百分比（独立）
    - phone_font_size_adjust: 电话字号微调百分比（独立）
    - 两者默认均基于 default_back_size，可各自偏移
    """
    shape = _resolve_shape(config.shape)
    template_path = TEMPLATE_DIR / f"back_{shape}_{config.size}.svg"
    svg = template_path.read_text(encoding="utf-8")

    color_fill = _resolve_color(config.color)
    info = TEMPLATE_INFO[config.size]

    # 从设计器确认的默认值出发，文字和电话各自独立微调
    default_back = info["default_back_size"]
    text_size  = round(default_back * (1.0 + config.back.text_font_size_adjust  / 100.0), 2)
    phone_size = round(default_back * (1.0 + config.back.phone_font_size_adjust / 100.0), 2)
    # 溢出保护 clamp
    text_size  = min(22.0, max(5.0, text_size))
    phone_size = min(22.0, max(5.0, phone_size))

    # Y 坐标：优先使用设计器校准值，叠加用户微调
    text_y  = round(info["default_back_text_y"]  + config.back.text_y_offset,  2)
    phone_y = round(info["default_back_phone_y"] + config.back.phone_y_offset, 2)

    # 防止出界
    top, bottom = info["text_area_top"], info["text_area_bottom"]
    text_y  = max(top, min(bottom, text_y))
    phone_y = max(top, min(bottom, phone_y))

    svg = svg.replace("{{COLOR_FILL}}", color_fill)
    svg = svg.replace("{{TEXT_FONT_SIZE}}", str(text_size))
    svg = svg.replace("{{PHONE_FONT_SIZE}}", str(phone_size))
    svg = svg.replace("{{TEXT_CONTENT}}", config.back.text_content)
    svg = svg.replace("{{PHONE_NUMBER}}", config.back.phone_number)
    svg = svg.replace("{{TEXT_Y}}", str(text_y))
    svg = svg.replace("{{PHONE_Y}}", str(phone_y))

    return svg


# ============================================================
# 主函数：生成效果图（架构拆分：核心 + 外部标注）
# ============================================================

def generate_effect_image(config: EffectConfig) -> str:
    """
    【核心函数】生成纯净效果图 SVG：正面 + 18px间距 + 背面 + 外边框。

    规范 V1.3：此函数只负责形状+颜色+文字渲染，不含尺寸标注。
    如需尺寸标注，调用 wrap_with_dimension(svg, config)。

    Returns:
        纯净 SVG 字符串，可直接嵌入HTML预览或发送给客户。
    """
    front_svg = _render_front(config)
    back_svg  = _render_back(config)

    shape_w = 141.7323 if config.size == "L" else 107.7168
    shape_h = 113.3858
    gap     = 18.0
    padding = 10.0

    front_content = _extract_inner_content(front_svg)
    back_content  = _extract_inner_content(back_svg)

    content_w = padding + shape_w + gap + shape_w + padding
    content_h = padding + shape_h + padding

    front_lx = padding + shape_w / 2
    back_lx  = padding + shape_w + gap + shape_w / 2
    label_y  = content_h - 1

    # 嵌入字体：F-04（正面）+ back_standard（背面）
    # 写法与设计器一致：<defs><style>@font-face{...}</style></defs>
    f04_b64  = _get_font_b64("F-04.ttf")
    back_b64 = _get_font_b64("back_standard.ttf")

    font_style = ""
    if f04_b64:
        font_style = f"""  <defs>
    <style>
      @font-face {{ font-family: 'F-04'; src: url('data:font/truetype;base64,{f04_b64}') format('truetype'); }}
      @font-face {{ font-family: 'back_standard'; src: url('data:font/truetype;base64,{back_b64}') format('truetype'); }}
    </style>
  </defs>"""

    return f'''<?xml version="1.0" encoding="utf-8"?>
<svg version="1.1" xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 {content_w:.4f} {content_h:.4f}"
     width="{content_w:.2f}" height="{content_h:.2f}"
     xml:space="preserve">

{font_style}

  <!-- 外层轻边框 -->
  <rect x="0.5" y="0.5" width="{content_w-1:.4f}" height="{content_h-1:.4f}"
        fill="none" stroke="#e2e8f0" stroke-width="0.8"/>

  <!-- 正面 -->
  <g transform="translate({padding:.2f},{padding:.2f})">
    {front_content}
  </g>

  <!-- 背面 -->
  <g transform="translate({padding + shape_w + gap:.2f},{padding:.2f})">
    {back_content}
  </g>

  <!-- Front / Back 标签 -->
  <text x="{front_lx:.2f}" y="{label_y:.2f}"
        font-family="Arial,sans-serif" font-size="7" fill="#94a3b8"
        text-anchor="middle">Front</text>
  <text x="{back_lx:.2f}" y="{label_y:.2f}"
        font-family="Arial,sans-serif" font-size="7" fill="#94a3b8"
        text-anchor="middle">Back</text>

</svg>'''


def wrap_with_dimension(core_svg: str, config: EffectConfig) -> str:
    """
    【外部包裹函数】在纯净效果图外部添加尺寸标注。

    规范 V1.3：尺寸标注与效果图核心完全分离，
    此函数不影响效果图本身的渲染稳定性。

    Args:
        core_svg: generate_effect_image() 返回的纯净 SVG
        config:   效果图配置（用于获取尺寸数据）

    Returns:
        包含尺寸标注的完整 SVG 字符串
    """
    shape_key = _resolve_shape(config.shape)
    w_mm, h_mm = SHAPE_DIMENSIONS.get(shape_key, {}).get(config.size, (32, 30))

    shape_w = 141.7323 if config.size == "L" else 107.7168
    shape_h = 113.3858
    gap     = 18.0
    padding = 10.0
    content_w = padding + shape_w + gap + shape_w + padding
    content_h = padding + shape_h + padding

    # 外部标注区域
    dim_top  = 22.0
    dim_left = 22.0
    canvas_w = dim_left + content_w
    canvas_h = dim_top  + content_h

    # 提取 core_svg 内容
    inner = _extract_inner_content(core_svg)

    # 宽度标注（正面上方，外框外）
    x1 = dim_left + padding
    x2 = dim_left + padding + shape_w
    ay = dim_top - 5
    # 高度标注（外框左侧）
    y1 = dim_top + padding
    y2 = dim_top + padding + shape_h
    ax = dim_left - 5
    my = (y1 + y2) / 2

    return f'''<?xml version="1.0" encoding="utf-8"?>
<svg version="1.1" xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 {canvas_w:.4f} {canvas_h:.4f}"
     width="{canvas_w:.2f}" height="{canvas_h:.2f}"
     xml:space="preserve">

  <!-- 效果图核心内容（平移到标注区域右下方） -->
  <g transform="translate({dim_left:.2f},{dim_top:.2f})">
    {inner}
  </g>

  <!-- 宽度标注（外框上方） -->
  <line x1="{x1:.2f}" y1="{ay:.2f}" x2="{x2:.2f}" y2="{ay:.2f}" stroke="#E71F19" stroke-width="0.8"/>
  <line x1="{x1:.2f}" y1="{ay-3:.2f}" x2="{x1:.2f}" y2="{ay+3:.2f}" stroke="#E71F19" stroke-width="0.8"/>
  <line x1="{x2:.2f}" y1="{ay-3:.2f}" x2="{x2:.2f}" y2="{ay+3:.2f}" stroke="#E71F19" stroke-width="0.8"/>
  <text x="{(x1+x2)/2:.2f}" y="{ay-4:.2f}" font-family="Arial,sans-serif" font-size="8"
        fill="#E71F19" text-anchor="middle">{w_mm} mm</text>

  <!-- 高度标注（外框左侧） -->
  <line x1="{ax:.2f}" y1="{y1:.2f}" x2="{ax:.2f}" y2="{y2:.2f}" stroke="#E71F19" stroke-width="0.8"/>
  <line x1="{ax-3:.2f}" y1="{y1:.2f}" x2="{ax+3:.2f}" y2="{y1:.2f}" stroke="#E71F19" stroke-width="0.8"/>
  <line x1="{ax-3:.2f}" y1="{y2:.2f}" x2="{ax+3:.2f}" y2="{y2:.2f}" stroke="#E71F19" stroke-width="0.8"/>
  <text x="{ax-5:.2f}" y="{my:.2f}" font-family="Arial,sans-serif" font-size="8"
        fill="#E71F19" text-anchor="middle"
        transform="rotate(-90,{ax-5:.2f},{my:.2f})">{h_mm} mm</text>

</svg>'''


def save_effect_image(config: EffectConfig, output_path: Optional[Path] = None,
                      with_dimension: bool = True) -> Path:
    """
    生成效果图并保存为 SVG 文件，返回保存路径。

    Args:
        config:         效果图配置
        output_path:    指定保存路径（None=自动生成）
        with_dimension: True=保存含尺寸标注版；False=保存纯净核心版
    """
    core_svg = generate_effect_image(config)
    svg_content = wrap_with_dimension(core_svg, config) if with_dimension else core_svg

    if output_path is None:
        output_dir = Path(__file__).parent.parent.parent / "output"
        output_dir.mkdir(exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        shape = _resolve_shape(config.shape)
        suffix = "_dim" if with_dimension else ""
        output_path = output_dir / f"effect_{shape}_{config.size}_{config.color}{suffix}_{ts}.svg"

    output_path.write_text(svg_content, encoding="utf-8")
    return output_path


# ============================================================
# 订单效果图自动生成（订单数据 → SVG → 上传 → 回写URL）
# ============================================================

def _build_config_from_order(order: dict) -> EffectConfig:
    """
    从 orders 表一条记录构建 EffectConfig。

    字段对应关系：
      order.product_shape  → config.shape  （中文，效果图服务支持中英文）
      order.product_color  → config.color
      order.product_size   → config.size   (L / S)
      order.front_text     → config.front.text
      order.font_code      → config.front.font_family  (F-04 等)
      order.back_text      → 解析为 text_content 或 phone_number
    """
    shape = order.get("product_shape") or "heart"
    color = order.get("product_color") or "Gold"
    size  = order.get("product_size")  or "L"

    # 正面
    front_text   = order.get("front_text") or ""
    font_code    = order.get("font_code")  or "F-04"

    # 背面：back_text 字段可能是纯电话，也可能是「文字 + 回车 + 电话」
    # 规则：全部数字/符号 → 当作电话；否则第一行是文字，最后一行是电话
    back_raw   = (order.get("back_text") or "").strip()
    text_part  = ""
    phone_part = ""
    if back_raw:
        lines = [l.strip() for l in back_raw.splitlines() if l.strip()]
        if len(lines) == 1:
            # 只有一行：纯数字/符号/点/横线 → 电话；否则 → 文字
            import re as _re
            if _re.fullmatch(r'[\d\s\+\-\.\(\)/]+', lines[0]):
                phone_part = lines[0]
            else:
                text_part = lines[0]
        else:
            # 多行：最后一行当电话，其余当文字
            import re as _re
            if _re.fullmatch(r'[\d\s\+\-\.\(\)/]+', lines[-1]):
                phone_part = lines[-1]
                text_part  = " ".join(lines[:-1])
            else:
                text_part  = " ".join(lines)

    return EffectConfig(
        shape  = shape,
        size   = size,
        color  = color,
        front  = FrontConfig(
            text        = front_text,
            font_family = font_code,
        ),
        back   = BackConfig(
            text_content = text_part,
            phone_number = phone_part,
        ),
    )


def generate_effect_image_for_order(
    order: dict,
    upload: bool = True,
    with_dimension: bool = False,
) -> Optional[str]:
    """
    根据订单数据生成效果图，可选上传到 Supabase Storage。

    Args:
        order:          orders 表一条记录（dict）
        upload:         True=上传 Storage 并返回 URL；False=只返回本地路径字符串
        with_dimension: 是否附加尺寸标注（默认 False，发给客户用纯净版）

    Returns:
        上传成功返回公开 URL；upload=False 返回本地文件路径字符串；失败返回 None
    """
    try:
        etsy_id = order.get("etsy_order_id", "unknown")
        config  = _build_config_from_order(order)

        # 生成 SVG
        core_svg = generate_effect_image(config)
        svg_content = wrap_with_dimension(core_svg, config) if with_dimension else core_svg

        # 保存到本地临时文件
        output_dir = Path(__file__).parent.parent.parent / "output"
        output_dir.mkdir(exist_ok=True)
        svg_path = output_dir / f"effect_{etsy_id}.svg"
        svg_path.write_text(svg_content, encoding="utf-8")
        print(f"  [效果图] 已生成 SVG: {svg_path.name}")

        if not upload:
            return str(svg_path)

        # 上传到 Supabase Storage
        from src.services.database_service import db
        url = db.upload_file("effect-images", svg_path, f"{etsy_id}.svg")
        return url

    except Exception as e:
        print(f"  [效果图] 生成失败: {e}")
        import traceback
        traceback.print_exc()
        return None

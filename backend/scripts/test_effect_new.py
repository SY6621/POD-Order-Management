# -*- coding: utf-8 -*-
"""
测试效果图生成 - 3种形状 × 大号
同时生成：纯净版（_core）和含标注版（_dim）
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.effect_template_service import (
    EffectConfig, FrontConfig, BackConfig,
    generate_effect_image, wrap_with_dimension, save_effect_image
)


def test_all_shapes():
    """测试3种形状的效果图生成"""

    cases = [
        {
            "label": "心形大号 玫瑰金",
            "config": EffectConfig(
                shape="心形", size="L", color="玫瑰金",
                front=FrontConfig(text="Alice", font_family="F-04"),
                back=BackConfig(
                    text_content="If Lost",
                    phone_number="13999926688",
                    layout_mode="text_top",
                ),
            ),
        },
        {
            "label": "圆形大号 金色",
            "config": EffectConfig(
                shape="圆形", size="L", color="金色",
                front=FrontConfig(text="Emma", font_family="F-04"),
                back=BackConfig(
                    text_content="Call Me",
                    phone_number="13800138000",
                    layout_mode="phone_top",
                ),
            ),
        },
        {
            "label": "骨头形大号 银色",
            "config": EffectConfig(
                shape="骨头形", size="L", color="银色",
                front=FrontConfig(text="Buddy", font_family="F-04"),
                back=BackConfig(
                    text_content="Lost Dog",
                    phone_number="13666666666",
                    layout_mode="text_top",
                ),
            ),
        },
    ]

    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)

    from datetime import datetime
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("=" * 60)
    print("效果图生成测试（V1.3 规范）")
    print("=" * 60)

    for case in cases:
        config = case["config"]
        print(f"\n生成：{case['label']}...")
        try:
            from src.services.effect_template_service import _resolve_shape
            shape = _resolve_shape(config.shape)

            # 纯净版（无标注）
            core_svg = generate_effect_image(config)
            core_path = output_dir / f"effect_{shape}_{config.size}_{config.color}_core_{ts}.svg"
            core_path.write_text(core_svg, encoding="utf-8")
            print(f"  ✅ 纯净版 → {core_path.name}")

            # 含标注版
            dim_svg  = wrap_with_dimension(core_svg, config)
            dim_path = output_dir / f"effect_{shape}_{config.size}_{config.color}_dim_{ts}.svg"
            dim_path.write_text(dim_svg, encoding="utf-8")
            print(f"  ✅ 标注版 → {dim_path.name}")

        except Exception as e:
            print(f"  ❌ 失败：{e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 60)
    print("输出目录：backend/output/")
    print("  _core = 纯净效果图（稳定出图）")
    print("  _dim  = 含尺寸标注版（预览用）")
    print("=" * 60)


if __name__ == "__main__":
    test_all_shapes()

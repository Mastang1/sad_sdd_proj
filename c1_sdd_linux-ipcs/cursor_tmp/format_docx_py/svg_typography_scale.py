# -*- coding: utf-8 -*-
"""
Per-SVG display width from viewBox + font-size so Word renders ~小四 (12pt) body text.

Does not modify SVG source files; only computes target width (cm) for Word extent scaling.
"""
from __future__ import annotations

import re
from collections import Counter

from svg_extent_utils import parse_svg_viewbox_wh, svg_diagram_type

# Calibrated against 3_3_1.svg: viewBox W=746, font-size 12, 14cm display ≈ readable 五号 (10.5pt)
_CALIB_BODY_PT = 10.5  # 五号（标定基准）
REF_VIEWBOX_W = 746.0
REF_WIDTH_CM = 14.0
REF_FONT_PX = 12.0
TARGET_BODY_PT = 12.0  # 小四（流程图 Word 内目标字号）

_FONT_SIZE_RE = re.compile(r'font-size="([\d.]+)"')


def dominant_body_font_size_px(svg_text: str) -> float:
    sizes = [float(x) for x in _FONT_SIZE_RE.findall(svg_text or "")]
    if not sizes:
        return REF_FONT_PX
    body = [s for s in sizes if s <= 13.0]
    pool = body or sizes
    return float(Counter(pool).most_common(1)[0][0])


def compute_typography_width_cm(viewbox_w: float, svg_font_px: float) -> float:
    if viewbox_w <= 0 or svg_font_px <= 0:
        return REF_WIDTH_CM * (TARGET_BODY_PT / _CALIB_BODY_PT)
    base = REF_WIDTH_CM * (viewbox_w / REF_VIEWBOX_W) * (REF_FONT_PX / svg_font_px)
    return base * (TARGET_BODY_PT / _CALIB_BODY_PT)


def target_width_cm_for_flow_svg(svg_text: str) -> float | None:
    """
    Return target display width (cm) for ACTIVITY (processing flow) SVGs only.
    """
    if svg_diagram_type(svg_text) != "ACTIVITY":
        return None
    wh = parse_svg_viewbox_wh(svg_text)
    if wh is None:
        return None
    viewbox_w, _viewbox_h = wh
    font_px = dominant_body_font_size_px(svg_text)
    return compute_typography_width_cm(viewbox_w, font_px)


def estimate_body_font_pt(display_width_cm: float, viewbox_w: float, svg_font_px: float) -> float:
    """Rough effective body font size (pt) after Word scaling."""
    if viewbox_w <= 0 or display_width_cm <= 0:
        return 0.0
    # PlantUML font-size uses viewBox user units; scale linearly with display width.
    font_cm = svg_font_px * (display_width_cm / viewbox_w)
    return font_cm * (72.0 / 2.54)

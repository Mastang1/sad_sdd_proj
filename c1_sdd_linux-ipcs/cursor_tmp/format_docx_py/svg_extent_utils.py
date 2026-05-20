# -*- coding: utf-8 -*-
"""从 DOCX 内嵌 SVG 读取 viewBox，修正 Pandoc 默认 extent 导致的宽高比错误。"""
from __future__ import annotations

import re
from typing import TYPE_CHECKING

from docx.oxml.ns import qn

if TYPE_CHECKING:
    from docx.document import Document

_SVG_BLIP_NS = "http://schemas.microsoft.com/office/drawing/2016/SVG/main"

_VIEWBOX_RE = re.compile(
    r'viewBox="\s*0\s+0\s+([\d.]+)\s+([\d.]+)\s*"', re.IGNORECASE
)


def parse_svg_viewbox_wh(svg_text: str) -> tuple[float, float] | None:
    """解析 SVG ``viewBox="0 0 W H"``，返回 (W, H)。"""
    m = _VIEWBOX_RE.search(svg_text or "")
    if not m:
        return None
    w, h = float(m.group(1)), float(m.group(2))
    if w <= 0 or h <= 0:
        return None
    return w, h


def _inline_blip_rid(inline_el) -> str | None:
    blip = inline_el.find(".//" + qn("a:blip"))
    if blip is None:
        return None
    svg_blip = blip.find(f".//{{{_SVG_BLIP_NS}}}svgBlip")
    if svg_blip is not None:
        rid = svg_blip.get(qn("r:embed"))
        if rid:
            return rid
    return blip.get(qn("r:embed"))


def _svg_text_from_inline(inline_el, document: Document) -> str | None:
    rid = _inline_blip_rid(inline_el)
    if not rid:
        return None
    part = document.part.related_parts.get(rid)
    if part is None:
        return None
    try:
        return part.blob.decode("utf-8")
    except (UnicodeDecodeError, AttributeError):
        return None


def svg_aspect_ratio_from_inline(inline_el, document: Document) -> float | None:
    """内嵌 SVG 的高宽比 cy/cx = viewBox H / W。"""
    svg = _svg_text_from_inline(inline_el, document)
    if not svg:
        return None
    wh = parse_svg_viewbox_wh(svg)
    if wh is None:
        return None
    w, h = wh
    return h / w


def read_inline_natural_extent(inline_el, document: Document | None = None) -> tuple[int, int]:
    """
    插图原始显示尺寸（EMU）。

    优先用内嵌 SVG ``viewBox`` 与 ``wp:extent.cx`` 计算高度，修正 Pandoc 对时序图等
    误设 3810000×2540000（cy/cx=2/3）的默认 extent。
    """
    ext_el = inline_el.find(qn("wp:extent"))
    cx = cy = 0
    if ext_el is not None:
        cx = int(ext_el.get("cx") or 0)
        cy = int(ext_el.get("cy") or 0)

    if document is not None and cx > 0:
        aspect = svg_aspect_ratio_from_inline(inline_el, document)
        if aspect is not None and aspect > 0:
            fixed_cy = int(round(cx * aspect))
            if fixed_cy > 0:
                return cx, fixed_cy

    if cx > 0 and cy > 0:
        return cx, cy

    from docx.text.run import InlineShape

    shape = InlineShape(inline_el)
    return int(shape.width), int(shape.height)

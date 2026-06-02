# -*- coding: utf-8 -*-
"""
按 viewBox + font-size 为 ACTIVITY（processing flow）流程图单独设 Word 显示宽度，
使 Word 中正文约 **五号（10.5pt）**；不修改 SVG 源文件。

管线 C（``md0519_to_final_sdd.py``）在表格适应窗口之后自动调用 ``apply_flow_typography_scale``。

单独补跑（已生成的 ``final_sdd.docx``）::

    python cursor_tmp/format_docx_py/scale_flow_diagram_typography.py
    python cursor_tmp/format_docx_py/scale_flow_diagram_typography.py path/to.docx
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_CURSOR_TMP = _SCRIPT_DIR.parent
if str(_CURSOR_TMP) not in sys.path:
    sys.path.insert(0, str(_CURSOR_TMP))
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from workspace_paths import FINAL_SDD_DOCX

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Cm
from docx.shape import InlineShape

from format_final_sdd import (
    _EMU_PER_CM,
    _apply_shape_extents,
    _compute_target_extents,
    _iter_body_paragraphs_in_order,
    _max_printable_box_emu,
    _read_inline_natural_extent,
)
from svg_extent_utils import parse_svg_viewbox_wh, svg_text_from_inline
from svg_typography_scale import (
    dominant_body_font_size_px,
    estimate_body_font_pt,
    target_width_cm_for_flow_svg,
)

DEFAULT_DOCX = FINAL_SDD_DOCX
REPORT_PATH = _CURSOR_TMP / "flow_typography_scale_report.txt"


def apply_flow_typography_scale(docx_path: Path) -> tuple[int, int, list[dict]]:
    doc = Document(str(docx_path))
    max_cx, max_cy = _max_printable_box_emu(doc)
    wp_inline = qn("wp:inline")
    scaled = 0
    skipped = 0
    reports: list[dict] = []

    for p_el in _iter_body_paragraphs_in_order(doc.element.body):
        for inline_el in p_el.findall(".//" + wp_inline):
            svg = svg_text_from_inline(inline_el, doc)
            if not svg:
                skipped += 1
                continue
            target_cm = target_width_cm_for_flow_svg(svg)
            if target_cm is None:
                skipped += 1
                continue

            shape = InlineShape(inline_el)
            oc, oh = _read_inline_natural_extent(inline_el, doc)
            if oc <= 0 or oh <= 0:
                skipped += 1
                continue

            before_cx, before_cy = int(shape.width), int(shape.height)
            wanted_emu = int(Cm(target_cm))
            exp_cx, exp_cy = _compute_target_extents(oc, oh, wanted_emu, max_cx, max_cy)
            _apply_shape_extents(shape, exp_cx, exp_cy)
            scaled += 1

            wh = parse_svg_viewbox_wh(svg) or (0.0, 0.0)
            font_px = dominant_body_font_size_px(svg)
            after_w_cm = exp_cx / _EMU_PER_CM
            after_h_cm = exp_cy / _EMU_PER_CM
            reports.append(
                {
                    "index": scaled,
                    "viewbox_w": wh[0],
                    "viewbox_h": wh[1],
                    "svg_font_px": font_px,
                    "target_cm": round(target_cm, 3),
                    "before_cm_w": round(before_cx / _EMU_PER_CM, 3),
                    "after_cm_w": round(after_w_cm, 3),
                    "after_cm_h": round(after_h_cm, 3),
                    "est_body_pt": round(
                        estimate_body_font_pt(after_w_cm, wh[0], font_px), 2
                    ),
                    "height_limited": exp_cx < wanted_emu
                    or exp_cy < int(round(wanted_emu * oh / oc)),
                }
            )

    doc.save(str(docx_path))
    return scaled, skipped, reports


def write_report(path: Path, docx_path: Path, scaled: int, skipped: int, reports: list[dict]) -> None:
    lines = [
        f"docx: {docx_path}",
        f"ACTIVITY flow diagrams scaled: {scaled}",
        f"inline images skipped (non-ACTIVITY / no SVG): {skipped}",
        "",
    ]
    if reports:
        pts = [r["est_body_pt"] for r in reports]
        lines.append(f"estimated body pt: min={min(pts):.2f} max={max(pts):.2f} avg={sum(pts)/len(pts):.2f}")
        lines.append("")
        lines.append("index\tviewBox_W\ttarget_cm\tafter_cm_w\tafter_cm_h\test_pt\theight_limited")
        for r in reports:
            lines.append(
                f"{r['index']}\t{r['viewbox_w']:.0f}\t{r['target_cm']}\t{r['after_cm_w']}\t"
                f"{r['after_cm_h']}\t{r['est_body_pt']}\t{r['height_limited']}"
            )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Scale ACTIVITY flow SVGs by typography width.")
    parser.add_argument(
        "--docx",
        type=Path,
        default=DEFAULT_DOCX,
        help="Target DOCX (default: final_sdd.docx)",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=REPORT_PATH,
        help="Report output path",
    )
    args = parser.parse_args()
    docx = args.docx.resolve()
    if not docx.is_file():
        print(f"Missing: {docx}", file=sys.stderr)
        return 1

    scaled, skipped, reports = apply_flow_typography_scale(docx)
    write_report(args.report.resolve(), docx, scaled, skipped, reports)
    print(f"Scaled {scaled} ACTIVITY diagram(s); skipped {skipped} inline image(s)")
    print(f"Report: {args.report.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

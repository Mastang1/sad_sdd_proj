# -*- coding: utf-8 -*-
"""
将 ``fuck.docx`` 中 ACTIVITY 流程图 EMF 替换为 ``cursor_tmp/flow_svgs`` 对应 SVG，
保留 Word 显示宽度并按 SVG viewBox 调整高度；其它插图不动。

用法::

    python cursor_tmp/format_docx_py/replace_flow_emf_with_svg.py
    python cursor_tmp/format_docx_py/replace_flow_emf_with_svg.py fuck.docx --dry-run
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_CURSOR_TMP = _SCRIPT_DIR.parent
if str(_CURSOR_TMP) not in sys.path:
    sys.path.insert(0, str(_CURSOR_TMP))
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from docx import Document
from flow_diagram_image_replace import (
    FlowInlineRecord,
    collect_emf_flow_inlines,
    display_extent_from_svg_file,
    list_activity_flow_svg_paths,
    replace_inline_with_svg,
)
from workspace_paths import (
    EMF_EXTENT_REPORT,
    FLOW_EMF,
    FUCK_DOCX,
    MD_SDD_0519,
    WORKSPACE_ROOT,
)

REPORT_PATH = _CURSOR_TMP / "flow_emf_to_svg_report.txt"
EMF_SVG_SRC = FLOW_EMF / "_svg_src"


def write_report(
    path: Path,
    docx_path: Path,
    rows: list[tuple[FlowInlineRecord, Path, int, int]],
) -> None:
    lines = [
        f"docx: {docx_path}",
        f"replaced: {len(rows)}",
        "",
        "index\tsvg\tcx_emu\tcy_emu\tcy_old\tviewbox_w\tviewbox_h",
    ]
    for rec, svg_path, cx, cy in rows:
        from svg_extent_utils import parse_svg_viewbox_wh

        wh = parse_svg_viewbox_wh(svg_path.read_text(encoding="utf-8")) or (0, 0)
        lines.append(
            f"{rec.index}\t{svg_path.name}\t{cx}\t{cy}\t{rec.cy}\t{wh[0]}\t{wh[1]}"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def apply_emf_to_svg(
    docx_path: Path,
    *,
    md_path: Path = MD_SDD_0519,
    report_path: Path = REPORT_PATH,
    dry_run: bool = False,
) -> tuple[int, int]:
    if docx_path.resolve().name.lower() != "fuck.docx":
        sys.exit("[ERROR] 本脚本仅允许操作 fuck.docx")

    svg_paths = list_activity_flow_svg_paths(md_path, workspace_root=WORKSPACE_ROOT)
    doc = Document(str(docx_path))
    records = collect_emf_flow_inlines(
        doc,
        emf_report_path=EMF_EXTENT_REPORT,
        svg_src_dirs=[EMF_SVG_SRC],
    )
    if not records:
        sys.exit("[ERROR] 未发现 EMF ACTIVITY 流程图 inline。")

    if len(svg_paths) != len(records):
        sys.exit(
            f"[ERROR] SVG 数量 {len(svg_paths)} 与 EMF inline {len(records)} 不一致"
        )

    print(f"[info] EMF flow inlines: {len(records)}")
    if dry_run:
        rows = []
        for rec, svg_path in zip(records, svg_paths):
            cx, cy = display_extent_from_svg_file(svg_path, rec.cx, rec.cy)
            rows.append((rec, svg_path, cx, cy))
        write_report(report_path, docx_path, rows)
        return 0, len(records)

    replaced_rows: list[tuple[FlowInlineRecord, Path, int, int]] = []
    for rec, svg_path in zip(records, svg_paths):
        cx, cy = display_extent_from_svg_file(svg_path, rec.cx, rec.cy)
        replace_inline_with_svg(rec.inline_el, doc, svg_path, cx, cy)
        replaced_rows.append((rec, svg_path, cx, cy))

    doc.save(str(docx_path))
    write_report(report_path, docx_path, replaced_rows)
    return len(replaced_rows), len(records)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Replace ACTIVITY EMF inlines with SVG (fuck.docx only)."
    )
    ap.add_argument("docx", nargs="?", type=Path, default=FUCK_DOCX)
    ap.add_argument("--report", type=Path, default=REPORT_PATH)
    ap.add_argument("--md", type=Path, default=MD_SDD_0519)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    docx = args.docx.resolve()
    if not docx.is_file():
        print(f"Missing: {docx}", file=sys.stderr)
        return 1

    t0 = time.time()
    replaced, total = apply_emf_to_svg(
        docx,
        md_path=args.md.resolve(),
        report_path=args.report.resolve(),
        dry_run=args.dry_run,
    )
    elapsed = time.time() - t0
    print(f"[done] replaced {replaced}/{total} EMF → SVG in {elapsed:.1f}s")
    print(f"[info] Report: {args.report.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

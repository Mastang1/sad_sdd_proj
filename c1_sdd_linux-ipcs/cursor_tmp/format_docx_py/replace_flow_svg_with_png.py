# -*- coding: utf-8 -*-
"""
将 ``final_sdd.docx`` 中 ACTIVITY（processing flow）内联图转为 PNG（200–300 DPI）并回写，
保留 Word ``wp:extent`` 显示尺寸；其它插图不动。

1. 记录每张 ACTIVITY 图的 cx/cy（EMU）；
2. 内嵌 SVG 缓存到 ``cursor_tmp/flow_png/_svg_src/{id}.svg``；
3. 按显示尺寸 × DPI 栅格化为 ``cursor_tmp/flow_png/{id}.png``（默认 300 DPI）；
4. 替换内联 blip 为 PNG，extent 不变。

支持输入态：内联 SVG（ACTIVITY），或此前 EMF 替换后的 ``flow_*.emf``（需
``cursor_tmp/flow_svg_to_emf_report.txt`` + ``flow_emf/_svg_src``）。

用法::

    python cursor_tmp/format_docx_py/replace_flow_svg_with_png.py
    python cursor_tmp/format_docx_py/replace_flow_svg_with_png.py final_sdd.docx --dpi 300
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

import cairosvg
from docx import Document
from flow_diagram_image_replace import (
    FlowInlineRecord,
    collect_activity_flow_inlines,
    replace_inline_blip_image,
)
from workspace_paths import EMF_EXTENT_REPORT, FINAL_SDD_DOCX, FLOW_EMF, FLOW_PNG, PNG_EXTENT_REPORT

_EMU_PER_INCH = 914400
REPORT_PATH = _CURSOR_TMP / "flow_svg_to_png_report.txt"
SVG_SRC_DIR = FLOW_PNG / "_svg_src"
EMF_SVG_SRC = FLOW_EMF / "_svg_src"


def png_pixel_size(cx: int, cy: int, dpi: int) -> tuple[int, int]:
    px_w = max(1, round(cx / _EMU_PER_INCH * dpi))
    px_h = max(1, round(cy / _EMU_PER_INCH * dpi))
    return px_w, px_h


def load_existing_png_map(records: list[FlowInlineRecord]) -> dict[str, Path]:
    out: dict[str, Path] = {}
    missing: list[str] = []
    for rec in records:
        if rec.content_id in out:
            continue
        png_path = FLOW_PNG / f"{rec.content_id}.png"
        if png_path.is_file():
            out[rec.content_id] = png_path
        else:
            missing.append(rec.content_id)
    if missing:
        sys.exit(
            f"[ERROR] --replace-only: 缺少 {len(missing)} 个 PNG，"
            f"例如 {missing[:5]}"
        )
    return out


def ensure_png_for_content(
    records: list[FlowInlineRecord],
    *,
    dpi: int,
    force: bool = False,
    replace_only: bool = False,
) -> dict[str, Path]:
    if replace_only:
        return load_existing_png_map(records)

    id_meta: dict[str, tuple[int, int, str]] = {}
    for rec in records:
        if rec.content_id not in id_meta:
            id_meta[rec.content_id] = (rec.cx, rec.cy, rec.svg_text)

    SVG_SRC_DIR.mkdir(parents=True, exist_ok=True)
    FLOW_PNG.mkdir(parents=True, exist_ok=True)
    out: dict[str, Path] = {}

    for cid, (_cx, _cy, svg_text) in id_meta.items():
        svg_path = SVG_SRC_DIR / f"{cid}.svg"
        png_path = FLOW_PNG / f"{cid}.png"
        if not svg_path.is_file() or force:
            svg_path.write_text(svg_text, encoding="utf-8")

        if (
            not force
            and png_path.is_file()
            and png_path.stat().st_mtime >= svg_path.stat().st_mtime
        ):
            out[cid] = png_path
            continue

        cx, cy = id_meta[cid][0], id_meta[cid][1]
        px_w, px_h = png_pixel_size(cx, cy, dpi)
        cairosvg.svg2png(
            url=str(svg_path.resolve()),
            write_to=str(png_path.resolve()),
            output_width=px_w,
            output_height=px_h,
        )
        out[cid] = png_path
    return out


def write_report(
    path: Path,
    docx_path: Path,
    records: list[FlowInlineRecord],
    replaced: int,
    unique_png: int,
    dpi: int,
) -> None:
    lines = [
        f"docx: {docx_path}",
        f"dpi: {dpi}",
        f"activity flow inlines: {len(records)}",
        f"unique content ids (PNG files): {unique_png}",
        f"replaced with PNG: {replaced}",
        f"png_dir: {FLOW_PNG}",
        f"svg_cache: {SVG_SRC_DIR}",
        "",
        "index\tcontent_id\tcx_emu\tcy_emu\twidth_cm\theight_cm\tpx_w\tpx_h\tpng",
    ]
    for r in records:
        px_w, px_h = png_pixel_size(r.cx, r.cy, dpi)
        lines.append(
            f"{r.index}\t{r.content_id}\t{r.cx}\t{r.cy}\t{r.cx_cm}\t{r.cy_cm}\t"
            f"{px_w}\t{px_h}\t{r.content_id}.png"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def apply_flow_diagrams_to_png(
    docx_path: Path,
    *,
    dpi: int = 300,
    report_path: Path = REPORT_PATH,
    force_png: bool = False,
    replace_only: bool = False,
    dry_run: bool = False,
) -> tuple[int, int, int]:
    if dpi < 200 or dpi > 300:
        sys.exit("[ERROR] --dpi 须在 200–300 之间")

    doc = Document(str(docx_path))
    records = collect_activity_flow_inlines(
        doc,
        emf_report_path=EMF_EXTENT_REPORT,
        png_report_path=PNG_EXTENT_REPORT,
        svg_src_dirs=[SVG_SRC_DIR, EMF_SVG_SRC],
    )
    if not records:
        sys.exit(
            "[ERROR] 未发现 ACTIVITY 流程图（SVG 或 flow_*.emf）。"
            " 若 docx 已栅格化 PNG 则无需重复执行。"
        )

    unique_ids = len({r.content_id for r in records})
    print(
        f"[info] ACTIVITY flow inlines: {len(records)} "
        f"({unique_ids} unique), dpi={dpi}"
    )

    if dry_run:
        write_report(report_path, docx_path, records, 0, unique_ids, dpi)
        return 0, len(records), unique_ids

    if replace_only:
        print("[info] --replace-only: 使用已有 PNG，不栅格化")

    png_map = ensure_png_for_content(
        records, dpi=dpi, force=force_png, replace_only=replace_only
    )

    replaced = 0
    for rec in records:
        replace_inline_blip_image(
            rec.inline_el, doc, png_map[rec.content_id], rec.cx, rec.cy
        )
        replaced += 1

    doc.save(str(docx_path))
    write_report(report_path, docx_path, records, replaced, unique_ids, dpi)
    return replaced, len(records), unique_ids


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Replace ACTIVITY flow SVG/EMF with PNG (preserve Word extents)."
    )
    ap.add_argument("docx", nargs="?", type=Path, default=FINAL_SDD_DOCX)
    ap.add_argument("--dpi", type=int, default=300, help="200–300, default 300")
    ap.add_argument("--report", type=Path, default=REPORT_PATH)
    ap.add_argument("--force-png", action="store_true", help="强制重栅格化 PNG")
    ap.add_argument(
        "--replace-only",
        action="store_true",
        help="仅替换 DOCX 内联图，使用 flow_png 已有 PNG，不调用 CairoSVG",
    )
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    docx = args.docx.resolve()
    if not docx.is_file():
        print(f"Missing: {docx}", file=sys.stderr)
        return 1

    t0 = time.time()
    replaced, total, unique = apply_flow_diagrams_to_png(
        docx,
        dpi=args.dpi,
        report_path=args.report.resolve(),
        force_png=args.force_png,
        replace_only=args.replace_only,
        dry_run=args.dry_run,
    )
    elapsed = time.time() - t0
    print(
        f"[done] replaced {replaced}/{total} ACTIVITY → PNG "
        f"({unique} unique @ {args.dpi}dpi) in {elapsed:.1f}s"
    )
    print(f"[info] PNG dir: {FLOW_PNG}")
    print(f"[info] Report: {args.report.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

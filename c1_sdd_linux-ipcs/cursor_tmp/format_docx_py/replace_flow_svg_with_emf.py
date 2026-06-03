# -*- coding: utf-8 -*-
"""
将 ``final_sdd.docx`` 中 ACTIVITY（processing flow）内联图替换为 EMF，
保留 Word ``wp:extent`` 显示尺寸；其它插图不动。

EMF 真源：``cursor_tmp/flow_emf/{content_id}.emf``（经 Inkscape 从 SVG 导出）。

用法::

    python cursor_tmp/format_docx_py/replace_flow_svg_with_emf.py final_sdd.docx --force-emf
    python cursor_tmp/format_docx_py/replace_flow_svg_with_emf.py final_sdd.docx --replace-only
    python cursor_tmp/format_docx_py/replace_flow_svg_with_emf.py final_sdd.docx --dry-run
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
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
    collect_activity_flow_inlines,
    replace_inline_with_emf,
)
from workspace_paths import (
    EMF_EXTENT_REPORT,
    FINAL_SDD_DOCX,
    FLOW_EMF,
    FLOW_PNG,
    PNG_EXTENT_REPORT,
)

REPORT_PATH = _CURSOR_TMP / "flow_svg_to_emf_report.txt"
SVG_SRC_DIR = FLOW_EMF / "_svg_src"
PNG_SVG_SRC = FLOW_PNG / "_svg_src"
_EMU_PER_INCH = 914400
_DEFAULT_INKSCAPE_PATHS = (
    Path(r"C:\Program Files\Inkscape\bin\inkscape.exe"),
    Path(r"C:\Program Files\Inkscape 1.4\bin\inkscape.exe"),
)


def find_inkscape(explicit: Path | None = None) -> Path:
    if explicit is not None:
        p = explicit.expanduser().resolve()
        if p.is_file():
            return p
        raise FileNotFoundError(f"Inkscape not found: {p}")

    env = os.environ.get("INKSCAPE")
    if env:
        p = Path(env).expanduser().resolve()
        if p.is_file():
            return p

    which = shutil.which("inkscape")
    if which:
        return Path(which).resolve()

    for candidate in _DEFAULT_INKSCAPE_PATHS:
        if candidate.is_file():
            return candidate

    raise FileNotFoundError(
        "Inkscape not found. Install Inkscape or set INKSCAPE / pass --inkscape."
    )


def _extent_to_export_px(cx: int, cy: int, dpi: int = 96) -> tuple[int, int]:
    px_w = max(1, round(cx / _EMU_PER_INCH * dpi))
    px_h = max(1, round(cy / _EMU_PER_INCH * dpi))
    return px_w, px_h


def export_svg_to_emf(
    inkscape: Path,
    svg_path: Path,
    emf_path: Path,
    *,
    cx: int,
    cy: int,
) -> None:
    emf_path.parent.mkdir(parents=True, exist_ok=True)
    px_w, px_h = _extent_to_export_px(cx, cy)
    cmd = [
        str(inkscape),
        str(svg_path.resolve()),
        "--export-type=emf",
        f"--export-filename={emf_path.resolve()}",
        f"--export-width={px_w}",
        f"--export-height={px_h}",
    ]
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip()
        raise RuntimeError(f"Inkscape failed ({svg_path.name}): {err}")
    if not emf_path.is_file() or emf_path.stat().st_size == 0:
        raise RuntimeError(f"Inkscape produced no EMF: {emf_path}")


def export_emf_batch(
    records: list[FlowInlineRecord],
    *,
    inkscape: Path,
    force: bool = False,
) -> dict[str, Path]:
    id_meta: dict[str, tuple[int, int, str]] = {}
    for rec in records:
        if rec.content_id not in id_meta:
            text = rec.svg_text
            if not text:
                for d in (SVG_SRC_DIR, PNG_SVG_SRC):
                    p = d / f"{rec.content_id}.svg"
                    if p.is_file():
                        text = p.read_text(encoding="utf-8")
                        break
            if not text:
                raise FileNotFoundError(
                    f"SVG source missing for content_id={rec.content_id}"
                )
            id_meta[rec.content_id] = (rec.cx, rec.cy, text)

    SVG_SRC_DIR.mkdir(parents=True, exist_ok=True)
    FLOW_EMF.mkdir(parents=True, exist_ok=True)
    out: dict[str, Path] = {}
    pending: list[tuple[str, Path, Path, int, int]] = []

    for cid, (cx, cy, svg_text) in id_meta.items():
        svg_path = SVG_SRC_DIR / f"{cid}.svg"
        emf_path = FLOW_EMF / f"{cid}.emf"
        if not svg_path.is_file() or force:
            svg_path.write_text(svg_text, encoding="utf-8")
        if (
            not force
            and emf_path.is_file()
            and emf_path.stat().st_mtime >= svg_path.stat().st_mtime
        ):
            out[cid] = emf_path
            continue
        pending.append((cid, svg_path, emf_path, cx, cy))

    if pending:
        print(f"[info] Exporting {len(pending)} EMF via Inkscape ({inkscape})...")
        for i, (cid, svg_path, emf_path, cx, cy) in enumerate(pending, 1):
            export_svg_to_emf(inkscape, svg_path, emf_path, cx=cx, cy=cy)
            out[cid] = emf_path
            if i % 20 == 0 or i == len(pending):
                print(f"[info]   {i}/{len(pending)} EMF exported")
    return out


def load_existing_emf_map(records: list[FlowInlineRecord]) -> dict[str, Path]:
    out: dict[str, Path] = {}
    missing: list[str] = []
    for rec in records:
        if rec.content_id in out:
            continue
        emf_path = FLOW_EMF / f"{rec.content_id}.emf"
        if emf_path.is_file():
            out[rec.content_id] = emf_path
        else:
            missing.append(rec.content_id)
    if missing:
        sys.exit(
            f"[ERROR] --replace-only: 缺少 {len(missing)} 个 EMF，"
            f"例如 {missing[:5]}"
        )
    return out


def ensure_emf_for_content(
    records: list[FlowInlineRecord],
    *,
    inkscape: Path,
    force: bool = False,
    replace_only: bool = False,
) -> dict[str, Path]:
    if replace_only:
        return load_existing_emf_map(records)

    return export_emf_batch(records, inkscape=inkscape, force=force)


def write_report(
    path: Path,
    docx_path: Path,
    records: list[FlowInlineRecord],
    replaced: int,
    unique_emf: int,
) -> None:
    lines = [
        f"docx: {docx_path}",
        f"activity flow inlines: {len(records)}",
        f"unique content ids (EMF files): {unique_emf}",
        f"replaced with EMF: {replaced}",
        f"emf_dir: {FLOW_EMF}",
        f"svg_cache: {SVG_SRC_DIR}",
        "",
        "index\tcontent_id\tcx_emu\tcy_emu\twidth_cm\theight_cm\temf",
    ]
    for r in records:
        lines.append(
            f"{r.index}\t{r.content_id}\t{r.cx}\t{r.cy}\t{r.cx_cm}\t{r.cy_cm}\t"
            f"{r.content_id}.emf"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def apply_flow_diagrams_to_emf(
    docx_path: Path,
    *,
    inkscape: Path,
    report_path: Path = REPORT_PATH,
    force_emf: bool = False,
    replace_only: bool = False,
    dry_run: bool = False,
) -> tuple[int, int, int]:
    doc = Document(str(docx_path))
    records = collect_activity_flow_inlines(
        doc,
        emf_report_path=EMF_EXTENT_REPORT,
        png_report_path=PNG_EXTENT_REPORT,
        svg_src_dirs=[SVG_SRC_DIR, PNG_SVG_SRC],
    )
    if not records:
        sys.exit(
            "[ERROR] 未发现 ACTIVITY 流程图（SVG / PNG / EMF）。"
            " 若已全部替换为 EMF 则无需重复执行。"
        )

    unique_ids = len({r.content_id for r in records})
    print(f"[info] ACTIVITY flow inlines: {len(records)} ({unique_ids} unique)")

    if dry_run:
        write_report(report_path, docx_path, records, 0, unique_ids)
        return 0, len(records), unique_ids

    if replace_only:
        print("[info] --replace-only: 使用 flow_emf 已有 EMF，不重新生成")

    emf_map = ensure_emf_for_content(
        records,
        inkscape=inkscape,
        force=force_emf,
        replace_only=replace_only,
    )

    replaced = 0
    for rec in records:
        replace_inline_with_emf(
            rec.inline_el, doc, emf_map[rec.content_id], rec.cx, rec.cy
        )
        replaced += 1

    doc.save(str(docx_path))
    write_report(report_path, docx_path, records, replaced, unique_ids)
    return replaced, len(records), unique_ids


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Replace ACTIVITY flow inlines with EMF (preserve Word extents)."
    )
    ap.add_argument("docx", nargs="?", type=Path, default=FINAL_SDD_DOCX)
    ap.add_argument("--report", type=Path, default=REPORT_PATH)
    ap.add_argument(
        "--force-emf",
        action="store_true",
        help="强制经 Inkscape 重导 EMF",
    )
    ap.add_argument(
        "--replace-only",
        action="store_true",
        help="仅插入 flow_emf 已有 EMF，不调用 Inkscape",
    )
    ap.add_argument(
        "--inkscape",
        type=Path,
        default=None,
        help="Inkscape 可执行文件路径（默认自动查找）",
    )
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    docx = args.docx.resolve()
    if not docx.is_file():
        print(f"Missing: {docx}", file=sys.stderr)
        return 1

    try:
        inkscape = find_inkscape(args.inkscape)
    except FileNotFoundError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

    t0 = time.time()
    replaced, total, unique = apply_flow_diagrams_to_emf(
        docx,
        inkscape=inkscape,
        report_path=args.report.resolve(),
        force_emf=args.force_emf,
        replace_only=args.replace_only,
        dry_run=args.dry_run,
    )
    elapsed = time.time() - t0
    print(
        f"[done] replaced {replaced}/{total} ACTIVITY → EMF "
        f"({unique} unique files) in {elapsed:.1f}s"
    )
    print(f"[info] EMF dir: {FLOW_EMF}")
    print(f"[info] Report: {args.report.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

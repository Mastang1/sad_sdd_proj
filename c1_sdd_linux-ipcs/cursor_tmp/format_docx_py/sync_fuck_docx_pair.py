# -*- coding: utf-8 -*-
"""
维护 ``fuck.docx``（EMF 流程图，供 Word 编辑）与 ``fuck_svg.docx``（SVG 流程图）成对交付。

| 文件 | 流程图格式 | 用途 |
|------|------------|------|
| ``fuck.docx`` | EMF | 用户版式编辑（Word 可稳定保存） |
| ``fuck_svg.docx`` | SVG | 校验 / PDF / 与 MD 插图一致 |

用法（工作区根目录）::

    python cursor_tmp/format_docx_py/sync_fuck_docx_pair.py
    python cursor_tmp/format_docx_py/sync_fuck_docx_pair.py --emf-only
    python cursor_tmp/format_docx_py/sync_fuck_docx_pair.py --svg-only
    python cursor_tmp/format_docx_py/update_fuck_svg_docx.py
"""
from __future__ import annotations

import argparse
import shutil
import sys
import time
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_CURSOR_TMP = _SCRIPT_DIR.parent
if str(_CURSOR_TMP) not in sys.path:
    sys.path.insert(0, str(_CURSOR_TMP))
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from replace_flow_emf_with_svg import apply_emf_to_svg
from replace_flow_svg_with_emf import (
    apply_flow_diagrams_to_emf,
    find_inkscape,
)
from workspace_paths import FUCK_DOCX, FUCK_SVG_DOCX

FUCK_EMF_REPORT = _CURSOR_TMP / "fuck_flow_svg_to_emf_report.txt"
FUCK_SVG_REPORT = _CURSOR_TMP / "fuck_flow_emf_to_svg_report.txt"


def apply_emf_to_fuck_docx(
    *,
    force_emf: bool = False,
    replace_only: bool = False,
    dry_run: bool = False,
) -> tuple[int, int, int]:
    if not FUCK_DOCX.is_file():
        sys.exit(f"[ERROR] Missing {FUCK_DOCX}")

    inkscape = find_inkscape(None)
    return apply_flow_diagrams_to_emf(
        FUCK_DOCX.resolve(),
        inkscape=inkscape,
        report_path=FUCK_EMF_REPORT,
        force_emf=force_emf,
        replace_only=replace_only,
        dry_run=dry_run,
    )


def update_fuck_svg_docx(*, dry_run: bool = False) -> tuple[int, int]:
    """Delete ``fuck_svg.docx``, copy ``fuck.docx``, replace EMF → SVG."""
    if not FUCK_DOCX.is_file():
        sys.exit(f"[ERROR] Missing {FUCK_DOCX}")

    if dry_run:
        print(f"[dry-run] would delete {FUCK_SVG_DOCX.name} if exists")
        print(f"[dry-run] would copy {FUCK_DOCX.name} → {FUCK_SVG_DOCX.name}")
        print("[dry-run] would replace EMF → SVG on fuck_svg.docx")
        return 0, 0

    if FUCK_SVG_DOCX.exists():
        print(f"[info] Deleting {FUCK_SVG_DOCX.name}")
        FUCK_SVG_DOCX.unlink()

    print(f"[info] Copy {FUCK_DOCX.name} → {FUCK_SVG_DOCX.name}")
    shutil.copy2(FUCK_DOCX, FUCK_SVG_DOCX)

    return apply_emf_to_svg(FUCK_SVG_DOCX, report_path=FUCK_SVG_REPORT)


def sync_pair(
    *,
    emf_only: bool = False,
    svg_only: bool = False,
    force_emf: bool = False,
    replace_only: bool = False,
    dry_run: bool = False,
) -> None:
    t0 = time.time()

    if not svg_only:
        print("[step 1] ACTIVITY 流程图 → EMF on fuck.docx")
        replaced, total, unique = apply_emf_to_fuck_docx(
            force_emf=force_emf,
            replace_only=replace_only,
            dry_run=dry_run,
        )
        print(
            f"[done] fuck.docx EMF: {replaced}/{total} "
            f"({unique} unique) report={FUCK_EMF_REPORT.name}"
        )

    if not emf_only:
        print("[step 2] copy fuck.docx → fuck_svg.docx + EMF → SVG")
        replaced, total = update_fuck_svg_docx(dry_run=dry_run)
        print(
            f"[done] fuck_svg.docx SVG: {replaced}/{total} "
            f"report={FUCK_SVG_REPORT.name}"
        )

    print(f"[info] elapsed {time.time() - t0:.1f}s")


def main() -> int:
    ap = argparse.ArgumentParser(description="Sync fuck.docx (EMF) and fuck_svg.docx (SVG).")
    ap.add_argument("--emf-only", action="store_true", help="仅刷新 fuck.docx EMF")
    ap.add_argument("--svg-only", action="store_true", help="仅从 fuck.docx 更新 fuck_svg.docx")
    ap.add_argument(
        "--force-emf",
        action="store_true",
        help="强制 Inkscape 重导 EMF（否则优先 flow_emf 缓存）",
    )
    ap.add_argument(
        "--replace-only",
        action="store_true",
        help="EMF 步仅插入 flow_emf 已有文件，不调用 Inkscape",
    )
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.emf_only and args.svg_only:
        ap.error("--emf-only 与 --svg-only 不可同时使用")

    sync_pair(
        emf_only=args.emf_only,
        svg_only=args.svg_only,
        force_emf=args.force_emf,
        replace_only=args.replace_only,
        dry_run=args.dry_run,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# -*- coding: utf-8 -*-
"""
用户编辑 ``fuck.docx`` 后，同步 ``fuck_svg.docx``（删除旧副本 → 拷贝 → SVG 替换）。

用法::

    python cursor_tmp/format_docx_py/update_fuck_svg_docx.py
"""
from __future__ import annotations

import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_CURSOR_TMP = _SCRIPT_DIR.parent
if str(_CURSOR_TMP) not in sys.path:
    sys.path.insert(0, str(_CURSOR_TMP))
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from sync_fuck_docx_pair import update_fuck_svg_docx


def main() -> int:
    replaced, total = update_fuck_svg_docx()
    print(f"[done] fuck_svg.docx updated: {replaced}/{total} EMF → SVG")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# -*- coding: utf-8 -*-
"""Convert chapter 6 pipe function tables to §4.4-style HTML tables in md_sdd_0519.md."""
from __future__ import annotations

import sys
from pathlib import Path

_CURSOR_TMP = Path(__file__).resolve().parents[1]
_ROOT = _CURSOR_TMP.parent
if str(_CURSOR_TMP / "format_docx_py") not in sys.path:
    sys.path.insert(0, str(_CURSOR_TMP / "format_docx_py"))

from function_table_html import convert_pipe_function_tables, validate_table_shape  # noqa: E402

MD = _ROOT / "md_sdd_0519.md"


def main() -> None:
    text = MD.read_text(encoding="utf-8")
    new_text, n = convert_pipe_function_tables(text, chapter_prefix="6.")
    if n == 0:
        print("no chapter-6 pipe function tables found")
        return
    # spot-check first converted table
    import re

    first = re.search(r'<table border="1"[^>]*>.*?</table>', new_text[n : n + 50000], re.DOTALL)
    if first:
        errs = validate_table_shape(first.group(0))
        if errs:
            raise SystemExit(f"template validation failed: {errs}")
    MD.write_text(new_text, encoding="utf-8")
    html_count = new_text.count('<table border="1"')
    print(f"converted {n} pipe tables -> HTML; total HTML function tables in MD: {html_count}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Extract §2.4 requirement allocation table from ipcs-architecture.pdf."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "ipcs-architecture.pdf"
OUT = ROOT / "cursor_tmp" / "req_allocation_24.json"


def main() -> int:
    try:
        import pdfplumber
    except ImportError:
        print("pdfplumber required", file=sys.stderr)
        return 1

    rows: list[dict[str, str]] = []
    with pdfplumber.open(PDF) as pdf:
        for page_idx in range(6, 9):
            for table in pdf.pages[page_idx].extract_tables() or []:
                for row in table:
                    if not row or not row[0]:
                        continue
                    rid = str(row[0]).strip()
                    if not re.match(r"^IPCS_\d+$", rid):
                        continue
                    rows.append(
                        {
                            "id": rid,
                            "summary": (row[1] or "").replace("\n", " ").strip(),
                            "components": (row[2] or "").replace("\n", " ").strip(),
                            "notes": (row[3] or "").replace("\n", " ").strip()
                            if len(row) > 3
                            else "",
                        }
                    )

    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(rows)} rows -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

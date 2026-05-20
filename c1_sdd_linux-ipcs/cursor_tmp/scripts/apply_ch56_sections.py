#!/usr/bin/env python3
"""Splice ch56_sections.md into md_sdd_0519.md (§5.1–5.2 and §6.1–6.2)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MD = ROOT / "md_sdd_0519.md"
CH56 = ROOT / "cursor_tmp" / "ch56_sections.md"


def main() -> None:
    text = MD.read_text(encoding="utf-8")
    ch56 = CH56.read_text(encoding="utf-8")
    parts = ch56.split("\n---\n\n", 1)
    ch5, ch6 = parts[0].strip(), parts[1].strip()

    s5 = text.find("## 5.1 ")
    e5 = text.find("\n## 5.3 ", s5)
    if s5 < 0 or e5 < 0:
        raise SystemExit("§5.1/5.3 markers not found")

    s6 = text.find("## 6.1 ")
    e6 = text.find("\n## 6.3 ", s6)
    if s6 < 0 or e6 < 0:
        raise SystemExit("§6.1/6.3 markers not found")

    new_text = text[:s5] + ch5 + "\n\n" + text[e5:s6] + ch6 + "\n\n" + text[e6:]
    MD.write_text(new_text, encoding="utf-8")
    print(f"Updated {MD}")


if __name__ == "__main__":
    main()

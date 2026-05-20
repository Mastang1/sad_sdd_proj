# -*- coding: utf-8 -*-
"""Ensure blank line before ### headings so Pandoc emits Word Heading 3."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MD = ROOT / "md_sdd_0519.md"


def main() -> None:
    text = MD.read_text(encoding="utf-8")
    # Single newline before ### → double newline (Pandoc ATX heading requirement).
    new_text, n = re.subn(r"([^\n])\n(### \d+\.\d+(?:\.\d+)? )", r"\1\n\n\2", text)
    MD.write_text(new_text, encoding="utf-8")
    print(f"fixed {n} heading blank-line(s) in {MD}")


if __name__ == "__main__":
    main()

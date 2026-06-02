# -*- coding: utf-8 -*-
"""Find function-table pages where extracted text is mostly digits."""
import sys
import re
import pdfplumber

sys.stdout.reconfigure(encoding="utf-8")

def digit_ratio(s: str) -> float:
    s = s.strip()
    if not s:
        return 0.0
    digits = sum(c.isdigit() for c in s)
    letters = sum(c.isalpha() or ord(c) > 127 for c in s)
    if letters >= 2:
        return 0.0
    return digits / max(len(s), 1)

bad_pages = []
with pdfplumber.open("final.pdf") as pdf:
    for pi, page in enumerate(pdf.pages):
        for t in page.extract_tables() or []:
            all_text = "\n".join(str(c) for row in t for c in (row or []) if c)
            if "\u51fd\u6570\u539f\u578b" not in all_text and "\u8f93\u5165/\u8f93\u51fa\u53c2\u6570" not in all_text:
                continue
            numeric_cells = 0
            total_cells = 0
            samples = []
            for row in t:
                for cell in row or []:
                    if not cell or not str(cell).strip():
                        continue
                    total_cells += 1
                    if digit_ratio(str(cell)) > 0.7:
                        numeric_cells += 1
                        if len(samples) < 3:
                            samples.append(str(cell)[:40])
            if total_cells and numeric_cells / total_cells > 0.5:
                bad_pages.append((pi + 1, numeric_cells, total_cells, samples))

print("bad function-like tables:", len(bad_pages))
for item in bad_pages[:15]:
    print(" page", item[0], f"{item[1]}/{item[2]} numeric", item[3])

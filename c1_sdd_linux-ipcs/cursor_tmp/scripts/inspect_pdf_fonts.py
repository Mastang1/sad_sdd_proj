# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding="utf-8")

try:
    import fitz  # pymupdf
except ImportError:
    print("no pymupdf")
    sys.exit(1)

def inspect(path, page_idx=50):
    doc = fitz.open(path)
    page = doc[page_idx]
    text = page.get_text()
    print("===", path, "page", page_idx + 1, "===")
    print("text sample:", repr(text[:500]))
    fonts = set()
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                fonts.add(span.get("font", ""))
    print("fonts:", sorted(fonts)[:15], "count", len(fonts))
    doc.close()

inspect("final.pdf", 50)
inspect("final_word_test.pdf", 50)

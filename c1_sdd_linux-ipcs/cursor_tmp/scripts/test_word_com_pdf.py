# -*- coding: utf-8 -*-
"""Quick test: Word COM export vs LibreOffice."""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

root = Path(__file__).resolve().parents[2]
docx = root / "final_sdd.docx"
pdf = root / "final_word_test.pdf"

import win32com.client  # type: ignore

word = win32com.client.Dispatch("Word.Application")
word.Visible = False
try:
    doc = word.Documents.Open(str(docx.resolve()))
    # 17 = wdExportFormatPDF
    doc.ExportAsFixedFormat(str(pdf.resolve()), ExportFormat=17, OpenAfterExport=False)
    doc.Close(False)
    print("Word export OK:", pdf, "size", pdf.stat().st_size)
finally:
    word.Quit()

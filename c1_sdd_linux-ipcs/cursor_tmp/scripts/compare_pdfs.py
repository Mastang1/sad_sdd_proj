# -*- coding: utf-8 -*-
import sys
import pdfplumber

sys.stdout.reconfigure(encoding="utf-8")

def sample_tables(path, pages=(51,)):
    print("===", path, "===")
    with pdfplumber.open(path) as pdf:
        for pi in pages:
            page = pdf.pages[pi - 1]
            tables = page.extract_tables() or []
            print("page", pi, "tables", len(tables))
            for ti, t in enumerate(tables[:2]):
                print(" table", ti)
                for row in t[:6]:
                    print("  ", row)

sample_tables("final.pdf", pages=[51, 6])
sample_tables("final_word_test.pdf", pages=[51, 6])

# -*- coding: utf-8 -*-
import sys
import zipfile
import re
sys.stdout.reconfigure(encoding="utf-8")

z = zipfile.ZipFile("final_sdd.docx")
xml = z.read("word/document.xml").decode("utf-8")
# count numPr inside tables
tbl_chunks = re.findall(r"<w:tbl>.*?</w:tbl>", xml, re.S)
numpr_in_tbl = sum(chunk.count("<w:numPr") for chunk in tbl_chunks)
fld_in_tbl = sum(chunk.count("<w:instrText") for chunk in tbl_chunks)
print("tables in xml:", len(tbl_chunks))
print("numPr inside tables:", numpr_in_tbl)
print("instrText inside tables:", fld_in_tbl)

# sample a pandoc table (early in doc) - table index 2
if tbl_chunks:
    chunk = tbl_chunks[2][:1200]
    print("sample table xml head:")
    print(chunk[:1200])

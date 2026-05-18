#!/usr/bin/env python3
"""Find the actual SWE.1 page content in the raw extracted text"""
import re

with open('aspice_4_4_raw.txt', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

with open('find_swe_output.txt', 'w', encoding='utf-8') as out:
    # Find all PAGE markers to understand structure
    page_markers = []
    for i, line in enumerate(lines):
        m = re.search(r'=== PAGE (\d+) ===', line)
        if m:
            page_markers.append((int(m.group(1)), i))

    out.write(f"Total PAGE markers: {len(page_markers)}\n")
    out.write("First 30 page markers:\n")
    for pn, li in page_markers[:30]:
        snippet = lines[li+1].strip() if li+1 < len(lines) else ""
        out.write(f"  Page {pn} at line {li}: {snippet[:100]}\n")

    # Find 4.4.1 SWE.1 content
    out.write("\n--- Looking for 4.4.1 SWE.1 content ---\n")
    for i, line in enumerate(lines):
        if re.search(r'4\.4\.1', line) and 'SWE.1' in line:
            out.write(f"Line {i}: {line.strip()[:150]}\n")

    # Print pages around 45 (SWE.1 page)
    out.write("\n--- Content around page 45 ---\n")
    for pn, li in page_markers:
        if 44 <= pn <= 50:
            out.write(f"\nPage {pn} starts at line {li}:\n")
            for j in range(li, min(li+10, len(lines))):
                out.write(f"  L{j}: {lines[j].strip()[:150]}\n")

print("Done, output written to find_swe_output.txt")

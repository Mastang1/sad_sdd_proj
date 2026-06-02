# -*- coding: utf-8 -*-
"""Audit chapter 6 flow PlantUML files referenced in md_sdd_0519.md."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUML_DIR = ROOT / "cursor_tmp" / "flow_umls"
MD = (ROOT / "md_sdd_0519.md").read_text(encoding="utf-8")

slugs = sorted(
    {m.replace(".svg", "") for m in re.findall(r"flow_svgs/(linux_[^)]+\.svg)", MD)}
)

PROSE = re.compile(
    r"(resolve|map to|initialize|configure|handle|process|branch|"
    r"save |copy |from channel|from priv|generic|placeholder|TODO|FIXME)",
    re.I,
)
BAD_NODE = re.compile(r":[^;\n]*(endif|\.\.\.|\bgoto\b)[^;\n]*;", re.I)
BAD_ELSE = re.compile(r"else \(no\)\s*\n\s*endif", re.M)
PARTITION = re.compile(r"\b(partition|floating note|\|\|)\b", re.I)


def count_activity_nodes(body: str) -> int:
    nodes = 0
    for line in body.splitlines():
        s = line.strip()
        if s.startswith(":") and (s.endswith(";") or ";;" in s):
            nodes += 1
    return nodes


def audit_slug(slug: str) -> list[str]:
    p = PUML_DIR / f"{slug}.puml"
    if not p.exists():
        return ["MISSING_PUML"]

    text = p.read_text(encoding="utf-8")
    probs: list[str] = []

    if BAD_ELSE.search(text):
        probs.append("empty_else_no_branch")

    for m in BAD_NODE.finditer(text):
        probs.append(f"bad_node:{m.group(0)[:80]}")

    for i, line in enumerate(text.splitlines(), 1):
        st = line.strip()
        if st.startswith(":") and "..." in st:
            probs.append(f"ellipsis_node:L{i}:{st[:80]}")
        if st.startswith(":") and not st.rstrip().endswith(";") and "@startuml" not in st:
            if i + 1 < len(text.splitlines()):
                nxt = text.splitlines()[i].strip() if i < len(text.splitlines()) else ""
                if not nxt.startswith('"') and not nxt.startswith(","):
                    probs.append(f"broken_node:L{i}:{st[:80]}")

    if ";;" in text:
        probs.append("double_semicolon")

    nodes = count_activity_nodes(text)
    if nodes > 20 and not PARTITION.search(text):
        probs.append(f"nodes={nodes}_no_partition")

    for line in text.splitlines():
        if line.strip().startswith(":"):
            content = line.strip()[1:].strip(" ;")
            if PROSE.search(content) and not re.search(r"[=()\[\]&]|->", content):
                probs.append(f"prose:{content[:60]}")

    return probs


def main() -> int:
    issues: list[tuple[str, list[str]]] = []
    for slug in slugs:
        probs = audit_slug(slug)
        if probs:
            issues.append((slug, probs))

    print(f"Chapter6 slugs in MD: {len(slugs)}")
    print(f"Slugs with issues: {len(issues)}")
    for slug, probs in issues:
        print(f"\n{slug}:")
        for p in probs:
            print(f"  - {p}")

    out = ROOT / "cursor_tmp" / "audit_ch6_flows_report.txt"
    lines = [f"Chapter6 slugs: {len(slugs)}", f"Issues: {len(issues)}", ""]
    for slug, probs in issues:
        lines.append(slug)
        lines.extend(f"  - {p}" for p in probs)
        lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n[written] {out}")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())

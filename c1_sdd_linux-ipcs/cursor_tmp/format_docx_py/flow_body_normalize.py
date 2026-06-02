# -*- coding: utf-8 -*-
"""Normalize PlantUML activity diagram bodies before writing .puml files."""
from __future__ import annotations

import re

_STRUCTURAL = re.compile(
    r"^(if |elseif |else |endif|while |endwhile|repeat|repeat while|stop|start|"
    r"partition|\|\||break|@)",
    re.I,
)


def normalize_flow_body(body: str) -> str:
    """Merge broken activity lines, fix ;; , split '; stop', drop empty else branches."""
    body = body.replace(";;", ";")
    body = re.sub(r";\s+stop\b", ";\nstop", body)

    lines = body.strip().splitlines()
    merged: list[str] = []
    i = 0
    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()
        if not stripped:
            merged.append(raw)
            i += 1
            continue

        indent = raw[: len(raw) - len(raw.lstrip())]
        if stripped.startswith(":") and not stripped.rstrip().endswith(";"):
            parts: list[str] = []
            first = stripped[1:].strip()
            if first:
                parts.append(first.rstrip(";"))
            i += 1
            while i < len(lines):
                cont = lines[i].strip()
                if not cont or _STRUCTURAL.match(cont):
                    break
                parts.append(cont.rstrip(";"))
                i += 1
                if cont.endswith(";"):
                    break
            text = f"{chr(92)}n".join(parts)
            merged.append(f"{indent}:{text};")
            continue

        merged.append(raw)
        i += 1

    text = "\n".join(merged)
    text = re.sub(r"(\n\s*stop\s*\n)\s*else \(no\)\s*\n", r"\1", text)
    text = re.sub(r"else \(no\)\s*\n(\s*)endif", r"\1endif", text)
    return text.strip() + "\n"

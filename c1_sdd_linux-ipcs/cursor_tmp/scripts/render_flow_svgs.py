# -*- coding: utf-8 -*-
"""SVG export for flow_umls via PlantUML (Java). Outputs to ../flow_svgs/."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def find_jar() -> Path:
    for candidate in plantuml_jar_candidates():
        if candidate.is_file():
            return candidate
    sys.exit("missing PlantUML jar (workspace root or cursor_tmp/scripts/plantuml.jar)")


def main() -> None:
    jar = find_jar()

    svg_dir = FLOW_SVGS
    svg_dir.mkdir(parents=True, exist_ok=True)
    umls = sorted(FLOW_UMLS.glob("*.puml"))
    if not umls:
        sys.exit("no .puml in flow_umls/")
    subprocess.check_call(
        [
            "java",
            "-jar",
            str(jar),
            "-charset",
            "UTF-8",
            "-tsvg",
            "-o",
            str(svg_dir),
            *[str(p) for p in umls],
        ]
    )
    print(f"{len(umls)} diagram(s) -> {svg_dir}/")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""SVG export for flow_umls via PlantUML (Java). Outputs to ../flow_svgs/."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JAR = ROOT / "scripts" / "plantuml.jar"


def main() -> None:
    if not JAR.is_file():
        sys.exit(f"missing PlantUML jar: {JAR}")

    svg_dir = ROOT / "flow_svgs"
    svg_dir.mkdir(parents=True, exist_ok=True)
    umls = sorted((ROOT / "flow_umls").glob("*.puml"))
    if not umls:
        sys.exit("no .puml in flow_umls/")
    subprocess.check_call(
        [
            "java",
            "-jar",
            str(JAR),
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

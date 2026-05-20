# -*- coding: utf-8 -*-
"""SVG export for flow_umls via PlantUML (Java). Outputs to ../flow_svgs/.

Pre-flight: SDD_TOOLCHAIN.md §3 pipeline B; excludes *_seq_* (use
render_scenario_sequences.py). After edits, run validate if delivering docx.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_CURSOR_TMP = Path(__file__).resolve().parents[1]
if str(_CURSOR_TMP) not in sys.path:
    sys.path.insert(0, str(_CURSOR_TMP))
from workspace_paths import FLOW_SVGS, FLOW_UMLS, plantuml_jar_candidates


def find_jar() -> Path:
    for candidate in plantuml_jar_candidates():
        if candidate.is_file():
            return candidate
    sys.exit("missing PlantUML jar (workspace root or cursor_tmp/scripts/plantuml.jar)")


def main() -> None:
    jar = find_jar()

    svg_dir = FLOW_SVGS
    svg_dir.mkdir(parents=True, exist_ok=True)
    umls = sorted(
        p for p in FLOW_UMLS.glob("*.puml") if "_seq_" not in p.stem
    )
    if not umls:
        sys.exit("no .puml in flow_umls/")
    failed: list[str] = []
    for puml in umls:
        r = subprocess.run(
            [
                "java",
                "-jar",
                str(jar),
                "-charset",
                "UTF-8",
                "-tsvg",
                "-o",
                str(svg_dir),
                str(puml),
            ],
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            failed.append(puml.stem)
    print(f"{len(umls) - len(failed)} diagram(s) -> {svg_dir}/")
    if failed:
        print(f"PlantUML failed ({len(failed)}): {', '.join(failed[:12])}")
        if len(failed) > 12:
            print(f"  ... +{len(failed) - 12} more")
        sys.exit(1)


if __name__ == "__main__":
    main()

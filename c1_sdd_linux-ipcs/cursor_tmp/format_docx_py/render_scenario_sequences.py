# -*- coding: utf-8 -*-
r"""
Render §5.7 / §6.7 cross-unit scenario sequence diagrams.

Usage (repository root)::

    python cursor_tmp/format_docx_py/render_scenario_sequences.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_CURSOR_TMP = Path(__file__).resolve().parents[1]
if str(_CURSOR_TMP) not in sys.path:
    sys.path.insert(0, str(_CURSOR_TMP))
from workspace_paths import FLOW_SVGS, FLOW_UMLS, plantuml_jar_candidates

from scenario_sequence_flows import ALL_DIAGRAMS


def find_plantuml_jar() -> Path:
    for candidate in plantuml_jar_candidates():
        if candidate.is_file():
            return candidate
    sys.exit("plantuml.jar not found at workspace root or cursor_tmp/scripts/plantuml.jar")


def main() -> None:
    jar = find_plantuml_jar()
    FLOW_UMLS.mkdir(parents=True, exist_ok=True)
    FLOW_SVGS.mkdir(parents=True, exist_ok=True)
    failed: list[str] = []
    for slug, body in sorted(ALL_DIAGRAMS.items()):
        puml = FLOW_UMLS / f"{slug}.puml"
        puml.write_text(body, encoding="utf-8")
        result = subprocess.run(
            [
                "java",
                "-jar",
                str(jar),
                "-charset",
                "UTF-8",
                "-tsvg",
                "-o",
                str(FLOW_SVGS),
                str(puml),
            ],
            capture_output=True,
            text=True,
        )
        svg = FLOW_SVGS / f"{slug}.svg"
        if result.returncode != 0 and not svg.is_file():
            failed.append(slug)
            err = (result.stderr or result.stdout or "").strip()
            if err:
                print(err.splitlines()[-1])
    ok = sum(1 for s in ALL_DIAGRAMS if (FLOW_SVGS / f"{s}.svg").is_file())
    print(f"Rendered {ok}/{len(ALL_DIAGRAMS)} sequence SVG(s) -> {FLOW_SVGS}/")
    if failed:
        sys.exit(f"failed: {failed}")


if __name__ == "__main__":
    main()

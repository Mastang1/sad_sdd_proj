# -*- coding: utf-8 -*-
r"""
Regenerate chapter 6 Linux PlantUML flows and render SVG via plantuml.jar.

Usage (repository root)::

    python cursor_tmp/format_docx_py/render_linux_ch6_flows.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from linux_ch6_flows import FLOWS, HEADER

ROOT = Path(__file__).resolve().parents[1]
FLOW_UMLS = ROOT / "flow_umls"
FLOW_SVGS = ROOT / "flow_svgs"


def find_plantuml_jar() -> Path:
    for candidate in plantuml_jar_candidates():
        if candidate.is_file():
            return candidate
    sys.exit("plantuml.jar not found at workspace root or cursor_tmp/scripts/plantuml.jar")


def write_puml(slug: str, body: str) -> Path:
    FLOW_UMLS.mkdir(parents=True, exist_ok=True)
    path = FLOW_UMLS / f"{slug}.puml"
    text = HEADER + body.strip() + "\n@enduml\n"
    path.write_text(text, encoding="utf-8")
    return path


def render_svgs(jar: Path, puml_files: list[Path]) -> list[str]:
    FLOW_SVGS.mkdir(parents=True, exist_ok=True)
    failed: list[str] = []
    for puml in puml_files:
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
        if result.returncode != 0:
            failed.append(puml.stem)
            err = (result.stderr or result.stdout or "").strip()
            if err:
                print(err.splitlines()[-1])
    return failed


def main() -> None:
    jar = find_plantuml_jar()
    puml_files: list[Path] = []
    for slug in sorted(FLOWS):
        puml_files.append(write_puml(slug, FLOWS[slug]))
    print(f"Wrote {len(puml_files)} .puml files")
    failed = render_svgs(jar, puml_files)
    rendered = sum(1 for slug in FLOWS if (FLOW_SVGS / f"{slug}.svg").is_file())
    print(f"Rendered {rendered} SVG(s) -> {FLOW_SVGS}/")
    if failed:
        sys.exit(f"PlantUML failed for: {failed}")
    if rendered != len(FLOWS):
        missing = [s for s in FLOWS if not (FLOW_SVGS / f"{s}.svg").is_file()]
        sys.exit(f"missing SVG: {missing[:5]} ... ({len(missing)} total)")


if __name__ == "__main__":
    main()

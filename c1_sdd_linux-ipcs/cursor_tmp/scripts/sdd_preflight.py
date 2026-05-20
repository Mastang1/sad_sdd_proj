# -*- coding: utf-8 -*-
r"""
SDD toolchain pre-flight checks (G1–G5 helpers).

Does NOT replace human/AI gate in SDD_TOOLCHAIN.md §1; run before batch scripts.

Usage (repository root)::

    python cursor_tmp/scripts/sdd_preflight.py
    python cursor_tmp/scripts/sdd_preflight.py --md-svg
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_CURSOR_TMP = Path(__file__).resolve().parents[1]
if str(_CURSOR_TMP) not in sys.path:
    sys.path.insert(0, str(_CURSOR_TMP))

from workspace_paths import (
    MD_SDD_0519,
    FLOW_SVGS,
    PLANTUML_JAR,
    WORKSPACE_ROOT,
    plantuml_jar_candidates,
)


def check_plantuml() -> bool:
    for p in plantuml_jar_candidates():
        if p.is_file():
            print(f"[OK] plantuml.jar: {p}")
            return True
    print("[FAIL] plantuml.jar not found")
    return False


def check_md_svg_refs() -> bool:
    text = MD_SDD_0519.read_text(encoding="utf-8")
    svgs = set(re.findall(r"flow_svgs/([^)]+\.svg)", text))
    missing = [s for s in sorted(svgs) if not (FLOW_SVGS / s).is_file()]
    print(f"[INFO] MD flow_svgs refs: {len(svgs)}")
    if missing:
        print(f"[FAIL] missing SVG on disk: {len(missing)}")
        for m in missing[:10]:
            print(f"  - {m}")
        if len(missing) > 10:
            print(f"  ... +{len(missing) - 10} more")
        return False
    print("[OK] all MD flow_svgs references exist")
    return True


def print_gate_reminder() -> None:
    print(
        """
=== SDD pre-flight (see cursor_tmp/SDD_TOOLCHAIN.md §1) ===
G1  Map task to pipeline A/B/C/D/E
G2  Pick scripts from §2; confirm overwrite scope
G3  Init/goto: prefer linux_ch6_flows / emit_puml, not bulk regenerate
G4  Fix script/manual if capability gap
G5  plantuml -checkonly per .puml; validate PASS before delivery
"""
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="SDD toolchain pre-flight")
    parser.add_argument("--md-svg", action="store_true", help="check MD svg refs")
    args = parser.parse_args()

    print_gate_reminder()
    ok = check_plantuml()
    if args.md_svg:
        ok = check_md_svg_refs() and ok
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

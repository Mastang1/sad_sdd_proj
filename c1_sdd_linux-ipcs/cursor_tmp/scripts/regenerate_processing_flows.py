# -*- coding: utf-8 -*-
r"""
Regenerate processing-flow PlantUML/SVG from ipcs/ sources (heuristic C→PlantUML).

WARNING — read cursor_tmp/SDD_TOOLCHAIN.md §1 G3 and §5 before running:
  - Do NOT use for Init/goto-heavy functions unless each .puml passes
    ``java -jar plantuml.jar -checkonly`` and you accept full diff review.
  - Prefer pipeline A: edit linux_ch6_flows.FLOWS / emit_puml, then
    render_linux_ch6_flows.py.
  - Running this BEFORE emit_puml.py will be overwritten by emit; running
    AFTER emit is OK only for slugs emit does not own.

Pre-flight (mandatory): complete G1–G4 in SDD_TOOLCHAIN.md; confirm task
requires bulk regen, not hand-written flows.

Usage (repository root)::

    python cursor_tmp/scripts/regenerate_processing_flows.py
    python cursor_tmp/scripts/render_flow_svgs.py
    python cursor_tmp/format_docx_py/render_scenario_sequences.py
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

_CURSOR_TMP = Path(__file__).resolve().parents[1]
if str(_CURSOR_TMP) not in sys.path:
    sys.path.insert(0, str(_CURSOR_TMP))
if str(_CURSOR_TMP / "format_docx_py") not in sys.path:
    sys.path.insert(0, str(_CURSOR_TMP / "format_docx_py"))

from workspace_paths import FLOW_UMLS, MD_SDD_0519, WORKSPACE_ROOT
from c_to_activity import read_source_function, write_puml
from workspace_paths import plantuml_jar_candidates

SKIP_SVG_STEMS = frozenset(
    {
        "architecture_layered_linux_variants",
    }
)

# MD 函数名与源码符号不一致时的别名（按定义文件）
FUNC_ALIASES: dict[tuple[str, str], str] = {
    ("ipcs/mcu/os/threadx/ipc-os-threadx.c", "ipcsShmSoftIrq"): "ipcsShmSoftIrq",
}


def find_plantuml_jar() -> Path | None:
    for candidate in plantuml_jar_candidates():
        if candidate.is_file():
            return candidate
    return None


def plantuml_ok(jar: Path, puml_path: Path) -> bool:
    r = subprocess.run(
        ["java", "-jar", str(jar), "-checkonly", str(puml_path)],
        capture_output=True,
        text=True,
    )
    return r.returncode == 0


def parse_md_flow_sections(md_text: str) -> list[dict]:
    sections: list[dict] = []
    for part in re.split(r"\n(?=### )", md_text):
        m = re.match(r"### (\d+\.\d+\.\d+) (\S+)", part)
        if not m or "processing flow" not in part:
            continue
        img = re.search(r"flow_svgs/([^)]+\.svg)", part)
        def_m = re.search(
            r"函数定义文件</td>\s*<td colspan=\"4\">`?([^`<]+)`?",
            part,
        )
        if not img or not def_m:
            continue
        slug = img.group(1).replace(".svg", "")
        if slug in SKIP_SVG_STEMS or "_seq_" in slug:
            continue
        sections.append(
            {
                "index": m.group(1),
                "func": m.group(2),
                "slug": slug,
                "def_file": def_m.group(1).strip(),
            }
        )
    return sections


def backup_md() -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = _CURSOR_TMP / f"md_sdd_0519_backup_{ts}.md"
    shutil.copy2(MD_SDD_0519, dest)
    return dest


def sync_linux_ch6_flows(generated: dict[str, str]) -> int:
    """Update FLOWS entries in linux_ch6_flows.py for regenerated linux_* slugs."""
    path = _CURSOR_TMP / "format_docx_py" / "linux_ch6_flows.py"
    text = path.read_text(encoding="utf-8")
    updated = 0
    for slug, body in generated.items():
        if not slug.startswith("linux_"):
            continue
        key = f'"{slug}"'
        if key not in text:
            continue
        pattern = rf'("{re.escape(slug)}": """)\n(.*?)"""'
        new_block = rf'\1\n{body.strip()}\n"""'
        new_text, n = re.subn(pattern, new_block, text, count=1, flags=re.DOTALL)
        if n:
            text = new_text
            updated += 1
    if updated:
        path.write_text(text, encoding="utf-8")
    return updated


def main() -> None:
    md_text = MD_SDD_0519.read_text(encoding="utf-8")
    sections = parse_md_flow_sections(md_text)
    if not sections:
        sys.exit("no processing-flow sections found in md_sdd_0519.md")

    backup = backup_md()
    print(f"MD backup: {backup.relative_to(WORKSPACE_ROOT)}")

    jar = find_plantuml_jar()
    ok, fail, skipped = 0, [], 0
    linux_bodies: dict[str, str] = {}
    FLOW_UMLS.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    for sec in sections:
        slug = sec["slug"]
        func = sec["func"]
        def_file = sec["def_file"]
        if not def_file.startswith("ipcs/"):
            def_file = f"ipcs/{def_file}" if "/" not in def_file else def_file

        lookup = FUNC_ALIASES.get((def_file, func), func)
        activity = read_source_function(def_file, lookup, WORKSPACE_ROOT)
        if activity is None:
            fail.append(f"{slug} ({func} @ {def_file})")
            continue

        title = f"{sec['index']} {func}"
        include_title = not slug.startswith("linux_")
        out = FLOW_UMLS / f"{slug}.puml"
        tmp = out.with_suffix(".puml.gen")
        write_puml(tmp, title, activity, include_title=include_title)
        if jar and not plantuml_ok(jar, tmp):
            tmp.unlink(missing_ok=True)
            skipped += 1
            continue
        tmp.replace(out)
        written.append(out)
        if slug.startswith("linux_"):
            linux_bodies[slug] = activity
        ok += 1

    print(f"Accepted {ok} .puml; skipped invalid {skipped}")
    if fail:
        print(f"Extract failed ({len(fail)}):")
        for line in fail[:15]:
            print(f"  - {line}")
        if len(fail) > 15:
            print(f"  ... and {len(fail) - 15} more")

    if jar and written:
        svg_dir = _CURSOR_TMP / "flow_svgs"
        svg_dir.mkdir(parents=True, exist_ok=True)
        for puml in written:
            subprocess.run(
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
                check=True,
            )
        print(f"Rendered {len(written)} SVG(s)")
    render = _CURSOR_TMP / "scripts" / "render_flow_svgs.py"
    subprocess.check_call([sys.executable, str(render)], cwd=WORKSPACE_ROOT)
    seq = _CURSOR_TMP / "format_docx_py" / "render_scenario_sequences.py"
    if seq.is_file():
        subprocess.check_call([sys.executable, str(seq)], cwd=WORKSPACE_ROOT)

    if fail and ok == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()

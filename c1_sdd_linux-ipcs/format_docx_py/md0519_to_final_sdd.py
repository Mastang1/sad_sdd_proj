# -*- coding: utf-8 -*-
r"""
将 ``md_sdd_0519.md`` 全文转换并写入 ``final_sdd.docx``（TF）。

流程（与 ``scripts/build_final_sdd_docx.py`` 一致，源文件改为 md_sdd_0519.md）：

1. 解析 Markdown：将 ``md_sdd_0519_media/imageN.png`` 按上文 ``### 3.2.x / 3.3.x / 3.4.x`` 映射到
   ``files_32_svgs/`` 或 ``flow_svgs/`` 中的 SVG（缺失则保留原路径并告警）。
2. Mermaid 预处理、SVG→PNG（CairoSVG）供 Pandoc 嵌入。
3. Pandoc 生成正文 DOCX，与现有 ``final_sdd.docx`` 封面（首个分页符之前）合并。
4. 调用 ``format_final_sdd`` 应用 .cursorrules 中的 TF 版式（字体、表格边框、插图宽度等）。

**依赖**::

    pip install python-docx docxcompose cairosvg beautifulsoup4 lxml
    pandoc 3.x（PATH 可用）

**使用方式**（仓库根目录 ``c1_sdd_linux-ipcs``）::

    python format_docx_py/md0519_to_final_sdd.py
    python format_docx_py/md0519_to_final_sdd.py "D:\\path\\final_sdd.docx"

若 ``final_sdd.docx`` 被 Word 占用，将写入 ``final_sdd.generated.docx``。
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[1]
SOURCE_MD = WORKSPACE / "md_sdd_0519.md"
TARGET_DOCX = WORKSPACE / "final_sdd.docx"
PANDOC_SRC = WORKSPACE / "_pandoc_md0519.md"
BODY_DOCX = WORKSPACE / "_body_md0519.docx"
BUILD_SCRIPT = WORKSPACE / "scripts" / "build_final_sdd_docx.py"
FORMAT_SCRIPT = WORKSPACE / "format_docx_py" / "format_final_sdd.py"

_HEADING_RE = re.compile(r"^###\s+(3\.2\.\d+|3\.3\.\d+|3\.4\.\d+)\s+", re.MULTILINE)
_MEDIA_IMG_RE = re.compile(
    r"!\[([^\]]*)\]\(md_sdd_0519_media/image(\d+)\.png\)"
)


def _load_build():
    spec = importlib.util.spec_from_file_location("bfd", BUILD_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {BUILD_SCRIPT}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _svg_for_section(section: str) -> Path | None:
    """3.2.2 -> files_32_svgs/3_2_2.svg ; 3.3.1 / 3.4.23 -> flow_svgs/3_3_1.svg"""
    parts = section.split(".")
    if len(parts) != 3:
        return None
    major, minor, patch = parts
    if major == "3" and minor == "2":
        p = WORKSPACE / "files_32_svgs" / f"3_2_{patch}.svg"
    elif major == "3" and minor in ("3", "4"):
        p = WORKSPACE / "flow_svgs" / f"3_{minor}_{patch}.svg"
        if not p.is_file() and minor == "4":
            alt = WORKSPACE / "flow_svgs" / f"tx_3_4_{patch}.svg"
            if alt.is_file():
                p = alt
    else:
        return None
    return p if p.is_file() else None


def resolve_media_images(md_text: str) -> str:
    """按最近 ### 3.x.y 标题，将 md_sdd_0519_media 占位图改为本地 SVG 路径。"""
    last_section: str | None = None
    out_lines: list[str] = []
    missing: list[str] = []

    for line in md_text.splitlines(keepends=True):
        hm = _HEADING_RE.match(line)
        if hm:
            last_section = hm.group(1)

        def repl(m: re.Match[str]) -> str:
            nonlocal last_section
            alt = m.group(1)
            num = m.group(2)
            if last_section:
                svg = _svg_for_section(last_section)
                if svg:
                    rel = svg.relative_to(WORKSPACE).as_posix()
                    return f"![{alt}]({rel})"
            missing.append(f"image{num}.png (section={last_section})")
            return m.group(0)

        out_lines.append(_MEDIA_IMG_RE.sub(repl, line))

    if missing:
        print(f"[warn] {len(missing)} image(s) could not be mapped to SVG, e.g. {missing[:5]}")
    return "".join(out_lines)


def ensure_media_from_docx(docx_path: Path) -> None:
    """从现有 TF 解出 word/media/* 到 md_sdd_0519_media/，供未映射的 imageN.png 使用。"""
    import zipfile

    media_dir = WORKSPACE / "md_sdd_0519_media"
    media_dir.mkdir(parents=True, exist_ok=True)
    if not docx_path.is_file():
        return
    with zipfile.ZipFile(docx_path) as z:
        for name in z.namelist():
            if not name.startswith("word/media/"):
                continue
            base = Path(name).name
            target = media_dir / base
            if not target.is_file():
                target.write_bytes(z.read(name))


def _special_image_fixes(md_text: str) -> str:
    """4.2.1 平台头文件等仍引用 image40；映射到 3_2_9.svg。"""
    p = WORKSPACE / "files_32_svgs" / "3_2_9.svg"
    if p.is_file():
        rel = p.relative_to(WORKSPACE).as_posix()
        md_text = md_text.replace("md_sdd_0519_media/image40.png", rel)
    return md_text


def run_pandoc_extended(bfd, md_path: Path, out_docx: Path) -> None:
    rpath = ";".join(
        [
            str(WORKSPACE),
            str(WORKSPACE / "flow_svgs"),
            str(WORKSPACE / "files_32_svgs"),
            str(WORKSPACE / "mermaid_svgs"),
            str(WORKSPACE / "_docx_raster"),
        ]
    )
    import subprocess

    cmd = [
        "pandoc",
        str(md_path),
        "-o",
        str(out_docx),
        "-f",
        "markdown+pipe_tables+raw_html+smart+yaml_metadata_block",
        "-t",
        "docx",
        "--resource-path",
        rpath,
        "--standalone",
    ]
    subprocess.run(cmd, cwd=str(WORKSPACE), check=True)
    print(f"[info] Pandoc → {out_docx}")


def run_format_final_sdd(docx_path: Path) -> None:
    spec = importlib.util.spec_from_file_location("format_final_sdd", FORMAT_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {FORMAT_SCRIPT}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    old_argv = sys.argv[:]
    try:
        sys.argv = [str(FORMAT_SCRIPT), str(docx_path)]
        mod.main()
    finally:
        sys.argv = old_argv


def main() -> None:
    out_docx = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else TARGET_DOCX.resolve()
    if not SOURCE_MD.is_file():
        sys.exit(f"missing: {SOURCE_MD}")

    bfd = _load_build()
    bfd.ROOT = WORKSPACE
    bfd.TARGET_DOCX = out_docx
    bfd.SOURCE_MD = SOURCE_MD

    bfd.ensure_default_cover(out_docx)
    ensure_media_from_docx(out_docx)

    md = SOURCE_MD.read_text(encoding="utf-8")
    md = resolve_media_images(md)
    md = _special_image_fixes(md)
    md = bfd.preprocess_mermaid(md)
    md = bfd.rasterize_svg_refs_for_docx(md, clear_cache=True)
    PANDOC_SRC.write_text(md, encoding="utf-8")

    run_pandoc_extended(bfd, PANDOC_SRC, BODY_DOCX)
    bfd.merge_cover_and_body(out_docx, BODY_DOCX, out_docx)

    alt = out_docx.with_name(out_docx.stem + ".generated.docx")
    saved = alt if alt.is_file() and (
        not out_docx.is_file() or alt.stat().st_mtime >= out_docx.stat().st_mtime
    ) else out_docx
    if saved == alt:
        print(f"[info] Using {saved} (target locked or alternate merge output)")

    for p in (PANDOC_SRC, BODY_DOCX):
        if p.is_file():
            p.unlink()

    print("[info] Applying format_final_sdd (TF styles)...")
    run_format_final_sdd(saved)
    print(f"[done] {saved}")
    if saved != out_docx and out_docx.is_file():
        print(f"[hint] Close Word and replace {out_docx} with {saved}")


if __name__ == "__main__":
    main()

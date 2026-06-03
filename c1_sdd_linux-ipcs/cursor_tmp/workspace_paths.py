# -*- coding: utf-8 -*-
"""
工作区路径约定（cursor_tmp 与根目录分离）。

工作区根目录保留：``ipcs/``、``*.md``、``final_sdd.docx``、``ipcs-architecture.pdf``、``plantuml.jar``。
其余构建产物、脚本、SVG/UML、媒体与临时文件位于 ``cursor_tmp/``。

脚本内统一::

    import sys
    from pathlib import Path
    _TMP = Path(__file__).resolve().parents[1]  # cursor_tmp（format_docx_py / scripts 下）
    if str(_TMP) not in sys.path:
        sys.path.insert(0, str(_TMP))
    from workspace_paths import WORKSPACE_ROOT, CURSOR_TMP, FLOW_SVGS, ...
"""

from __future__ import annotations

from pathlib import Path

CURSOR_TMP = Path(__file__).resolve().parent
WORKSPACE_ROOT = CURSOR_TMP.parent

# —— 工作区根目录（交付物）——
FINAL_SDD_DOCX = WORKSPACE_ROOT / "final_sdd.docx"
FORMAT_REFER_DOCX = WORKSPACE_ROOT / "format_refer" / "format_refer.docx"
MD_SDD_0519 = WORKSPACE_ROOT / "md_sdd_0519.md"
IPCS_SDD_MD = WORKSPACE_ROOT / "ipcs_sdd.md"
PLANTUML_JAR = WORKSPACE_ROOT / "plantuml.jar"
IPCS_ARCH_PDF = WORKSPACE_ROOT / "ipcs-architecture.pdf"
IPCS_SRC = WORKSPACE_ROOT / "ipcs"

# —— cursor_tmp 内资源 ——
FLOW_SVGS = CURSOR_TMP / "flow_svgs"
FLOW_EMF = CURSOR_TMP / "flow_emf"
FLOW_PNG = CURSOR_TMP / "flow_png"
EMF_EXTENT_REPORT = CURSOR_TMP / "flow_svg_to_emf_report.txt"
PNG_EXTENT_REPORT = CURSOR_TMP / "flow_svg_to_png_report.txt"
FLOW_UMLS = CURSOR_TMP / "flow_umls"
FILES_32_SVGS = CURSOR_TMP / "files_32_svgs"
FILES_32_UMLS = CURSOR_TMP / "files_32_umls"
MERMAID_SVGS = CURSOR_TMP / "mermaid_svgs"
MEDIA_DIR = CURSOR_TMP / "md_sdd_0519_media"
DOCX_RASTER = CURSOR_TMP / "_docx_raster"
FORMAT_DOCX_PY = CURSOR_TMP / "format_docx_py"
SCRIPTS = CURSOR_TMP / "scripts"
VALIDATE_REPORT = CURSOR_TMP / "validate_md_docx_report.txt"
MEM_INFO = CURSOR_TMP / "mem_info.md"
SDD_TOOLCHAIN = CURSOR_TMP / "SDD_TOOLCHAIN.md"

# 构建临时文件（cursor_tmp）
PANDOC_REFERENCE = CURSOR_TMP / "_pandoc_reference.docx"
PANDOC_MD0519 = CURSOR_TMP / "_pandoc_md0519.md"
BODY_MD0519 = CURSOR_TMP / "_body_md0519.docx"
PANDOC_FOR_WORD = CURSOR_TMP / "_pandoc_for_word.md"
BODY_GENERATED = CURSOR_TMP / "_body_generated.docx"


def rel_to_workspace(path: Path) -> str:
    """返回相对工作区根的路径（POSIX），供 Markdown / Pandoc 引用。"""
    return path.relative_to(WORKSPACE_ROOT).as_posix()


def pandoc_resource_path_str() -> str:
    """Pandoc ``--resource-path`` 分号分隔列表。"""
    return ";".join(
        str(p)
        for p in (
            WORKSPACE_ROOT,
            CURSOR_TMP,
            FLOW_SVGS,
            FILES_32_SVGS,
            MERMAID_SVGS,
            DOCX_RASTER,
        )
    )


def plantuml_jar_candidates() -> list[Path]:
    return [
        PLANTUML_JAR,
        SCRIPTS / "plantuml.jar",
        CURSOR_TMP / "plantuml.jar",
    ]

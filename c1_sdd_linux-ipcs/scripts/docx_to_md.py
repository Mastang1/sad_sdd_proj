#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 final_sdd.docx 完整转换为 Markdown，保留标题层级与编号、章节顺序及插图。

使用方式（在工作区根目录 c1_sdd 下执行）::

    python scripts/docx_to_md.py
    python scripts/docx_to_md.py final_sdd.docx md_sdd_0519.md

依赖：``pip install python-docx``
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterator

from docx import Document
from docx.document import Document as DocxDocument
from docx.oxml.ns import qn
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table, _Cell
from docx.text.paragraph import Paragraph

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DOCX = ROOT / "final_sdd.docx"
DEFAULT_MD = ROOT / "md_sdd_0519.md"
DEFAULT_MEDIA = ROOT / "md_sdd_0519_media"

SKIP_STYLES = frozenset({"Captioned Figure"})
TOC_STYLE_LEVEL = {"toc 1": 1, "toc 2": 2, "toc 3": 3}
HEADING_STYLE_LEVEL = {"Heading 1": 1, "Heading 2": 2, "Heading 3": 3}


def iter_block_items(parent: DocxDocument | _Cell) -> Iterator[Paragraph | Table]:
    """按文档顺序迭代段落与表格。"""
    if isinstance(parent, DocxDocument):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise TypeError(f"unsupported parent: {type(parent)!r}")

    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


def unique_row_cells(row) -> list:
    """去重合并单元格，避免 Markdown 表格重复列。"""
    seen: set[int] = set()
    cells = []
    for cell in row.cells:
        tc_id = id(cell._tc)
        if tc_id in seen:
            continue
        seen.add(tc_id)
        cells.append(cell)
    return cells


def escape_md_cell(text: str) -> str:
    """转义表格单元格中的 Markdown 特殊字符。"""
    return text.replace("|", "\\|").replace("\n", " ").strip()


def escape_html_cell(text: str) -> str:
    """转义 HTML 表格单元格文本。"""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("\n", " ")
        .strip()
    )


def _parse_word_table_rows(table: Table) -> list[list[dict]]:
    """
    解析 Word 表格 XML，提取 colspan / vMerge 信息。
    返回每行单元格列表；vMerge continue 单元格标记 skip=True。
    """
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    rows_data: list[list[dict]] = []

    for tr in table._tbl.findall("w:tr", ns):
        row_cells: list[dict] = []
        for tc in tr.findall("w:tc", ns):
            tc_pr = tc.find("w:tcPr", ns)
            colspan = 1
            vmerge: str | None = None
            if tc_pr is not None:
                grid_span = tc_pr.find("w:gridSpan", ns)
                if grid_span is not None:
                    colspan = int(grid_span.get(qn("w:val")))
                vm = tc_pr.find("w:vMerge", ns)
                if vm is not None:
                    vmerge = vm.get(qn("w:val")) or "continue"

            texts = [node.text or "" for node in tc.findall(".//w:t", ns)]
            text = escape_html_cell("".join(texts))

            if vmerge == "continue":
                row_cells.append({"skip": True, "colspan": colspan})
            else:
                row_cells.append(
                    {
                        "skip": False,
                        "text": text,
                        "colspan": colspan,
                        "vmerge": vmerge,
                        "rowspan": 1,
                    }
                )
        rows_data.append(row_cells)

    for ri, row in enumerate(rows_data):
        col_pos = 0
        for cell in row:
            if cell["skip"]:
                col_pos += cell["colspan"]
                continue
            if cell.get("vmerge") == "restart":
                cell["rowspan"] = _count_vmerge_rowspan(
                    rows_data, ri, col_pos, cell["colspan"]
                )
            col_pos += cell["colspan"]

    return rows_data


def _count_vmerge_rowspan(
    rows_data: list[list[dict]], start_row: int, col_start: int, colspan: int
) -> int:
    """计算纵向合并单元格的 rowspan。"""
    span = 1
    for ri in range(start_row + 1, len(rows_data)):
        col_pos = 0
        matched = False
        for cell in rows_data[ri]:
            if col_pos == col_start:
                if cell["skip"] and cell["colspan"] == colspan:
                    span += 1
                    matched = True
                break
            col_pos += cell["colspan"]
        if not matched:
            break
    return span


def _table_has_merges(rows_data: list[list[dict]]) -> bool:
    """判断表格是否含合并单元格。"""
    for row in rows_data:
        for cell in row:
            if cell["skip"]:
                return True
            if cell.get("colspan", 1) > 1:
                return True
            if cell.get("rowspan", 1) > 1:
                return True
    return False


def table_to_html(table: Table) -> str:
    """将含合并单元格的 Word 表格转为 HTML table（与 ipcs_sdd.md 风格一致）。"""
    rows_data = _parse_word_table_rows(table)
    if not rows_data:
        return ""

    lines = [
        '<table border="1" cellspacing="0" cellpadding="4">',
        "<tbody>",
    ]
    for row in rows_data:
        lines.append("<tr>")
        for cell in row:
            if cell["skip"]:
                continue
            attrs: list[str] = []
            if cell["colspan"] > 1:
                attrs.append(f'colspan="{cell["colspan"]}"')
            if cell.get("rowspan", 1) > 1:
                attrs.append(f'rowspan="{cell["rowspan"]}"')
            attr_str = (" " + " ".join(attrs)) if attrs else ""
            lines.append(f"<td{attr_str}>{cell['text']}</td>")
        lines.append("</tr>")
    lines.extend(["</tbody>", "</table>"])
    return "\n".join(lines)


def table_to_markdown(table: Table) -> str:
    """将 Word 表格转为 Markdown；含合并单元格时输出 HTML table。"""
    rows_data = _parse_word_table_rows(table)
    if not rows_data:
        return ""

    if _table_has_merges(rows_data):
        return table_to_html(table)

    md_rows: list[list[str]] = []
    for row in rows_data:
        md_rows.append([c["text"] for c in row if not c["skip"]])

    col_count = max(len(r) for r in md_rows)
    for row in md_rows:
        while len(row) < col_count:
            row.append("")

    lines = [
        "| " + " | ".join(md_rows[0]) + " |",
        "|" + "|".join(["---"] * col_count) + "|",
    ]
    for row in md_rows[1:]:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def parse_toc_entry(text: str) -> tuple[int, str] | None:
    """
    解析 TOC 段落，如 ``1.1\\tConfidentiality 保密性\\t9``。
    返回 (markdown_level, full_heading_text)。
    """
    parts = text.split("\t")
    if len(parts) < 2:
        return None
    num, title = parts[0].strip(), parts[1].strip()
    if not title or title.isdigit():
        return None
    if "CONTENTS" in num or "CONTENTS" in title:
        return None
    full = f"{num} {title}" if num else title
    depth = num.count(".") + 1 if re.match(r"^\d", num) else 1
    return depth, full


def toc_title_matches(full: str, body_text: str) -> bool:
    """判断 TOC 完整标题是否与 Word 正文标题匹配。"""
    if not body_text:
        return False
    title_part = full.split(" ", 1)[1] if " " in full else full
    return (
        body_text == title_part
        or body_text == full
        or body_text in full
        or title_part.endswith(body_text)
        or body_text in title_part
    )


def is_extra_heading(body_text: str) -> bool:
    """Word 中不在 TOC 内的附加标题（OSAL 分节、TODO、附录等）。"""
    markers = (
        "OSAL(",
        "OSAL（",
        "Linux部署",
        "双向追溯",
        "TODO 核心场景",
        "（todo）",
        "(todo)",
    )
    return any(m in body_text for m in markers)


def resolve_heading(
    toc_queue: list[tuple[int, str]],
    body_text: str,
    style: str,
) -> str:
    """根据 Word 标题样式与 TOC 匹配/顺序生成 Markdown 标题行。"""
    word_level = HEADING_STYLE_LEVEL[style]
    hashes = "#" * word_level

    if body_text:
        for i, (_depth, full) in enumerate(toc_queue):
            if toc_title_matches(full, body_text):
                toc_queue.pop(i)
                return f"{hashes} {full}"

        if is_extra_heading(body_text):
            return f"{hashes} {body_text}"

        # 章级标题文本可能与 TOC 不一致（如「单元划分」），顺序消费下一条
        if style == "Heading 1" and toc_queue:
            _depth, full = toc_queue.pop(0)
            return f"{hashes} {full}"

        return f"{hashes} {body_text}"

    if toc_queue:
        _depth, full = toc_queue.pop(0)
        return f"{hashes} {full}"

    return f"{hashes} {body_text}"


def build_toc_markdown(entries: list[tuple[int, str]]) -> str:
    """由 TOC 条目生成嵌套 bullet 目录（与 ipcs_sdd.md 风格一致）。"""
    lines = ["## CONTENTS 目录", ""]
    for depth, full in entries:
        indent = "  " * (depth - 1)
        lines.append(f"{indent}- {full}")
    return "\n".join(lines)


def paragraph_inline_md(paragraph: Paragraph) -> str:
    """提取段落文本，保留 run 级粗体。"""
    parts: list[str] = []
    for run in paragraph.runs:
        if run._element.xpath(".//a:blip"):
            continue
        text = run.text
        if not text:
            continue
        if run.bold:
            parts.append(f"**{text}**")
        else:
            parts.append(text)
    result = "".join(parts).strip()
    return result if result else paragraph.text.strip()


def extract_images(
    paragraph: Paragraph,
    doc: DocxDocument,
    media_dir: Path,
    counter: list[int],
) -> list[str]:
    """从段落提取内嵌图片，保存到 media_dir，返回 Markdown 图片引用。"""
    lines: list[str] = []
    rel_prefix = media_dir.name

    for run in paragraph.runs:
        for blip in run._element.xpath(".//a:blip"):
            r_id = blip.get(qn("r:embed"))
            if not r_id or r_id not in doc.part.related_parts:
                continue
            part = doc.part.related_parts[r_id]
            ctype = part.content_type
            if "svg" in ctype:
                ext = "svg"
            elif "png" in ctype:
                ext = "png"
            elif "jpeg" in ctype or "jpg" in ctype:
                ext = "jpg"
            elif "emf" in ctype:
                ext = "emf"
            else:
                ext = "bin"

            counter[0] += 1
            fname = f"image{counter[0]}.{ext}"
            out_path = media_dir / fname
            out_path.write_bytes(part.blob)

            alt = paragraph_inline_md(paragraph) or fname
            alt = alt.replace("[", "").replace("]", "")
            lines.append(f"![{alt}]({rel_prefix}/{fname})")

    return lines


def collect_toc_entries(doc: DocxDocument) -> list[tuple[int, str]]:
    """收集正文 TOC 条目（跳过 CONTENTS 自身）。"""
    entries: list[tuple[int, str]] = []
    for para in doc.paragraphs:
        level = TOC_STYLE_LEVEL.get(para.style.name)
        if level is None:
            continue
        parsed = parse_toc_entry(para.text)
        if parsed:
            entries.append(parsed)
    return entries


def convert_docx_to_md(docx_path: Path, md_path: Path, media_dir: Path) -> None:
    """主转换逻辑。"""
    doc = Document(str(docx_path))
    toc_entries = collect_toc_entries(doc)
    toc_queue = list(toc_entries)
    img_counter = [0]

    if media_dir.exists():
        for f in media_dir.iterdir():
            if f.is_file():
                f.unlink()
    media_dir.mkdir(parents=True, exist_ok=True)

    out: list[str] = []
    phase = "cover"  # cover -> toc_skip -> content
    toc_emitted = False
    blank_pending = False

    def emit_blank() -> None:
        nonlocal blank_pending
        if out and out[-1] != "":
            out.append("")
        blank_pending = False

    def emit_line(line: str) -> None:
        nonlocal blank_pending
        if line == "":
            blank_pending = True
            return
        if blank_pending or (out and out[-1] != ""):
            if out and out[-1] != "":
                out.append("")
        out.append(line)
        blank_pending = False

    for block in iter_block_items(doc):
        if isinstance(block, Table):
            if phase == "toc_skip":
                continue
            md_table = table_to_markdown(block)
            if md_table:
                emit_line(md_table)
            continue

        para: Paragraph = block
        style = para.style.name
        text = paragraph_inline_md(para)

        if style in SKIP_STYLES:
            imgs = extract_images(para, doc, media_dir, img_counter)
            for img in imgs:
                emit_line(img)
            continue

        if style == "Title" and phase == "cover" and text:
            emit_line(text)
            continue

        if style == "Heading 2" and text == "CONTENTS 目录":
            phase = "toc_skip"
            if not toc_emitted:
                emit_line(build_toc_markdown(toc_entries))
                toc_emitted = True
            continue

        if phase == "toc_skip":
            if style.startswith("toc"):
                continue
            if style.startswith("Heading") and style in HEADING_STYLE_LEVEL:
                phase = "content"
            elif style == "Compact":
                continue
            else:
                continue

        if phase == "cover":
            if not text and not para._element.xpath(".//a:blip"):
                continue
            if text:
                emit_line(text)
            imgs = extract_images(para, doc, media_dir, img_counter)
            for img in imgs:
                emit_line(img)
            continue

        # content phase
        if style.startswith("Heading") and style in HEADING_STYLE_LEVEL:
            if not text and style == "Heading 2":
                continue
            emit_line(resolve_heading(toc_queue, text, style))
            continue

        if not text:
            imgs = extract_images(para, doc, media_dir, img_counter)
            for img in imgs:
                emit_line(img)
            continue

        if style == "Block Text":
            emit_line(f"> {text}")
        elif style == "First Paragraph" and text.startswith("`"):
            emit_line(f"> {text}")
        else:
            emit_line(text)

        imgs = extract_images(para, doc, media_dir, img_counter)
        for img in imgs:
            emit_line(img)

    # 清理末尾空行
    while out and out[-1] == "":
        out.pop()

    md_path.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"[ok] {docx_path.name} -> {md_path.name}")
    print(f"[ok] images: {img_counter[0]} -> {media_dir}/")


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert final_sdd.docx to Markdown.")
    parser.add_argument("docx", nargs="?", default=str(DEFAULT_DOCX), help="Source DOCX")
    parser.add_argument("md", nargs="?", default=str(DEFAULT_MD), help="Output Markdown")
    parser.add_argument(
        "--media",
        default=str(DEFAULT_MEDIA),
        help="Directory for extracted images",
    )
    args = parser.parse_args()

    docx_path = Path(args.docx)
    md_path = Path(args.md)
    media_dir = Path(args.media)

    if not docx_path.is_file():
        print(f"[error] DOCX not found: {docx_path}", file=sys.stderr)
        return 1

    convert_docx_to_md(docx_path, md_path, media_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

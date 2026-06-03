# -*- coding: utf-8 -*-
"""
Shared helpers for replacing ACTIVITY flow diagram inlines in Word (extent preserved).
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.shape import InlineShape

from format_final_sdd import _apply_shape_extents, _iter_body_paragraphs_in_order
from svg_extent_utils import parse_svg_viewbox_wh, svg_diagram_type, svg_text_from_inline

_SVG_BLIP_NS = "http://schemas.microsoft.com/office/drawing/2016/SVG/main"
_PLANTUML_SRC_RE = re.compile(r"<\?plantuml-src[^?]*\?>", re.DOTALL)
_EMU_PER_INCH = 914400


@dataclass
class FlowInlineRecord:
    index: int
    content_id: str
    cx: int
    cy: int
    cx_cm: float
    cy_cm: float
    svg_text: str
    inline_el: object


def normalize_svg(text: str) -> str:
    return _PLANTUML_SRC_RE.sub("", text or "").strip()


def content_id_for_svg(text: str) -> str:
    return hashlib.sha256(normalize_svg(text).encode("utf-8")).hexdigest()[:16]


def inline_extent_emu(inline_el) -> tuple[int, int]:
    ext = inline_el.find(qn("wp:extent"))
    if ext is None:
        return 0, 0
    return int(ext.get("cx") or 0), int(ext.get("cy") or 0)


def emu_to_cm(cx: int, cy: int) -> tuple[float, float]:
    return round(cx / _EMU_PER_INCH * 2.54, 4), round(cy / _EMU_PER_INCH * 2.54, 4)


def is_activity_svg_inline(inline_el, doc: Document) -> bool:
    svg = svg_text_from_inline(inline_el, doc)
    return bool(svg) and svg_diagram_type(svg) == "ACTIVITY"


def _blip_embed_part(inline_el, doc: Document):
    blip = inline_el.find(".//" + qn("a:blip"))
    if blip is None:
        return None
    rid = blip.get(qn("r:embed"))
    if not rid:
        return None
    return doc.part.related_parts.get(rid)


def is_flow_emf_inline(inline_el, doc: Document) -> bool:
    """Prior EMF pass: main blip embeds ``image/x-emf`` (ACTIVITY flow diagrams)."""
    part = _blip_embed_part(inline_el, doc)
    return part is not None and "emf" in part.content_type


def is_flow_png_inline(inline_el, doc: Document) -> bool:
    """Prior PNG pass: main blip embeds ``image/png`` (ACTIVITY flow diagrams)."""
    part = _blip_embed_part(inline_el, doc)
    return part is not None and "png" in part.content_type


def replace_inline_blip_image(
    inline_el, doc: Document, image_path: Path, cx: int, cy: int
) -> None:
    blip = inline_el.find(".//" + qn("a:blip"))
    if blip is None:
        raise RuntimeError("no a:blip")
    svg_blip = blip.find(f"{{{_SVG_BLIP_NS}}}svgBlip")
    if svg_blip is not None:
        blip.remove(svg_blip)
    ext_lst = blip.find(qn("a:extLst"))
    if ext_lst is not None:
        blip.remove(ext_lst)

    r_id, _ = doc.part.get_or_add_image(str(image_path.resolve()))
    blip.set(qn("r:embed"), r_id)
    link = blip.get(qn("r:link"))
    if link is not None:
        blip.attrib.pop(qn("r:link"), None)

    shape = InlineShape(inline_el)
    _apply_shape_extents(shape, cx, cy)


def parse_extent_report(report_path: Path) -> list[dict[str, str | int]]:
    if not report_path.is_file():
        return []
    lines = report_path.read_text(encoding="utf-8").splitlines()
    rows: list[dict[str, str | int]] = []
    for line in lines:
        if not line or line.startswith("docx:") or line.startswith("activity"):
            continue
        if line.startswith("unique") or line.startswith("replaced"):
            continue
        if line.startswith("emf_dir") or line.startswith("svg_cache"):
            continue
        if line.startswith("png_dir"):
            continue
        if line.startswith("index\t"):
            continue
        if line.startswith("---"):
            continue
        parts = line.split("\t")
        if len(parts) < 6 or not parts[0].isdigit():
            continue
        rows.append(
            {
                "index": int(parts[0]),
                "content_id": parts[1],
                "cx": int(parts[2]),
                "cy": int(parts[3]),
            }
        )
    return rows


def load_svg_text(content_id: str, svg_src_dirs: list[Path], inline_svg: str | None) -> str:
    if inline_svg:
        return inline_svg
    for d in svg_src_dirs:
        p = d / f"{content_id}.svg"
        if p.is_file():
            return p.read_text(encoding="utf-8")
    raise FileNotFoundError(f"SVG source missing for content_id={content_id}")


def _append_from_report_row(
    records: list[FlowInlineRecord],
    inline_el,
    row: dict[str, str | int],
    cx: int,
    cy: int,
    svg_src_dirs: list[Path],
) -> None:
    cid = str(row["content_id"])
    if int(row["cx"]) != cx or int(row["cy"]) != cy:
        print(
            f"[warn] extent mismatch #{row['index']} {cid}: "
            f"report {row['cx']}x{row['cy']} vs docx {cx}x{cy}"
        )
    svg_text = ""
    try:
        svg_text = load_svg_text(cid, svg_src_dirs, None)
    except FileNotFoundError:
        pass
    cx_cm, cy_cm = emu_to_cm(cx, cy)
    records.append(
        FlowInlineRecord(
            index=len(records) + 1,
            content_id=cid,
            cx=cx,
            cy=cy,
            cx_cm=cx_cm,
            cy_cm=cy_cm,
            svg_text=svg_text,
            inline_el=inline_el,
        )
    )


def collect_activity_flow_inlines(
    doc: Document,
    *,
    emf_report_path: Path | None = None,
    png_report_path: Path | None = None,
    svg_src_dirs: list[Path] | None = None,
) -> list[FlowInlineRecord]:
    """Collect ACTIVITY flow inlines (SVG / EMF / PNG from prior passes)."""
    emf_rows = parse_extent_report(emf_report_path) if emf_report_path else []
    png_rows = parse_extent_report(png_report_path) if png_report_path else []
    emf_row_idx = 0
    png_row_idx = 0
    src_dirs = svg_src_dirs or []
    records: list[FlowInlineRecord] = []
    wp_inline = qn("wp:inline")

    for p_el in _iter_body_paragraphs_in_order(doc.element.body):
        for inline_el in p_el.findall(".//" + wp_inline):
            svg = svg_text_from_inline(inline_el, doc)
            if svg and svg_diagram_type(svg) == "ACTIVITY":
                cx, cy = inline_extent_emu(inline_el)
                if cx <= 0 or cy <= 0:
                    continue
                cx_cm, cy_cm = emu_to_cm(cx, cy)
                records.append(
                    FlowInlineRecord(
                        index=len(records) + 1,
                        content_id=content_id_for_svg(svg),
                        cx=cx,
                        cy=cy,
                        cx_cm=cx_cm,
                        cy_cm=cy_cm,
                        svg_text=svg,
                        inline_el=inline_el,
                    )
                )
                continue

            if is_flow_png_inline(inline_el, doc):
                cx, cy = inline_extent_emu(inline_el)
                if cx <= 0 or cy <= 0:
                    continue
                if png_row_idx >= len(png_rows):
                    raise RuntimeError(
                        "DOCX 含 PNG 流程图，但缺少 "
                        f"{png_report_path} 中的 extent 记录"
                    )
                row = png_rows[png_row_idx]
                png_row_idx += 1
                _append_from_report_row(records, inline_el, row, cx, cy, src_dirs)
                continue

            if not is_flow_emf_inline(inline_el, doc):
                continue

            cx, cy = inline_extent_emu(inline_el)
            if cx <= 0 or cy <= 0:
                continue
            if emf_row_idx >= len(emf_rows):
                raise RuntimeError(
                    "DOCX 含 EMF 流程图，但缺少 "
                    f"{emf_report_path} 中的 extent 记录"
                )
            row = emf_rows[emf_row_idx]
            emf_row_idx += 1
            _append_from_report_row(records, inline_el, row, cx, cy, src_dirs)

def collect_emf_flow_inlines(
    doc: Document,
    *,
    emf_report_path: Path | None = None,
    svg_src_dirs: list[Path] | None = None,
) -> list[FlowInlineRecord]:
    """Collect ACTIVITY flow inlines that embed ``image/x-emf`` only."""
    emf_rows = parse_extent_report(emf_report_path) if emf_report_path else []
    emf_row_idx = 0
    src_dirs = svg_src_dirs or []
    records: list[FlowInlineRecord] = []
    wp_inline = qn("wp:inline")

    for p_el in _iter_body_paragraphs_in_order(doc.element.body):
        for inline_el in p_el.findall(".//" + wp_inline):
            if not is_flow_emf_inline(inline_el, doc):
                continue
            cx, cy = inline_extent_emu(inline_el)
            if cx <= 0 or cy <= 0:
                continue
            if emf_row_idx >= len(emf_rows):
                raise RuntimeError(
                    "DOCX 含 EMF 流程图，但缺少 "
                    f"{emf_report_path} 中的 extent 记录"
                )
            row = emf_rows[emf_row_idx]
            emf_row_idx += 1
            _append_from_report_row(records, inline_el, row, cx, cy, src_dirs)

    return records


def add_emf_image_part(doc: Document, emf_path: Path) -> str:
    """Register EMF bytes (python-docx 不识别 .emf 扩展名)。"""
    from docx.opc.constants import RELATIONSHIP_TYPE as RT
    from docx.opc.packuri import PackURI
    from docx.opc.part import Part

    existing = {part.partname for part in doc.part.package.iter_parts()}
    for i in range(1, 10000):
        partname = PackURI(f"/word/media/flow_{i}.emf")
        if partname not in existing:
            break
    else:
        raise RuntimeError("no free EMF part name")

    blob = emf_path.read_bytes()
    part = Part(partname, "image/x-emf", blob, doc.part.package)
    return doc.part.relate_to(part, RT.IMAGE)


def replace_inline_with_emf(
    inline_el, doc: Document, emf_path: Path, cx: int, cy: int
) -> None:
    blip = inline_el.find(".//" + qn("a:blip"))
    if blip is None:
        raise RuntimeError("no a:blip")
    svg_blip = blip.find(f"{{{_SVG_BLIP_NS}}}svgBlip")
    if svg_blip is not None:
        blip.remove(svg_blip)
    ext_lst = blip.find(qn("a:extLst"))
    if ext_lst is not None:
        blip.remove(ext_lst)

    r_id = add_emf_image_part(doc, emf_path)
    blip.set(qn("r:embed"), r_id)
    link = blip.get(qn("r:link"))
    if link is not None:
        blip.attrib.pop(qn("r:link"), None)

    shape = InlineShape(inline_el)
    _apply_shape_extents(shape, cx, cy)


_MD_FLOW_SVG_RE = re.compile(r"!\[\]\((cursor_tmp/flow_svgs/[^)]+\.svg)\)")


def list_activity_flow_svg_paths(
    md_path: Path, *, workspace_root: Path
) -> list[Path]:
    """Return ACTIVITY flow SVG paths in ``md_sdd_0519.md`` appearance order."""
    text = md_path.read_text(encoding="utf-8")
    out: list[Path] = []
    for rel in _MD_FLOW_SVG_RE.findall(text):
        svg_path = (workspace_root / rel).resolve()
        if not svg_path.is_file():
            raise FileNotFoundError(f"Missing flow SVG: {svg_path}")
        head = svg_path.read_text(encoding="utf-8")[:800]
        if svg_diagram_type(head) != "ACTIVITY":
            continue
        out.append(svg_path)
    return out


def display_extent_from_svg_file(svg_path: Path, cx: int, cy: int) -> tuple[int, int]:
    """Keep EMF display width ``cx``; adjust ``cy`` from SVG viewBox aspect ratio."""
    wh = parse_svg_viewbox_wh(svg_path.read_text(encoding="utf-8"))
    if wh is None or cx <= 0:
        return cx, cy
    w, h = wh
    if w <= 0 or h <= 0:
        return cx, cy
    new_cy = max(1, int(round(cx * h / w)))
    return cx, new_cy


def add_svg_image_part(doc: Document, svg_path: Path) -> str:
    """Register SVG bytes for ``asvg:svgBlip`` embedding."""
    from docx.opc.constants import RELATIONSHIP_TYPE as RT
    from docx.opc.packuri import PackURI
    from docx.opc.part import Part

    existing = {part.partname for part in doc.part.package.iter_parts()}
    for i in range(1, 10000):
        partname = PackURI(f"/word/media/flow_svg_{i}.svg")
        if partname not in existing:
            break
    else:
        raise RuntimeError("no free SVG part name")

    blob = svg_path.read_bytes()
    part = Part(partname, "image/svg+xml", blob, doc.part.package)
    return doc.part.relate_to(part, RT.IMAGE)


def replace_inline_with_svg(
    inline_el, doc: Document, svg_path: Path, cx: int, cy: int
) -> None:
    """Replace EMF/PNG blip with Pandoc-style ``asvg:svgBlip`` (extent preserved)."""
    from docx.oxml import parse_xml

    blip = inline_el.find(".//" + qn("a:blip"))
    if blip is None:
        raise RuntimeError("no a:blip")

    for child in list(blip):
        blip.remove(child)
    for attr in (qn("r:embed"), qn("r:link")):
        if attr in blip.attrib:
            blip.attrib.pop(attr, None)

    r_id = add_svg_image_part(doc, svg_path)
    ext_lst = parse_xml(
        f'<a:extLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        f'xmlns:a14="http://schemas.microsoft.com/office/drawing/2010/main" '
        f'xmlns:asvg="{_SVG_BLIP_NS}" '
        f'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f'<a:ext uri="{{28A0092B-C50C-407E-A947-70E740481C1C}}">'
        f'<a14:useLocalDpi xmlns:a14="http://schemas.microsoft.com/office/drawing/2010/main" val="0"/>'
        f"</a:ext>"
        f'<a:ext uri="{{96DAC541-7B7A-43D3-8B79-37D633B846F1}}">'
        f'<asvg:svgBlip xmlns:asvg="{_SVG_BLIP_NS}" r:embed="{r_id}"/>'
        f"</a:ext>"
        f"</a:extLst>"
    )
    blip.append(ext_lst)

    shape = InlineShape(inline_el)
    _apply_shape_extents(shape, cx, cy)

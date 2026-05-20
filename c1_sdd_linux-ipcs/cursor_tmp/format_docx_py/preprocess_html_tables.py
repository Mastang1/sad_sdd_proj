# -*- coding: utf-8 -*-
r"""
将 MD 中带 colspan/rowspan 的 HTML 表格展开为 Pandoc 可稳定转换的网格表。

Pandoc 对复杂合并单元格常会压扁多行，导致「函数定义文件」等行并入上一格。
本模块在 Pandoc 之前把每张表展开为规则矩形网格（保留 colspan 仅作横向合并）。

使用：由 ``md0519_to_final_sdd.py`` 在写入 ``_pandoc_md0519.md`` 前调用。
"""

from __future__ import annotations

import re
from html.parser import HTMLParser
from typing import Any

_TABLE_RE = re.compile(r"<table\b[^>]*>.*?</table>", re.IGNORECASE | re.DOTALL)


class _TableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.rows: list[list[dict[str, Any]]] = []
        self._row: list[dict[str, Any]] | None = None
        self._cell: dict[str, Any] | None = None
        self._buf: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        ad = {k: (v or "") for k, v in attrs}
        if tag == "tr":
            self._row = []
        elif tag in ("td", "th") and self._row is not None:
            self._cell = {
                "tag": tag,
                "colspan": int(ad.get("colspan", "1") or "1"),
                "rowspan": int(ad.get("rowspan", "1") or "1"),
            }
            self._buf = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in ("td", "th") and self._cell is not None and self._row is not None:
            self._cell["text"] = "".join(self._buf).strip()
            self._row.append(self._cell)
            self._cell = None
            self._buf = []
        elif tag == "tr" and self._row is not None:
            if self._row:
                self.rows.append(self._row)
            self._row = None

    def handle_data(self, data: str) -> None:
        if self._cell is not None:
            self._buf.append(data)


def _build_grid(rows: list[list[dict[str, Any]]]) -> list[list[str]]:
    grid: list[list[str | None]] = []
    col_count = 0

    for r_idx, row in enumerate(rows):
        while len(grid) <= r_idx:
            grid.append([])
        c_idx = 0

        for cell in row:
            while c_idx < len(grid[r_idx]) and grid[r_idx][c_idx] is not None:
                c_idx += 1
            need = c_idx + cell["colspan"]
            if need > col_count:
                col_count = need
            for r in range(r_idx, r_idx + cell["rowspan"]):
                while len(grid) <= r:
                    grid.append([])
                while len(grid[r]) < col_count:
                    grid[r].append(None)
            for dr in range(cell["rowspan"]):
                for dc in range(cell["colspan"]):
                    rr, cc = r_idx + dr, c_idx + dc
                    while len(grid) <= rr:
                        grid.append([])
                    while len(grid[rr]) <= cc:
                        grid[rr].append(None)
                    grid[rr][cc] = cell["text"] if (dr == 0 and dc == 0) else ""
            c_idx += cell["colspan"]

    out: list[list[str]] = []
    for row in grid:
        while len(row) < col_count:
            row.append("")
        out.append([(c if c is not None else "") for c in row[:col_count]])
    return out


def _grid_to_html(grid: list[list[str]]) -> str:
    lines = ['<table border="1" cellspacing="0" cellpadding="4">', "<tbody>"]
    for row in grid:
        lines.append("<tr>")
        for text in row:
            esc = (
                text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )
            lines.append(f"<td>{esc}</td>")
        lines.append("</tr>")
    lines.extend(["</tbody>", "</table>"])
    return "\n".join(lines)


def expand_html_table(html: str) -> str:
    parser = _TableParser()
    parser.feed(html)
    if not parser.rows:
        return html
    grid = _build_grid(parser.rows)
    return _grid_to_html(grid)


def preprocess_md_html_tables(md_text: str) -> tuple[str, int]:
    count = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal count
        expanded = expand_html_table(m.group(0))
        if expanded != m.group(0):
            count += 1
        return expanded

    return _TABLE_RE.sub(repl, md_text), count

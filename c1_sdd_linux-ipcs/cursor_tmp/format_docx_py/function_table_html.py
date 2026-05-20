# -*- coding: utf-8 -*-
"""
Build SDD function-design HTML tables (§4.4 / §5.4 reference layout).

Canonical template: ``md_sdd_0519.md`` §4.4 Internal Functions — 5 columns,
``rowspan``/``colspan`` on 输入/输出参数 and 返回值, ``border="1" cellspacing="0" cellpadding="4"``.
"""

from __future__ import annotations

import re
from html import escape

TABLE_OPEN = '<table border="1" cellspacing="0" cellpadding="4">\n<tbody>'
TABLE_CLOSE = "</tbody>\n</table>"

_PIPE_FUNC_TABLE = re.compile(
    r"(###\s+(\d+\.\d+(?:\.\d+)?)\s+\S+)\s*\n\n"
    r"\| 项 \| 内容 \|\n"
    r"\|[-:]+\|[-:]+\|\n"
    r"((?:\|[^\n]+\|\n)+)",
    re.MULTILINE,
)


def _row(label: str, value: str, *, label_colspan: int | None = None) -> str:
    val = escape(value.strip())
    if label_colspan:
        return f"<tr>\n<td>{escape(label)}</td>\n<td colspan=\"{label_colspan}\">{val}</td>\n</tr>\n"
    return f"<tr>\n<td>{escape(label)}</td>\n<td colspan=\"4\">{val}</td>\n</tr>\n"


def _parse_params(text: str, prototype: str) -> list[tuple[str, str, str, str]]:
    """Return list of (I/O, name, dtype, description)."""
    raw = text.strip()
    if raw in ("-", ""):
        return []

    params: list[tuple[str, str, str, str]] = []
    for chunk in re.split(r"<br\s*/?>", raw, flags=re.I):
        chunk = chunk.strip()
        if not chunk:
            continue
        m = re.match(r"`([^`]+)`\s*:\s*`([^`]+)`", chunk)
        if m:
            name, dtype = m.group(1).strip(), m.group(2).strip()
            params.append(("I", name, dtype, f"[IN] {name}"))
            continue
        m = re.match(r"`([^`]+)`", chunk)
        if m:
            name = m.group(1).strip()
            params.append(("I", name, "-", f"[IN] {name}"))
    if params:
        return params

    # Fallback: parse formal parameters from prototype
    m = re.search(r"\(([^)]*)\)", prototype)
    if not m or not m.group(1).strip():
        return []
    for part in m.group(1).split(","):
        part = part.strip()
        if not part or part == "void":
            continue
        part = re.sub(r"\b(const|volatile|struct|enum)\b", "", part).strip()
        tokens = part.split()
        if not tokens:
            continue
        name = tokens[-1].lstrip("*")
        dtype = part[: part.rfind(name)].strip() or part
        params.append(("I", name, dtype, f"[IN] {name}"))
    return params


def _params_rows(params: list[tuple[str, str, str, str]]) -> str:
    if not params:
        return _row("输入/输出参数", "-")
    n = len(params) + 1
    out = [f'<tr>\n<td rowspan="{n}">输入/输出参数</td>\n<td>I/O</td>\n<td>参数名</td>\n<td>数据类型</td>\n<td>说明</td>\n</tr>\n']
    for io, name, dtype, desc in params:
        out.append(
            f"<tr>\n<td>{escape(io)}</td>\n<td>{escape(name)}</td>\n"
            f"<td>{escape(dtype)}</td>\n<td>{escape(desc)}</td>\n</tr>\n"
        )
    return "".join(out)


def _return_rows(ret: str) -> str:
    ret = ret.strip().strip("`")
    if ret in ("-", "", "void") or re.match(r"^void\b", ret):
        return (
            '<tr>\n<td rowspan="2">返回值</td>\n<td colspan="2">数据类型</td>\n'
            '<td colspan="2">说明</td>\n</tr>\n'
            "<tr>\n<td colspan=\"4\">-</td>\n</tr>\n"
        )
    return (
        '<tr>\n<td rowspan="2">返回值</td>\n<td colspan="2">数据类型</td>\n'
        '<td colspan="2">说明</td>\n</tr>\n'
        f"<tr>\n<td colspan=\"2\">{escape(ret)}</td>\n"
        f'<td colspan="2">-</td>\n</tr>\n'
    )


def build_function_table_html(
    *,
    arch_id: str,
    unit_id: str,
    description: str,
    prototype: str,
    constraints: str,
    params_text: str,
    return_type: str,
    def_file: str,
    decl_file: str,
) -> str:
    """Emit reference-style HTML function table (5 logical columns)."""
    proto = prototype.strip().strip("`")
    parts = [
        TABLE_OPEN + "\n",
        _row("对应软件架构ID", arch_id),
        _row("软件单元 ID", unit_id),
        _row("函数说明", description),
        _row("函数原型", proto),
        _row("制约条件", constraints if constraints.strip() not in ("", "-") else "-"),
        _params_rows(_parse_params(params_text, proto)),
        _return_rows(return_type),
        _row("函数定义文件", def_file),
        _row("函数声明文件", decl_file if decl_file.strip() else "-"),
        TABLE_CLOSE,
    ]
    return "".join(parts)


def parse_pipe_function_table(pipe_body: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in pipe_body.strip().splitlines():
        m = re.match(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$", line)
        if not m:
            continue
        key = m.group(1).strip()
        val = m.group(2).strip()
        rows[key] = val
    return rows


def pipe_block_to_html(pipe_body: str) -> str:
    r = parse_pipe_function_table(pipe_body)
    arch = r.get("对应软件架构 ID", r.get("对应软件架构ID", "-"))
    return build_function_table_html(
        arch_id=arch,
        unit_id=r.get("软件单元 ID", "-"),
        description=r.get("函数说明", "-"),
        prototype=r.get("函数原型", "-"),
        constraints=r.get("制约条件", "-"),
        params_text=r.get("输入/输出参数", "-"),
        return_type=r.get("返回值", "-"),
        def_file=r.get("函数定义文件", "-"),
        decl_file=r.get("函数声明文件", "-"),
    )


def convert_pipe_function_tables(md_text: str, *, chapter_prefix: str = "6.") -> tuple[str, int]:
    """Replace ``| 项 | 内容 |`` blocks under ### {chapter_prefix}* with HTML tables."""

    def repl(m: re.Match[str]) -> str:
        heading = m.group(1).strip()
        section = m.group(2)
        if not section.startswith(chapter_prefix):
            return m.group(0)
        pipe_body = m.group(3)
        html = pipe_block_to_html(pipe_body)
        return f"{heading}\n\n{html}\n\n"

    new_md, n = _PIPE_FUNC_TABLE.subn(repl, md_text)
    return new_md, n


def validate_table_shape(table_html: str) -> list[str]:
    """Basic structural checks against §4.4 template."""
    errs: list[str] = []
    if 'border="1"' not in table_html or "cellspacing=\"0\"" not in table_html:
        errs.append("missing border/spacing attributes")
    if "对应软件架构ID" not in table_html:
        errs.append("missing 对应软件架构ID row")
    if "rowspan" not in table_html and "输入/输出参数" in table_html:
        if "colspan=\"4\">-</td>" not in table_html.replace(" ", ""):
            errs.append("params without rowspan/colspan layout")
    if "返回值" not in table_html:
        errs.append("missing 返回值 section")
    return errs

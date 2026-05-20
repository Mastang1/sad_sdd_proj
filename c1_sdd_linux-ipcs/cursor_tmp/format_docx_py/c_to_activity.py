# -*- coding: utf-8 -*-
"""Heuristic C function body -> PlantUML activity diagram body (no @startuml)."""

from __future__ import annotations

import re
from pathlib import Path

HEADER = """\
@startuml
!pragma layout smetana
skinparam conditionStyle insideDiamond
skinparam linetype ortho
"""

MAX_NODES = 42


def strip_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    text = re.sub(r"//[^\n]*", "", text)
    return text


def extract_function_body(source: str, func_name: str) -> str | None:
    src = strip_comments(source)
    pat = re.compile(
        rf"(?:^|\n)(?:static\s+|inline\s+)*(?:const\s+)?[\w\s]+\*?\s*{re.escape(func_name)}\s*\(",
        re.MULTILINE,
    )
    m = pat.search(src)
    if not m:
        return None
    i = m.end()
    while i < len(src) and src[i] != "{":
        if src[i] == ";":
            return None
        i += 1
    if i >= len(src):
        return None
    depth = 0
    start = i
    while i < len(src):
        c = src[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return src[start + 1 : i]
        i += 1
    return None


def _short_label(expr: str, limit: int = 48) -> str:
    s = " ".join(expr.split())
    s = s.replace('"', "'")
    s = s.replace("&", "\\&")
    if len(s) > limit:
        s = s[: limit - 3] + "..."
    return s


def _sanitize_line(line: str) -> str:
    if line.strip() == "break":
        return "break"
    if line.startswith(":") and line.rstrip().endswith(";"):
        inner = line[1:].strip()
        if inner == "break;":
            return "break"
    return line


def _find_matching_paren(s: str, open_pos: int) -> int:
    depth = 0
    i = open_pos
    while i < len(s):
        if s[i] == "(":
            depth += 1
        elif s[i] == ")":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def _find_block_brace(s: str, start: int) -> int | None:
    i = start
    while i < len(s) and s[i].isspace():
        i += 1
    if i >= len(s) or s[i] != "{":
        return None
    depth = 0
    while i < len(s):
        if s[i] == "{":
            depth += 1
        elif s[i] == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return None


def _stmt_until_semicolon(s: str) -> tuple[str, int]:
    depth = 0
    i = 0
    while i < len(s):
        c = s[i]
        if c in "({":
            depth += 1
        elif c in ")}":
            depth -= 1
        elif c == ";" and depth == 0:
            return s[: i].strip(), i + 1
        i += 1
    return s.strip(), len(s)


class _Gen:
    def __init__(self) -> None:
        self.lines: list[str] = []
        self.n = 0

    def emit(self, line: str) -> bool:
        if self.n >= MAX_NODES:
            return False
        self.lines.append(_sanitize_line(line))
        self.n += 1
        return True

    def _advance(self, body: str, pos: int, rest: str, consumed: int) -> int:
        return (len(body) - len(rest)) + consumed

    def _parse_braced(self, tail: str) -> int:
        """Parse braced block or single statement after condition. Returns chars consumed from tail."""
        tail = tail.lstrip()
        b2 = _find_block_brace(tail, 0)
        if b2 is not None:
            inner = tail[1:b2]
            self.parse_block(inner)
            return b2 + 1
        stmt, adv = _stmt_until_semicolon(tail)
        if stmt:
            self._emit_simple(stmt)
        return adv

    def parse_block(self, body: str) -> None:
        pos = 0
        body = body.strip()
        while pos < len(body) and self.n < MAX_NODES:
            rest = body[pos:].lstrip()
            if not rest:
                break
            pos += len(body[pos:]) - len(rest)

            if rest.startswith("}"):
                pos += 1
                continue

            if rest.startswith("else if"):
                m = re.match(r"else\s+if\s*\(", rest)
                assert m
                p0 = m.end() - 1
                p1 = _find_matching_paren(rest, p0)
                cond = rest[p0 + 1 : p1]
                self.emit("else (no)")
                self.emit(f"if ({_short_label(cond)}?) then (yes)")
                tail_ei = rest[p1 + 1 :].lstrip()
                used = p1 + 1 + (len(rest[p1 + 1 :]) - len(tail_ei))
                used += self._parse_braced(tail_ei)
                pos += used
                continue

            if rest.startswith("else"):
                self.emit("else (no)")
                used = 4 + self._parse_braced(rest[4:])
                pos += used
                continue

            if rest.startswith("if"):
                m = re.match(r"if\s*\(", rest)
                assert m
                p0 = m.end() - 1
                p1 = _find_matching_paren(rest, p0)
                cond = rest[p0 + 1 : p1]
                self.emit(f"if ({_short_label(cond)}?) then (yes)")
                tail = rest[p1 + 1 :].lstrip()
                used = p1 + 1 + (len(rest[p1 + 1 :]) - len(tail))
                used += self._parse_braced(tail)
                tail2 = rest[used:].lstrip()
                used += len(rest[used:]) - len(tail2)
                if tail2.startswith("else"):
                    self.emit("else (no)")
                    used += 4
                    used += self._parse_braced(tail2[4:])
                self.emit("endif")
                pos += used
                continue

            if rest.startswith("while"):
                m = re.match(r"while\s*\(", rest)
                p0 = m.end() - 1
                p1 = _find_matching_paren(rest, p0)
                cond = rest[p0 + 1 : p1]
                self.emit(f"while ({_short_label(cond)}?) is (yes)")
                tail_w = rest[p1 + 1 :].lstrip()
                used = p1 + 1 + (len(rest[p1 + 1 :]) - len(tail_w))
                used += self._parse_braced(tail_w)
                self.emit("endwhile (no)")
                pos += used
                continue

            if rest.startswith("for"):
                m = re.match(r"for\s*\(", rest)
                p0 = m.end() - 1
                p1 = _find_matching_paren(rest, p0)
                inner_for = rest[p0 + 1 : p1]
                parts = inner_for.split(";")
                cond = parts[1].strip() if len(parts) > 1 else "1"
                self.emit(f"while ({_short_label(cond)}?) is (yes)")
                tail_f = rest[p1 + 1 :].lstrip()
                used = p1 + 1 + (len(rest[p1 + 1 :]) - len(tail_f))
                used += self._parse_braced(tail_f)
                self.emit("endwhile (no)")
                pos += used
                continue

            if rest.startswith("do"):
                self.emit("repeat")
                used = 2
                b2 = _find_block_brace(rest, 2)
                if b2 is not None:
                    self.parse_block(rest[3:b2])
                    used = b2 + 1
                tail = rest[used:].lstrip()
                m = re.match(r"while\s*\(", tail)
                if m:
                    p0 = m.end() - 1
                    p1 = _find_matching_paren(tail, p0)
                    cond = tail[p0 + 1 : p1]
                    self.emit(f"repeat while ({_short_label(cond)}?) is (yes)")
                    used += p1 + 1
                pos += used
                continue

            if rest.startswith("return"):
                stmt, adv = _stmt_until_semicolon(rest)
                val = stmt.replace("return", "", 1).strip().rstrip(";")
                self.emit(f":return {_short_label(val, 32)};")
                self.emit("stop")
                return

            if rest.startswith("goto"):
                stmt, adv = _stmt_until_semicolon(rest)
                lbl = stmt.replace("goto", "", 1).strip().rstrip(";")
                self.emit(f":goto {lbl};")
                pos += adv
                continue

            stmt, adv = _stmt_until_semicolon(rest)
            if stmt:
                self._emit_simple(stmt)
            pos += adv

    def _emit_simple(self, stmt: str) -> None:
        stmt = stmt.strip()
        if not stmt:
            return
        if re.match(r"return\b", stmt):
            val = stmt.replace("return", "", 1).strip().rstrip(";")
            self.emit(f":return {_short_label(val, 32)};")
            self.emit("stop")
            return
        self.emit(f":{_short_label(stmt.rstrip(';'), 56)};")

    def result(self) -> str:
        lines = ["start", *self.lines]
        if not self.lines or self.lines[-1] != "stop":
            lines.append("stop")
        return "\n".join(lines)


def body_to_activity(body: str) -> str:
    g = _Gen()
    g.parse_block(body)
    return g.result()


def read_source_function(def_file: str, func_name: str, workspace: Path) -> str | None:
    path = workspace / def_file.replace("\\", "/").lstrip("/")
    if not path.is_file():
        path = workspace / "ipcs" / Path(def_file).name
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    body = extract_function_body(text, func_name)
    if body is None:
        return None
    return body_to_activity(body)


def write_puml(path: Path, title: str, activity_body: str, include_title: bool = False) -> None:
    parts = [HEADER.strip()]
    if include_title:
        parts.append(f"title {title}")
    parts.append(activity_body.strip())
    parts.append("@enduml")
    path.write_text("\n".join(parts) + "\n", encoding="utf-8")

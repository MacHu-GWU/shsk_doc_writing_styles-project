#!/usr/bin/env python3
"""Compare the structural skeleton of two Markdown files and report the differences."""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

EXCERPT_CHARS = 30

FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})\s*([^\s`]*)")
ATX_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
SETEXT_H1_RE = re.compile(r"^\s{0,3}=+\s*$")
SETEXT_H2_RE = re.compile(r"^\s{0,3}-+\s*$")
HRULE_RE = re.compile(r"^\s{0,3}(?:(?:-\s*){3,}|(?:\*\s*){3,}|(?:_\s*){3,})$")
BULLET_RE = re.compile(r"^(\s*)[-*+]\s+\S")
ORDERED_RE = re.compile(r"^(\s*)\d+[.)]\s+\S")
QUOTE_RE = re.compile(r"^\s{0,3}>")
TABLE_ROW_RE = re.compile(r"^\s{0,3}\|")
TABLE_DIVIDER_RE = re.compile(r"^[\s|:-]+$")
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(\s*([^)\s]*)")
INLINE_MD_RE = re.compile(r"[`*_~\[\]()#>|!]")


def display_width(text: str) -> int:
    """Terminal columns a string occupies, counting CJK characters as two."""
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in text)


def pad(text: str, width: int) -> str:
    """Left justify to a display width that accounts for double wide characters."""
    short = display_width(text)
    if short <= width:
        return text + " " * (width - short)
    out = ""
    used = 0
    for c in text:
        w = 2 if unicodedata.east_asian_width(c) in "WF" else 1
        if used + w > width:
            break
        out += c
        used += w
    return out + " " * (width - used)


def excerpt(text: str, limit: int = EXCERPT_CHARS) -> str:
    """A short, punctuation free sample of an element, for a human to recognize it by."""
    flat = INLINE_MD_RE.sub("", text)
    flat = re.sub(r"\s+", " ", flat).strip()
    return flat[:limit]


# --------------------------------------------------------------------------- #
# Elements
# --------------------------------------------------------------------------- #


@dataclass
class Element:
    """One block level thing a reader can see from across the room."""

    kind: str
    line: int
    detail: str = ""
    sample: str = ""
    payload: str = ""

    @property
    def label(self) -> str:
        return f"{self.kind} {self.detail}".strip()

    def display(self) -> str:
        left = self.label
        return f"{pad(left, 14)}{self.sample}" if self.sample else left


@dataclass
class Doc:
    path: Path
    elements: list[Element] = field(default_factory=list)

    @property
    def kinds(self) -> list[str]:
        return [e.kind for e in self.elements]


def parse(path: Path) -> Doc:
    """Walk a Markdown file once and collect its block elements in document order.

    Fenced code is handled first so nothing inside a fence is mistaken for structure.
    Front matter is skipped: it is metadata, not part of the reading order.
    """
    doc = Doc(path=path)
    lines = path.read_text(encoding="utf-8").splitlines()

    start = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                start = i + 1
                break

    fence: tuple[str, int] | None = None
    lang = ""
    body: list[str] = []
    fence_line = 0

    table: list[str] = []
    table_line = 0
    list_kind = ""
    list_items = 0
    list_line = 0
    in_quote = False
    quote_line = 0
    quote_text = ""

    def close_table() -> None:
        nonlocal table
        if len(table) >= 2:
            header = table[0]
            cols = len(header.strip().strip("|").split("|"))
            rows = sum(1 for r in table if not TABLE_DIVIDER_RE.match(r.strip()))
            doc.elements.append(
                Element("table", table_line, f"{rows}x{cols}",
                        excerpt(header.strip().strip("|").replace("|", " ")),
                        payload=f"{rows}x{cols}")
            )
        table = []

    def close_list() -> None:
        nonlocal list_kind, list_items
        if list_items:
            doc.elements.append(
                Element("list", list_line, f"{list_kind} x{list_items}",
                        payload=f"{list_kind}:{list_items}")
            )
        list_kind = ""
        list_items = 0

    def close_quote() -> None:
        nonlocal in_quote, quote_text
        if in_quote:
            doc.elements.append(Element("quote", quote_line, "", excerpt(quote_text)))
        in_quote = False
        quote_text = ""

    def close_all() -> None:
        close_table()
        close_list()
        close_quote()

    for index in range(start, len(lines)):
        line = lines[index]
        num = index + 1
        m = FENCE_RE.match(line)

        if fence is not None:
            char, length = fence
            if m and m.group(2)[0] == char and len(m.group(2)) >= length and not m.group(3):
                code = "\n".join(body)
                doc.elements.append(
                    Element("code", fence_line, lang or "plain",
                            f"{len(body)} lines", payload=code.strip())
                )
                fence = None
                lang = ""
                body = []
                continue
            body.append(line)
            continue

        if m and m.group(2):
            close_all()
            fence = (m.group(2)[0], len(m.group(2)))
            lang = m.group(3)
            fence_line = num
            body = []
            continue

        stripped = line.strip()

        if not stripped:
            close_all()
            continue

        atx = ATX_RE.match(line)
        if atx:
            close_all()
            level = len(atx.group(1))
            doc.elements.append(
                Element(f"h{level}", num, "", excerpt(atx.group(2)))
            )
            continue

        previous = lines[index - 1].strip() if index else ""
        if previous and not table:
            if SETEXT_H1_RE.match(line) or (SETEXT_H2_RE.match(line) and set(stripped) == {"-"}):
                close_all()
                level = 1 if SETEXT_H1_RE.match(line) else 2
                doc.elements.append(Element(f"h{level}", num - 1, "", excerpt(previous)))
                continue

        if HRULE_RE.match(line):
            close_all()
            doc.elements.append(Element("hr", num))
            continue

        if TABLE_ROW_RE.match(line):
            close_list()
            close_quote()
            if not table:
                table_line = num
            table.append(line)
            continue
        close_table()

        img = IMAGE_RE.search(line)
        if img and not QUOTE_RE.match(line):
            close_list()
            close_quote()
            doc.elements.append(
                Element("image", num, "", excerpt(img.group(1) or img.group(2)),
                        payload=img.group(2))
            )
            continue

        if QUOTE_RE.match(line):
            close_list()
            text = re.sub(r"^\s{0,3}>+\s?", "", line)
            if not in_quote:
                in_quote = True
                quote_line = num
                quote_text = text
            elif len(quote_text) < EXCERPT_CHARS * 2:
                quote_text += " " + text
            continue
        close_quote()

        bullet = BULLET_RE.match(line)
        ordered = ORDERED_RE.match(line)
        if bullet or ordered:
            kind = "ul" if bullet else "ol"
            if list_kind and list_kind != kind:
                close_list()
            if not list_items:
                list_line = num
            list_kind = kind
            list_items += 1
            continue
        if list_items and line[:1].isspace():
            continue
        close_list()

    close_all()
    if fence is not None:
        doc.elements.append(
            Element("code", fence_line, lang or "plain", f"{len(body)} lines",
                    payload="\n".join(body).strip())
        )
    return doc


# --------------------------------------------------------------------------- #
# Comparison
# --------------------------------------------------------------------------- #

# Kinds whose content should survive a translation untouched. Everything else is
# prose and gets compared on type and position only.
CONTENT_CHECKED = {"code": "code body", "table": "table shape", "image": "image path"}

# A line comment runs to the end of its own line and no further. The space after the
# marker keeps a shebang, a CLI flag such as --json, and a CSS color out of it.
LINE_COMMENT_RE = re.compile(r"(?m)(?:#|//|--|;)\s[^\n]*$")
BLOCK_COMMENT_RE = re.compile(r"<!--.*?-->|/\*.*?\*/", re.S)


def code_without_comments(body: str) -> str:
    """The code with its comments removed, for telling a real change from a translated one.

    Comments inside a code block are prose and are supposed to be translated. The code
    around them is not. Stripping comments before comparing separates the expected
    difference from the defect, which keeps the report quiet enough to be worth reading.
    The stripping is a heuristic and can be fooled by a hash inside a string literal, so
    it is only ever used to *downgrade* a difference, never to hide one that the raw
    comparison did not already find.
    """
    stripped = BLOCK_COMMENT_RE.sub("", body)
    stripped = LINE_COMMENT_RE.sub("", stripped)
    return re.sub(r"\s+", " ", stripped).strip()


@dataclass
class Row:
    mark: str
    left: Element | None
    right: Element | None
    note: str = ""


def align(left: Doc, right: Doc) -> tuple[list[Row], list[str]]:
    """Pair the two element sequences up by type, and report where they part ways."""
    rows: list[Row] = []
    problems: list[str] = []
    matcher = difflib.SequenceMatcher(None, left.kinds, right.kinds, autojunk=False)

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                le, re_ = left.elements[i1 + k], right.elements[j1 + k]
                note = ""
                if le.kind in CONTENT_CHECKED and le.payload != re_.payload:
                    if le.kind == "code" and code_without_comments(
                        le.payload
                    ) == code_without_comments(re_.payload):
                        # Only the comments moved, which is what should happen.
                        rows.append(Row("~", le, re_, "comments translated, code identical"))
                        continue
                    note = f"{CONTENT_CHECKED[le.kind]} differs"
                    problems.append(
                        f"{le.kind} at {left.path.name}:{le.line} and "
                        f"{right.path.name}:{re_.line}: {note}"
                    )
                rows.append(Row("=" if not note else "!", le, re_, note))
        elif tag == "delete":
            for k in range(i1, i2):
                rows.append(Row("-", left.elements[k], None))
                problems.append(
                    f"only in {left.path.name}:{left.elements[k].line}: "
                    f"{left.elements[k].label} {left.elements[k].sample}".rstrip()
                )
        elif tag == "insert":
            for k in range(j1, j2):
                rows.append(Row("+", None, right.elements[k]))
                problems.append(
                    f"only in {right.path.name}:{right.elements[k].line}: "
                    f"{right.elements[k].label} {right.elements[k].sample}".rstrip()
                )
        else:  # replace
            span = max(i2 - i1, j2 - j1)
            for k in range(span):
                le = left.elements[i1 + k] if i1 + k < i2 else None
                re_ = right.elements[j1 + k] if j1 + k < j2 else None
                rows.append(Row("x", le, re_))
                problems.append(
                    f"mismatch: {left.path.name} has "
                    f"{le.label if le else 'nothing'}, {right.path.name} has "
                    f"{re_.label if re_ else 'nothing'}"
                )
    return rows, problems


# --------------------------------------------------------------------------- #
# Reporting
# --------------------------------------------------------------------------- #

COL = 46


def render(left: Doc, right: Doc, rows: list[Row], problems: list[str],
           inventory: bool) -> str:
    out: list[str] = []
    out.append(f"left  : {left.path}   ({len(left.elements)} elements)")
    out.append(f"right : {right.path}   ({len(right.elements)} elements)")
    out.append("")

    if inventory:
        for name, doc in (("left", left), ("right", right)):
            out.append(f"{name} inventory")
            for i, e in enumerate(doc.elements, 1):
                out.append(f"  {i:>3}  line {e.line:>4}  {e.display()}")
            out.append("")

    out.append(f"  {'#':>3}  {pad(left.path.name, COL)}    {right.path.name}")
    out.append("  " + "-" * (COL + 58))
    for i, r in enumerate(rows, 1):
        lt = r.left.display() if r.left else ""
        rt = r.right.display() if r.right else ""
        out.append(f"  {i:>3}  {pad(lt, COL)}  {r.mark}  {rt}")
        if r.note:
            out.append(f"       {' ' * COL}     ^ {r.note}")
    out.append("")

    if problems:
        out.append(f"DIVERGES  {len(problems)} finding(s)")
        out.append("")
        for p in problems:
            out.append(f"  {p}")
    else:
        out.append("AGREES  same element sequence, and code, tables, and images match")
    out.append("")
    out.append("  legend  =  same kind        -  only on the left     x  different kind")
    out.append("          !  content differs   +  only on the right")
    out.append("          ~  code comments translated, the code itself is unchanged")
    return "\n".join(out)


def _main(
    left: Path,
    right: Path,
    inventory: bool = False,
    json_output: bool = False,
) -> int:
    """Compare the structural skeleton of two Markdown files and report the differences.

    Reads only. This never edits a file and never suggests a rewrite. It prints what the
    two documents are made of, side by side, and where the two sequences stop agreeing.
    Deciding what to do about that is somebody else's job.

    It is language agnostic. Cross-language pairs are the usual case, so headings and
    prose are matched on element type and position, never on text. The text excerpt in
    the report is there for a human to eyeball, not for the comparison. Three element
    kinds do carry content that should survive a translation unchanged, so those are
    compared for real: code block bodies, table dimensions, and image paths. Comments
    inside a code block are prose and are expected to be translated, so a block whose
    comments moved but whose code did not is reported without being counted as a finding.

    Returns an exit code: 0 when the two skeletons agree, 1 when they diverge, 2 when a
    path is not a readable file.
    """
    for path in (left, right):
        if not path.is_file():
            print(f"ERROR: not a file: {path}", file=sys.stderr)
            return 2

    left_doc, right_doc = parse(left), parse(right)
    rows, problems = align(left_doc, right_doc)

    if json_output:
        print(json.dumps({
            "left": str(left),
            "right": str(right),
            "agrees": not problems,
            "elements": {
                "left": len(left_doc.elements),
                "right": len(right_doc.elements),
            },
            "rows": [{
                "mark": r.mark,
                "left": None if not r.left else {
                    "kind": r.left.kind, "line": r.left.line,
                    "detail": r.left.detail, "sample": r.left.sample},
                "right": None if not r.right else {
                    "kind": r.right.kind, "line": r.right.line,
                    "detail": r.right.detail, "sample": r.right.sample},
                "note": r.note,
            } for r in rows],
            "findings": problems,
        }, ensure_ascii=False, indent=2))
    else:
        print(render(left_doc, right_doc, rows, problems, inventory))

    return 1 if problems else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="structure_report",
        description="Compare the structural skeleton of two Markdown files. Reads only.",
    )
    parser.add_argument("--left", type=Path, required=True,
                        help="the document that was rewritten from")
    parser.add_argument("--right", type=Path, required=True,
                        help="the document to check against it")
    parser.add_argument("--inventory", action="store_true",
                        help="also list each file's elements on their own")
    parser.add_argument("--json_output", action="store_true",
                        help="emit machine readable JSON instead of the table")
    args = parser.parse_args(argv)
    return _main(
        left=args.left,
        right=args.right,
        inventory=args.inventory,
        json_output=args.json_output,
    )


if __name__ == "__main__":
    sys.exit(main())

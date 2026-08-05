#!/usr/bin/env python3
"""Regroup, renumber, and regenerate the index and reading copy of a Chinglish cases folder."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

CASE_DIR = re.compile(r"^(\d{4})-(.+)$")
FENCE = re.compile(r"^(```|~~~)")
INLINE_LINK = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")   # [text](url) and ![alt](src)
REF_LINK = re.compile(r"!?\[([^\]]*)\]\[[^\]]*\]")     # [text][ref]
CJK = re.compile(r"[一-鿿]")

META = "00-meta.toml"
SOURCE = "01-source.md"
LITERAL = "02-literal.md"
GOOD = "03-good.md"

# Groups sort in this order, which is the canonical case-type order from chinglish-spec.
# Anything unrecognized sorts after all of these, alphabetically among themselves.
TYPE_ORDER = ["sentence", "paragraph", "passage", "bullet-list", "diagram"]

EXCERPT_CHARS = 50


class CaseError(Exception):
    """A case directory is malformed enough that reordering the folder is unsafe."""


def load_meta(path: Path) -> dict[str, str]:
    """Parse 00-meta.toml.

    Falls back to a line parser when tomllib is unavailable (Python < 3.11). The
    fallback is safe because the spec constrains these files to flat `key = "value"`
    pairs on single lines with basic strings.
    """
    text = path.read_text(encoding="utf-8")
    try:
        import tomllib

        return tomllib.loads(text)
    except ImportError:
        pass

    out: dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, sep, value = line.partition("=")
        if not sep:
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
        out[key.strip()] = value
    return out


def group_rank(group: str) -> tuple[int, int, str]:
    """Sort rank for a group, putting the canonical types first and in order."""
    if group in TYPE_ORDER:
        return (0, TYPE_ORDER.index(group), "")
    return (1, 0, group)


def read_case(directory: Path) -> dict[str, object]:
    """Load one case directory into a record, or raise CaseError if it is unusable."""
    match = CASE_DIR.match(directory.name)
    if match is None:
        raise CaseError(f"{directory.name} is not a NNNN-slug directory")

    meta_path = directory / META
    if not meta_path.exists():
        raise CaseError(f"{directory.name} has no {META}")

    meta = load_meta(meta_path)
    case_type = str(meta.get("type", "")).strip()
    group = str(meta.get("group") or case_type).strip()
    if not group:
        raise CaseError(f"{directory.name} has neither `group` nor `type` in {META}")

    return {
        "dir": directory,
        "number": int(match.group(1)),
        "slug": match.group(2),
        "meta": meta,
        "type": case_type,
        "group": group,
    }


def preview_line(text: str) -> str:
    """The one line of a fragment worth previewing.

    The first line, not the whole fragment flattened: a bullet list previews as its
    first bullet, a passage as its opening line. Code-fence markers carry no content
    and are skipped, so a diagram case previews as its first real line. If that first
    line happens to hold no Chinese, look ahead for one, since the column this feeds
    is 中文原文.
    """
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line and not FENCE.match(line)]
    if not lines:
        return ""
    if CJK.search(lines[0]):
        return lines[0]
    for line in lines[1:]:
        if CJK.search(line):
            return line
    return lines[0]


def excerpt(case: dict[str, object]) -> str:
    """One-line, pipe-safe, truncated preview of the Chinese fragment.

    Markdown link syntax is reduced to its visible text before anything is counted, so
    a URL never eats the character budget and never widens the table.
    """
    path = case["dir"] / SOURCE  # type: ignore[operator]
    if not path.exists():
        return ""
    text = preview_line(path.read_text(encoding="utf-8"))
    text = INLINE_LINK.sub(r"\1", text)
    text = REF_LINK.sub(r"\1", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > EXCERPT_CHARS:
        text = text[:EXCERPT_CHARS] + "…"
    return text.replace("|", r"\|")


def renumber(cases: list[dict[str, object]], folder: Path, dry_run: bool) -> list[tuple[str, str]]:
    """Assign new numbers in sorted order. Returns the rename map that was applied."""
    moves: list[tuple[str, str]] = []
    for index, case in enumerate(cases, start=1):
        new_name = f"{index:04d}-{case['slug']}"
        if new_name != case["dir"].name:  # type: ignore[union-attr]
            moves.append((str(case["dir"].name), new_name))  # type: ignore[union-attr]
        case["new_name"] = new_name

    if not moves or dry_run:
        for case in cases:
            case["dir"] = folder / str(case["new_name"])
        return moves

    # Two phases, because a target name is very likely occupied by another case
    # that has not moved yet.
    staged: list[Path] = []
    for case in cases:
        current: Path = case["dir"]  # type: ignore[assignment]
        if current.name == case["new_name"]:
            staged.append(current)
            continue
        temp = folder / f".reindex-{case['new_name']}"
        shutil.move(str(current), str(temp))
        staged.append(temp)
    for case, temp in zip(cases, staged):
        final = folder / str(case["new_name"])
        if temp != final:
            shutil.move(str(temp), str(final))
        case["dir"] = final
    return moves


def write_index(cases: list[dict[str, object]], folder: Path) -> Path:
    """Write INDEX.md, the committed three-column table."""
    lines = [
        "# Chinglish cases",
        "",
        "| folder | type | 中文原文 |",
        "| :--- | :--- | :--- |",
    ]
    for case in cases:
        lines.append(f"| {case['dir'].name} | {case['type']} | {excerpt(case)} |")  # type: ignore[union-attr]
    lines.append("")
    out = folder / "INDEX.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def read_or(path: Path, fallback: str) -> str:
    """File contents stripped, or the fallback when missing or empty."""
    if not path.exists():
        return fallback
    text = path.read_text(encoding="utf-8").strip()
    return text if text else fallback


def write_view(cases: list[dict[str, object]], folder: Path) -> Path:
    """Write tmp/view.md, the uncommitted reading copy with all three versions inline."""
    counts: dict[str, int] = {}
    for case in cases:
        group = str(case["group"])
        counts[group] = counts.get(group, 0) + 1

    lines = [
        f"# Chinglish cases: {folder.name}",
        "",
        "由 `chinglish-index` 生成, 供人通读. 不要手改, 重跑脚本即可.",
        "",
        f"共 {len(cases)} 个 case: " + ", ".join(f"{g} {n}" for g, n in counts.items()) + ".",
        "",
    ]

    current = None
    for case in cases:
        directory: Path = case["dir"]  # type: ignore[assignment]
        group = str(case["group"])
        if group != current:
            current = group
            lines += ["---", "", f"**组: {current}** ({counts[current]} 个)", ""]

        lines += [f"## {directory.name}", ""]
        context = str(case["meta"].get("context", "")).strip()  # type: ignore[union-attr]
        if context:
            lines += [f"*{context}*", ""]

        lines += ["**中文**", "", read_or(directory / SOURCE, "*(缺失)*"), ""]
        lines += ["**烂翻译**", "", read_or(directory / LITERAL, "*(缺失)*"), ""]
        lines += ["**好翻译**", "", read_or(directory / GOOD, "*(尚未产出)*"), ""]

    out = folder / "tmp" / "view.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def _main(folder: Path, dry_run: bool = False) -> int:
    """Regroup, renumber, and regenerate a Chinglish cases folder in one pass.

    Three passes over the folder:

    1. Sort every case and renumber from 0001, with a collision-safe two-phase rename.
       The sort key is the case's group, then its slug. A case's group is `group` from
       its 00-meta.toml when that key is present, otherwise `type`. Sorting by slug
       rather than by the existing number makes the layout a function of the folder's
       content alone, so the result is stable across runs and reproducible across a
       re-collection. Nothing here induces groups; it only sorts by what the meta files
       already say.
    2. Write INDEX.md, which is committed.
    3. Write tmp/view.md, the reading copy, which is not.

    With dry_run set, prints the rename plan and changes nothing.

    Returns an exit code: 0 on success, 1 on failure.
    """
    if not folder.is_dir():
        print(f"ERROR: {folder} is not a directory", file=sys.stderr)
        return 1

    directories = sorted(d for d in folder.iterdir() if d.is_dir() and CASE_DIR.match(d.name))
    if not directories:
        print(f"no cases found in {folder}")
        return 0

    try:
        cases = [read_case(d) for d in directories]
    except CaseError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        print("ERROR: refusing to reorder a folder with malformed cases", file=sys.stderr)
        return 1

    unknown = sorted({str(c["group"]) for c in cases if c["group"] not in TYPE_ORDER})

    # Type first, in the canonical order, then slug. The number only breaks ties
    # between two cases that share both a group and a slug.
    cases.sort(key=lambda c: (group_rank(str(c["group"])), str(c["slug"]), int(c["number"])))  # type: ignore[arg-type]

    moves = renumber(cases, folder, dry_run)

    if dry_run:
        print(f"dry run over {len(cases)} cases in {folder}")
        for old, new in moves:
            print(f"  {old}  ->  {new}")
        if not moves:
            print("  already in order, nothing to rename")
        return 0

    index_path = write_index(cases, folder)
    view_path = write_view(cases, folder)

    counts: dict[str, int] = {}
    for case in cases:
        group = str(case["group"])
        counts[group] = counts.get(group, 0) + 1

    print(f"{len(cases)} cases in {folder}")
    print(f"  renamed: {len(moves)}")
    for old, new in moves:
        print(f"    {old}  ->  {new}")
    print("  groups: " + ", ".join(f"{g}={n}" for g, n in counts.items()))
    if unknown:
        print(f"  WARNING unrecognized groups, sorted last: {', '.join(unknown)}")
    print(f"  wrote {index_path}")
    print(f"  wrote {view_path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="reindex",
        description="Regroup, renumber, and regenerate INDEX.md and tmp/view.md for a Chinglish cases folder.",
    )
    parser.add_argument("--folder", type=Path, required=True, help="the Chinglish cases folder")
    parser.add_argument("--dry_run", action="store_true", help="show the rename plan, change nothing")
    args = parser.parse_args(argv)
    return _main(folder=args.folder, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())

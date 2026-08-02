# Changelog

All notable changes to the `chinese-english-punctuation` skill are documented here.

## [0.1.3] - 2026-08-01

- Drop the bundled `scripts/chinese_to_english_punctuation.py` linter. Lint by
  running the `chinese_to_english_punctuation` PyPI package's `c2ep` CLI via
  `uvx --from "chinese_to_english_punctuation>=0.1.2" c2ep file --path ...`
  instead, so this skill no longer maintains a duplicate implementation.

## [0.1.2] - 2026-07-29

- Ported bracket handling to a generic `BracketPair` table and extended it beyond
  `（）`/`“”` to `【】`, `［］`, `《》`, `〈〉`, `＜＞`, `｛｝`, including correct spacing
  for nested/adjacent pairs (e.g. `【《书名》】` -> `[<书名>]`).
- Preserve leading indentation (spaces/tabs) so Markdown/reST code blocks and list
  continuations are no longer mangled.
- Empty/whitespace-only lines, and lines that consist of a single punctuation mark,
  now normalize to an empty line instead of leaving stray whitespace.
- Ported from the latest `chinese_to_english_punctuation` implementation
  (`impl.py`), keeping this skill self-contained with no dependency on the PyPI
  package.

## [0.1.1] - 2026-07-04

- Initial release.
